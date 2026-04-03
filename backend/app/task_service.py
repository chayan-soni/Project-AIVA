from sqlalchemy.orm import Session
from app import models
from app.date_utils import parse_deadline
from datetime import datetime,timedelta


def calculate_priority(deadline, hours):

    score = 0

    if deadline:
        days_left = (deadline - datetime.utcnow().date()).days

        if days_left <= 1:
            score += 100
        elif days_left <= 3:
            score += 70
        elif days_left <= 7:
            score += 40
        else:
            score += 10

    if hours:
        score += hours * 5

    return score


def create_task(db: Session, data: dict):

    parsed_deadline = parse_deadline(data.get("deadline"))

    priority = calculate_priority(
        parsed_deadline,
        data.get("estimated_hours")
    )

    task = models.Task(
        title=data.get("title"),
        category=data.get("category"),
        estimated_hours=data.get("estimated_hours"),
        deadline=str(parsed_deadline),
        priority_score=priority
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def update_task(db: Session, data: dict):

    target = data.get("target")

    task = db.query(models.Task).filter(
        models.Task.title.ilike(f"%{target}%")
    ).first()

    if not task:
        return None

    field = data.get("field")
    value = data.get("value")

    if field == "estimated_hours":
        task.estimated_hours = int(value)

    if field == "deadline":
        task.deadline = value

    db.commit()
    db.refresh(task)

    return task

def delete_task(db: Session, data: dict):

    target = data.get("target")

    task = db.query(models.Task).filter(
        models.Task.title.ilike(f"%{target}%")
    ).first()

    if not task:
        return None

    db.delete(task)
    db.commit()

    return task

def get_today_plan(db: Session):

    tasks = (
        db.query(models.Task)
        .filter(models.Task.completed == False)
        .order_by(models.Task.priority_score.desc())
        .limit(3)
        .all()
    )

    return tasks

def analyze_workload(db: Session):

    tasks = db.query(models.Task).filter(
        models.Task.completed == False
    ).all()

    total_hours = 0

    for task in tasks:
        if task.estimated_hours:
            total_hours += task.estimated_hours

    days = 7
    avg_hours = total_hours / days

    status = "manageable"

    if avg_hours > 6:
        status = "overloaded"

    return {
        "total_hours": total_hours,
        "avg_per_day": round(avg_hours, 2),
        "status": status
    }