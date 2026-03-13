"""
Sessions API endpoints - 練習セッション管理
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.core.database import get_db
from app.models.scenario import Scenario
from app.models.session import PracticeSession
from app.models.message import Message
from app.services.claude_service import generate_response, generate_session_summary

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


class StartSessionRequest(BaseModel):
    scenario_id: int


class SendMessageRequest(BaseModel):
    content: str


@router.post("")
async def start_session(req: StartSessionRequest, db: AsyncSession = Depends(get_db)):
    """新しい練習セッションを開始"""
    # シナリオを取得
    result = await db.execute(select(Scenario).where(Scenario.id == req.scenario_id))
    scenario = result.scalar_one_or_none()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # セッション作成
    session = PracticeSession(
        scenario_id=scenario.id,
        status="active",
        total_turns=0,
    )
    db.add(session)
    await db.flush()

    # AIの最初のメッセージを保存
    first_msg = Message(
        session_id=session.id,
        role="assistant",
        content=scenario.first_message,
        turn_number=1,
    )
    db.add(first_msg)
    session.total_turns = 1

    await db.commit()
    await db.refresh(session)

    return {
        "session_id": session.id,
        "scenario": {
            "id": scenario.id,
            "title": scenario.title,
            "title_ja": scenario.title_ja,
            "icon": scenario.icon,
            "estimated_turns": scenario.estimated_turns,
        },
        "first_message": {
            "role": "assistant",
            "content": scenario.first_message,
            "turn_number": 1,
        },
    }


@router.get("")
async def list_sessions(db: AsyncSession = Depends(get_db)):
    """セッション履歴一覧"""
    result = await db.execute(
        select(PracticeSession)
        .options(selectinload(PracticeSession.scenario))
        .order_by(PracticeSession.started_at.desc())
        .limit(50)
    )
    sessions = result.scalars().all()

    return [
        {
            "id": s.id,
            "scenario_title": s.scenario.title,
            "scenario_title_ja": s.scenario.title_ja,
            "scenario_icon": s.scenario.icon,
            "difficulty": s.scenario.difficulty,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            "total_turns": s.total_turns,
            "score": s.score,
            "status": s.status,
        }
        for s in sessions
    ]


@router.get("/{session_id}")
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """セッション詳細（メッセージ履歴含む）"""
    result = await db.execute(
        select(PracticeSession)
        .options(
            selectinload(PracticeSession.scenario),
            selectinload(PracticeSession.messages),
        )
        .where(PracticeSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "id": session.id,
        "scenario": {
            "id": session.scenario.id,
            "title": session.scenario.title,
            "title_ja": session.scenario.title_ja,
            "icon": session.scenario.icon,
            "estimated_turns": session.scenario.estimated_turns,
        },
        "status": session.status,
        "total_turns": session.total_turns,
        "score": session.score,
        "feedback_summary": session.feedback_summary,
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "ended_at": session.ended_at.isoformat() if session.ended_at else None,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "correction": m.correction,
                "feedback": m.feedback,
                "turn_number": m.turn_number,
            }
            for m in session.messages
        ],
    }


@router.post("/{session_id}/messages")
async def send_message(
    session_id: int,
    req: SendMessageRequest,
    db: AsyncSession = Depends(get_db),
):
    """ユーザーメッセージを送信し、AI応答を取得"""
    # セッション取得
    result = await db.execute(
        select(PracticeSession)
        .options(
            selectinload(PracticeSession.scenario),
            selectinload(PracticeSession.messages),
        )
        .where(PracticeSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Session is not active")

    # 会話履歴を構築
    conversation_history = [
        {"role": m.role, "content": m.content} for m in session.messages
    ]

    # Claude APIで応答生成
    ai_result = await generate_response(
        system_prompt=session.scenario.system_prompt,
        conversation_history=conversation_history,
        user_input=req.content,
    )

    current_turn = session.total_turns + 1

    # ユーザーメッセージを保存
    user_msg = Message(
        session_id=session.id,
        role="user",
        content=req.content,
        correction=ai_result.get("correction"),
        feedback=ai_result.get("feedback"),
        turn_number=current_turn,
    )
    db.add(user_msg)

    # AI応答メッセージを保存
    ai_msg = Message(
        session_id=session.id,
        role="assistant",
        content=ai_result["response"],
        turn_number=current_turn + 1,
    )
    db.add(ai_msg)

    session.total_turns = current_turn + 1

    # 会話終了判定
    should_end = ai_result.get("should_end", False)
    if should_end or session.total_turns >= session.scenario.estimated_turns * 2:
        session.status = "completed"
        session.ended_at = datetime.utcnow()

    await db.commit()

    return {
        "user_message": {
            "role": "user",
            "content": req.content,
            "correction": ai_result.get("correction"),
            "feedback": ai_result.get("feedback"),
            "turn_number": current_turn,
        },
        "ai_message": {
            "role": "assistant",
            "content": ai_result["response"],
            "turn_number": current_turn + 1,
        },
        "should_end": should_end,
        "session_status": session.status,
    }


@router.post("/{session_id}/end")
async def end_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """セッションを終了し、総合評価を取得"""
    result = await db.execute(
        select(PracticeSession)
        .options(
            selectinload(PracticeSession.scenario),
            selectinload(PracticeSession.messages),
        )
        .where(PracticeSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # 会話履歴からユーザーメッセージのみ抽出して評価
    conversation_history = [
        {"role": m.role, "content": m.content} for m in session.messages
    ]

    # 総合評価を生成
    summary = await generate_session_summary(
        scenario_title=session.scenario.title,
        conversation_history=conversation_history,
    )

    # セッション更新
    session.status = "completed"
    session.ended_at = datetime.utcnow()
    session.score = summary.get("score", 0)
    session.feedback_summary = (
        f"{summary.get('summary', '')}\n\n"
        f"【良かった点】\n" + "\n".join(f"・{s}" for s in summary.get("strengths", [])) + "\n\n"
        f"【改善点】\n" + "\n".join(f"・{s}" for s in summary.get("improvements", []))
    )

    await db.commit()

    return {
        "session_id": session.id,
        "score": session.score,
        "feedback_summary": session.feedback_summary,
        "summary": summary,
    }
