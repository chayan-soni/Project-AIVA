import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.conversation_service import add_message, get_history

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are AIVA, an AI academic assistant.

Your job is to convert the user's message into structured JSON.

Available intents:

create_task
update_task
delete_task
today_plan
list_tasks
check_overload
generate_study_plan

Return ONLY JSON.

Example:

User: Add DSA practice tomorrow for 2 hours

Response:
{
  "intent": "create_task",
  "title": "DSA practice",
  "category": "Competitive",
  "estimated_hours": 2,
  "deadline": "tomorrow"
}

If the user asks for a study plan:

User: Plan my study for next 3 days

Response:
{
  "intent": "generate_study_plan",
  "days": 3,
  "plan": [
    {"day": 1, "tasks": ["DSA practice", "Assignment work"]},
    {"day": 2, "tasks": ["Project work", "Revision"]},
    {"day": 3, "tasks": ["Mock test", "Weak topics"]}
  ]
}

If the user wants to modify a task, return JSON like:

{
 "intent": "update_task",
 "target": "DSA practice",
 "field": "estimated_hours",
 "value": 3
}

If the user wants to delete a task:

{
 "intent": "delete_task",
 "target": "DSA practice"
}

If the user asks about workload or being overloaded, return:

{
 "intent": "analyze_workload"
}
"""


def parse_user_command(user_message: str):

    add_message("user", user_message)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + get_history()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    content = response.choices[0].message.content

    add_message("assistant", content)

    try:
        return json.loads(content)
    except:
        return {"intent": "unknown"}