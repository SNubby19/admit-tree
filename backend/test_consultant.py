"""
Terminal test script for the Gemini Consultant
"""

from consultant.consultant import Consultant, ConsultantError
from consultant.mockdata.user import (
    User, BelowGrade12, Extracurricular, PathwayPreference, Links,
    CourseWithGrade, PlannedCourse, Task, Roadmap, Subtask
)


def create_sample_user() -> User:
    """Create a sample user for testing"""
    return User(
        name="Alex Chen",
        email="alex.chen@example.com",
        academic=BelowGrade12(
            kind="below_grade_12",
            grade_level=11,
            current_average=92.5,
            courses_so_far=[
                CourseWithGrade(course_name="Advanced Functions", course_code="MHF4U", grade=94.0),
                CourseWithGrade(course_name="Physics", course_code="SPH4U", grade=91.0),
                CourseWithGrade(course_name="Chemistry", course_code="SCH4U", grade=93.0),
            ],
            planned_courses=[
                PlannedCourse(
                    course_name="Calculus and Vectors",
                    course_code="MCV4U",
                    reason="Required for engineering programs"
                ),
                PlannedCourse(
                    course_name="Computer Science",
                    course_code="ICS4U",
                    reason="Interested in software engineering"
                ),
            ]
        ),
        extracurriculars=[
            Extracurricular(
                name="Robotics Club",
                leadership_level=4,
                role_title="Team Captain",
                impact_level=4,
                hours_per_week=8.0,
                months=24,
                notes="Led team to regional competition finals"
            ),
            Extracurricular(
                name="Math Tutoring",
                leadership_level=2,
                role_title="Volunteer Tutor",
                impact_level=3,
                hours_per_week=3.0,
                months=12,
                notes="Tutoring grade 9 and 10 students"
            ),
        ],
        interests=["programming", "robotics", "math", "physics"],
        pathway_preference=PathwayPreference(
            coop_importance=9,
            research_importance=6
        ),
        links=Links(
            github_url="https://github.com/alexchen"
        ),
        roadmap=Roadmap(
            school="McMaster University",
            program="Engineer",
            tasks=[
                Task(
                    content="Create OUAC Account - Register for Ontario Universities' Application Centre",
                    deadline="2025-10-15",
                    status="done"
                ),
                Task(
                    content="Submit OUAC Application - Complete and submit your OUAC application through OUAC",
                    deadline="2025-11-15",
                    status="done"
                ),
                Task(
                    content="Complete Supplementary Application - Submit the McMaster supplementary application",
                    deadline="2025-04-10",
                    status="done"
                ),
                Task(
                    content="CASPer Test - Take online CASPer situational judgment test",
                    deadline="2025-06-15",
                    status="in progress"
                ),
                Task(
                    content="Await Decision - Wait for admission decision",
                    deadline="2025-06-30",
                    status="to do"
                ),
            ],
            progress=60,
            deadline="2025-01-15",
            done=[0, 1, 2],
            toDo=[4],
            inProgress=[3]
        )
    )


def main():
    """Main test function"""
    print("=" * 60)
    print("Gemini Consultant - Terminal Test")
    print("=" * 60)
    print()
    
    # Initialize consultant
    try:
        consultant = Consultant()
        print("✓ Consultant initialized successfully")
    except ConsultantError as e:
        print(f"✗ Failed to initialize consultant: {e}")
        print("\nMake sure to set GEMINI_API_KEY environment variable:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        return
    
    # Create sample user
    user = create_sample_user()
    consultant.set_user_profile(user)
    print(f"✓ User profile loaded: {user.name}")
    print()
    
    # Interactive chat loop
    print("You can now chat with the consultant!")
    print("Commands:")
    print("  - Type your question and press Enter")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'quit' or 'exit' to end the session")
    print()
    
    while True:
        try:
            # Get user input
            question = input("You: ").strip()
            
            if not question:
                continue
            
            # Handle commands
            if question.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
            
            if question.lower() == 'clear':
                consultant.clear_history()
                print("✓ Conversation history cleared\n")
                continue
            
            # Get response from consultant
            print("\nConsultant: ", end="", flush=True)
            response = consultant.ask(question)
            print(response)
            print()
        
        except ConsultantError as e:
            print(f"\n✗ Error: {e}\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
