import asyncio
import datetime
from app.models import Skill, User, Professional, Task, TaskTracker
from app.enums.task import Priority, Status
from core.db import Transactional, session, standalone_session


@standalone_session
async def seed_skills():
    # Seed the Skill table
    skills_data = ["Python", "Java", "SQL", "HTML", "CSS", "JavaScript", "C++", "React", "Node.js"]
    skills = [Skill(name=skill) for skill in skills_data]
    session.add_all(skills)


@standalone_session
async def seed_users():
    # Seed the User table
    users_data = [
        {"email": "user1@example.com", "user_name": "user1", "password": "user1password"},
        {"email": "user2@example.com", "user_name": "user2", "password": "user2password"},
        {"email": "user3@example.com", "user_name": "user3", "password": "user3password"},
        # Add more user data here
    ]

    users = [User(**user_data) for user_data in users_data]
    session.add_all(users)


@standalone_session
async def seed_professionals():
    # Seed the Professional table
    professionals_data = [
        {"first_name": "John", "last_name": "Doe", "user_id": 1},
        {"first_name": "Jane", "last_name": "Smith", "user_id": 2},
        {"first_name": "Mike", "last_name": "Johnson", "user_id": 3},
        # Add more professional data here
    ]

    professionals = [Professional(**professional_data) for professional_data in professionals_data]
    session.add_all(professionals)


@standalone_session
async def seed_tasks():
    # Seed the Task table
    tasks_data = [
        {"name": "Task 1", "priority": Priority.LOW, "status": Status.NEW},
        {"name": "Task 2", "priority": Priority.MEDIUM, "status": Status.IN_PROGRESS},
        {"name": "Task 3", "priority": Priority.HIGH, "status": Status.COMPLETED},
        # Add more task data here
    ]

    tasks = [Task(**task_data) for task_data in tasks_data]
    session.add_all(tasks)


async def main():
    await seed_skills()
    await seed_users()
    await seed_professionals()
    await seed_tasks()


# def seed_task_trackers(session):
#     # Seed the TaskTracker table
#     task_trackers_data = [
#         {"start_time": datetime.datetime(2023, 7, 25, 12, 0, 0), "end_time": datetime.datetime(2023, 7, 25, 14, 0, 0), "task_id": 1, "professional_id": 1},
#         {"start_time": datetime.datetime(2023, 7, 25, 15, 0, 0), "end_time": datetime.datetime(2023, 7, 25, 17, 0, 0), "task_id": 2, "professional_id": 2},
#         {"start_time": datetime.datetime(2023, 7, 25, 18, 0, 0), "end_time": datetime.datetime(2023, 7, 25, 20, 0, 0), "task_id": 3, "professional_id": 3},
#         # Add more task tracker data here
#     ]
#
#     task_trackers = [TaskTracker(**tracker_data) for tracker_data in task_trackers_data]
#     session.add_all(task_trackers)

if __name__ == "__main__":
    asyncio.run(main())
    # seed_task_trackers(session)
