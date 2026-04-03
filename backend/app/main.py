from fastapi import FastAPI
from app.database import engine
from app import models
from app.conversation_service import reset_history
from app.ai_service import parse_user_command
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.task_service import create_task,get_today_plan,update_task, delete_task,analyze_workload
from app.schemas import AICommand

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "AIVA v2 backend running"}


@app.post("/ai-command")
def ai_command(command: AICommand, db: Session = Depends(get_db)):

    message = command.message

    if message.lower() == "/reset":
        reset_history()
        return {"message": "Conversation reset"}

    ai_result = parse_user_command(message)

    intent = ai_result.get("intent")

    if intent == "create_task":
        task = create_task(db, ai_result)
        return {"message": "Task created", "task": task}

    if intent == "today_plan":
        tasks = get_today_plan(db)

        if len(tasks) == 0:
            return {"message": "No tasks found"}

        return {"today_plan": tasks}
    
    if intent == "generate_study_plan":
        return {
            "message": "Here is your suggested study plan",
            "plan": ai_result.get("plan")
        }

    if intent == "update_task":

        task = update_task(db, ai_result)

        if not task:
            return {"message": "Task not found"}

        return {
            "message": "Task updated successfully",
            "task": task
        }

    if intent == "delete_task":

        task = delete_task(db, ai_result)

        if not task:
            return {"message": "Task not found"}

        return {
            "message": "Task deleted successfully"
        }

    if intent == "analyze_workload":

        analysis = analyze_workload(db)

        if analysis["status"] == "overloaded":
            message = (
                f"You have {analysis['total_hours']} hours scheduled this week. "
                f"Average per day: {analysis['avg_per_day']} hours. "
                "This might be heavy."
            )
        else:
            message = (
                f"You have {analysis['total_hours']} hours scheduled this week. "
                f"Average per day: {analysis['avg_per_day']} hours. "
                "Your workload looks manageable."
            )

        return {"message": message}

    return {
        "message": "I couldn't understand the request.",
        "ai_interpretation": ai_result
    }


@app.post("/approve-plan")
def approve_plan(plan: dict, db: Session = Depends(get_db)):

    created_tasks = []

    for day in plan.get("plan", []):
        for task_title in day["tasks"]:

            task = create_task(db, {
                "title": task_title,
                "category": "Study Plan",
                "estimated_hours": 1,
                "deadline": None
            })

            created_tasks.append(task)

    return {
        "message": "Study plan added successfully",
        "tasks": created_tasks
    }