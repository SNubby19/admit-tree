from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Literal, Union


# -------------------------
# Small scalar ADTs
# -------------------------
LeadershipLevel = Literal[1, 2, 3, 4, 5]  # 1=member ... 3-4=president ... 5=top leadership
ImpactLevel = Literal[1, 2, 3, 4, 5]

Interest = Literal[
    "programming",
    "robotics",
    "math",
    "physics",
    "biology",
    "chem",
]

TaskStatus = Literal["done", "to do", "in progress"]


# -------------------------
# Academic ADTs
# -------------------------
@dataclass
class CourseWithGrade:
    course_name: str
    course_code: Optional[str] = None
    grade: Optional[float] = None  # can be % or GPA; normalize later


@dataclass
class PlannedCourse:
    course_name: str
    course_code: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class Grade12OrAbove:
    kind: Literal["grade_12_or_above"]
    gpa_or_average: float
    courses_taken: List[CourseWithGrade]


@dataclass
class BelowGrade12:
    kind: Literal["below_grade_12"]
    grade_level: int  # 9, 10, 11
    current_average: Optional[float]
    courses_so_far: List[CourseWithGrade]
    planned_courses: List[PlannedCourse]


AcademicInfo = Union[Grade12OrAbove, BelowGrade12]


# -------------------------
# Extracurricular ADT
# -------------------------
@dataclass
class Extracurricular:
    name: str
    leadership_level: LeadershipLevel
    role_title: Optional[str] = None
    impact_level: Optional[ImpactLevel] = None
    hours_per_week: Optional[float] = None
    months: Optional[int] = None
    notes: Optional[str] = None


# -------------------------
# Preference + links + transcript
# -------------------------
@dataclass
class PathwayPreference:
    coop_importance: int      # 0–10
    research_importance: int  # 0–10


@dataclass
class Links:
    resume_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None


@dataclass
class TranscriptInfo:
    kind: Literal["file_upload", "none"]
    file_id: Optional[str] = None
    file_name: Optional[str] = None

@dataclass
class Program:
    school: str
    program: str


# -------------------------
# Root ADT (your "User")
# -------------------------
@dataclass
class User:
    name: str
    email: str

    academic: AcademicInfo
    extracurriculars: List[Extracurricular]
    interests: List[Interest]

    pathway_preference: PathwayPreference
    links: Links


    programs: List[Program]    
    transcript: Optional[TranscriptInfo] = None
    roadmap: Optional[Roadmap] = None


# -------------------------
# Roadmap ADT
# -------------------------
@dataclass
class Task:
    content: str
    deadline: str  # ISO 8601 format: "YYYY-MM-DD"
    status: TaskStatus = "to do"


@dataclass
class Roadmap:
    school: str
    program: str
    tasks: List[Task]
    progress: int
    deadline: str  # ISO 8601 format: "YYYY-MM-DD"
    done: List[int]
    toDo: List[int]
    inProgress: List[int]