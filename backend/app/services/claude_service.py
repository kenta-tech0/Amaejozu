"""
Claude API service - AI会話エンジン
"""

import json
from anthropic import Anthropic
from app.core.config import settings


client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)


async def generate_response(
    system_prompt: str,
    conversation_history: list[dict],
    user_input: str,
) -> dict:
    """
    シナリオに沿ったAI応答とフィードバックを生成する。

    Returns:
        {
            "response": "AI's English reply in the scenario",
            "correction": "文法修正（日本語）",
            "feedback": "表現のアドバイス（日本語）",
            "should_end": false
        }
    """
    messages = []
    for msg in conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_input})

    full_system = f"""{system_prompt}

IMPORTANT INSTRUCTIONS FOR EVERY RESPONSE:
You must respond in valid JSON format with these fields:
- "response": Your English reply staying in character for the scenario. Keep it natural and conversational (2-4 sentences).
- "correction": If the user's English has grammar or vocabulary errors, provide the corrected version in Japanese. Explain what was wrong and show the correct form. If the user's English was correct, set this to null.
- "feedback": Provide a brief tip in Japanese about the user's expression, suggesting more natural alternatives or praising good usage. If nothing notable, set this to null.
- "should_end": Set to true if the conversation has reached a natural conclusion, otherwise false.

Respond ONLY with the JSON object, no other text."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=full_system,
        messages=messages,
    )

    text = response.content[0].text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        result = {
            "response": text,
            "correction": None,
            "feedback": None,
            "should_end": False,
        }

    return result


async def generate_session_summary(
    scenario_title: str,
    conversation_history: list[dict],
) -> dict:
    """
    セッション終了時の総合評価を生成する。

    Returns:
        {
            "score": 75,
            "summary": "総合フィードバック（日本語）",
            "strengths": ["良かった点1", "良かった点2"],
            "improvements": ["改善点1", "改善点2"]
        }
    """
    conversation_text = ""
    for msg in conversation_history:
        role = "You" if msg["role"] == "user" else "AI"
        conversation_text += f"{role}: {msg['content']}\n"

    messages = [
        {
            "role": "user",
            "content": f"""以下は「{scenario_title}」というシナリオでの英会話練習の記録です。

{conversation_text}

この会話を評価して、以下のJSON形式で回答してください:
- "score": 0-100の総合スコア（文法の正確さ、語彙の豊富さ、会話の自然さを考慮）
- "summary": 総合フィードバック（日本語、3-4文）
- "strengths": 良かった点のリスト（日本語、2-3個）
- "improvements": 改善すべき点のリスト（日本語、2-3個）

JSON形式のみで回答してください。""",
        }
    ]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=messages,
    )

    text = response.content[0].text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        result = {
            "score": 50,
            "summary": "評価を生成できませんでした。",
            "strengths": [],
            "improvements": [],
        }

    return result
