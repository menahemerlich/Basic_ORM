from typing import Optional
from sqlmodel import SQLModel, Field
from sqlmodel import create_engine
from sqlmodel import Session, select

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    hours: int
    is_active: bool = True

engine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/courses", echo=True)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def add_course(name: str, hours: int, is_active: bool = True) -> None:
    course = Course(name=name, hours=hours, is_active=is_active)
    with Session(engine) as session:
        session.add(course)
        session.commit()
        session.refresh(course)
        print(f"Added course with id = {course.id}")

def get_active_courses() -> list[Course]:
    with Session(engine) as session:
        statement = select(Course).where(Course.is_active == True)
        results = session.exec(statement)
        courses = results.all()
        return courses


if __name__ == "__main__":
    create_db_and_tables()

    add_course("SQL Basics", 20, True)
    add_course("Python Intro", 30, True)
    add_course("Legacy system", 10, False)

    active = get_active_courses()
    print("Active courses:")
    for c in active:
        print(f"{c.id}: {c.name} ({c.hours} hours) active = {c.is_active}")

