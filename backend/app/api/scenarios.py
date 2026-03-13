"""
Scenarios API endpoints - シナリオ一覧・詳細
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.scenario import Scenario

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


@router.get("")
async def list_scenarios(
    category: str | None = None,
    difficulty: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """シナリオ一覧を取得"""
    query = select(Scenario)
    if category:
        query = query.where(Scenario.category == category)
    if difficulty:
        query = query.where(Scenario.difficulty == difficulty)
    query = query.order_by(Scenario.difficulty, Scenario.id)

    result = await db.execute(query)
    scenarios = result.scalars().all()

    return [
        {
            "id": s.id,
            "title": s.title,
            "title_ja": s.title_ja,
            "description": s.description,
            "description_ja": s.description_ja,
            "difficulty": s.difficulty,
            "category": s.category,
            "icon": s.icon,
            "estimated_turns": s.estimated_turns,
        }
        for s in scenarios
    ]


@router.get("/{scenario_id}")
async def get_scenario(scenario_id: int, db: AsyncSession = Depends(get_db)):
    """シナリオ詳細を取得"""
    result = await db.execute(select(Scenario).where(Scenario.id == scenario_id))
    scenario = result.scalar_one_or_none()

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return {
        "id": scenario.id,
        "title": scenario.title,
        "title_ja": scenario.title_ja,
        "description": scenario.description,
        "description_ja": scenario.description_ja,
        "difficulty": scenario.difficulty,
        "category": scenario.category,
        "icon": scenario.icon,
        "estimated_turns": scenario.estimated_turns,
        "first_message": scenario.first_message,
    }
