"""
Terminal test script for the Gemini Consultant
"""

from consultant.geminiConsultant import GeminiConsultant, ConsultantError
from consultant.mockdata.user import (
    User, BelowGrade12, Extracurricular, PathwayPreference, Links,
    CourseWithGrade, PlannedCourse, Task, Roadmap, Program
)
import json


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
        )
        programs = [
            Program(
                school = "McMaster University",
                program = "civil engineer"
            ),
            Program(
                school = "York University",
                program = "civil engineer"
            ),
            Program(
                school = "University of Toronto",
                program = "civil engineer"
            )
        ]
        # roadmap=Roadmap(
        #     school="McMaster University",
        #     program="Engineer",
        #     tasks=[
        #         Task(
        #             content="Create OUAC Account - Register for Ontario Universities' Application Centre",
        #             deadline="2025-10-15",
        #             status="done"
        #         ),
        #         Task(
        #             content="Submit OUAC Application - Complete and submit your OUAC application through OUAC",
        #             deadline="2025-11-15",
        #             status="done"
        #         ),
        #         Task(
        #             content="Complete Supplementary Application - Submit the McMaster supplementary application",
        #             deadline="2025-04-10",
        #             status="done"
        #         ),
        #         Task(
        #             content="CASPer Test - Take online CASPer situational judgment test",
        #             deadline="2025-06-15",
        #             status="in progress"
        #         ),
        #         Task(
        #             content="Await Decision - Wait for admission decision",
        #             deadline="2025-06-30",
        #             status="to do"
        #         ),
        #     ],
        #     progress=60,
        #     deadline="2025-01-15",
        #     done=[0, 1, 2],
        #     toDo=[4],
        #     inProgress=[3]
        # )
        
    )


def test_generate_program_roadmap():
    """Test the generate_program_roadmap function with just a list of programs"""
    print("=" * 60)
    print("Testing generate_program_roadmap() Function (Gemini)")
    print("=" * 60)
    print()
    
    # Initialize consultant
    try:
        consultant = GeminiConsultant()
        print("✓ Gemini Consultant initialized successfully")
    except ConsultantError as e:
        print(f"✗ Failed to initialize consultant: {e}")
        return
    
    # Create program list
    from consultant.mockdata.user import Program
    programs = [
        Program(school="McMaster University", program="civil Engineer"),
        Program(school="University of Toronto", program="mechanical Engineer"),
        Program(school="University of Waterloo", program="Mechanical Engineer")
    ]
    
    print(f"✓ Programs to process: {len(programs)}")
    for prog in programs:
        print(f"  - {prog.school}: {prog.program}")
    print()
    
    # Generate roadmap
    print("Generating roadmap... (this may take a moment)")
    print()
    try:
        roadmap = consultant.generate_program_roadmap(programs)
        print("✓ Roadmap generated successfully!\n")
        
        # Display roadmap summary
        print(f"Admissions Cycle: {roadmap.get('admissionsCycle', 'N/A')}")
        print(f"Number of Schools: {len(roadmap.get('schools', []))}")
        print()
        
        # Display detailed roadmap
        print("=" * 60)
        print("DETAILED ROADMAP")
        print("=" * 60)
        print(json.dumps(roadmap, indent=2))
        print()
        
        # Display summary statistics
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for school in roadmap.get('schools', []):
            school_name = school.get('schoolName', 'Unknown')
            program_name = school.get('programName', '')
            tasks = school.get('tasks', [])
            
            print(f"\n{school_name}")
            if program_name:
                print(f"  Program: {program_name}")
            print(f"  Total Tasks: {len(tasks)}")
            
            # Count by priority
            priority_counts = {}
            type_counts = {}
            for task in tasks:
                priority = task.get('priority', 'Unknown')
                task_type = task.get('type', 'Unknown')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                type_counts[task_type] = type_counts.get(task_type, 0) + 1
            
            print(f"  By Priority: {dict(priority_counts)}")
            print(f"  By Type: {dict(type_counts)}")
        
        print("\n✓ Test completed successfully!")
        
    except ConsultantError as e:
        print(f"✗ Error generating roadmap: {e}")
        print("\nTip: Check that your GEMINI_API_KEY is correct in .env")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


def test_generate_roadmap():
    """Test the generate_roadmap function"""
    print("=" * 60)
    print("Testing generate_roadmap() Function (Gemini)")
    print("=" * 60)
    print()
    
    # Initialize consultant
    try:
        consultant = GeminiConsultant()
        print("✓ Gemini Consultant initialized successfully")
    except ConsultantError as e:
        print(f"✗ Failed to initialize consultant: {e}")
        return
    
    # Create sample user
    user = create_sample_user()
    consultant.set_user_profile(user)
    print(f"✓ User profile loaded: {user.name}")
    print(f"✓ Programs: {len(user.programs)} programs")
    for prog in user.programs:
        print(f"  - {prog.school}: {prog.program}")
    print()
    
    # Note: GeminiConsultant doesn't have generate_roadmap() method, using generate_program_roadmap instead
    print("Generating roadmap using program list... (this may take a moment)")
    print()
    try:
        roadmap = consultant.generate_program_roadmap(user.programs)
        print("✓ Roadmap generated successfully!\n")
        
        # Display roadmap summary
        print(f"Admissions Cycle: {roadmap.get('admissionsCycle', 'N/A')}")
        print(f"Number of Schools: {len(roadmap.get('schools', []))}")
        print()
        
        # Display detailed roadmap
        print("=" * 60)
        print("DETAILED ROADMAP")
        print("=" * 60)
        print(json.dumps(roadmap, indent=2))
        print()
        
        # Display summary statistics
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for school in roadmap.get('schools', []):
            school_name = school.get('schoolName', 'Unknown')
            program_name = school.get('programName', '')
            tasks = school.get('tasks', [])
            
            print(f"\n{school_name}")
            if program_name:
                print(f"  Program: {program_name}")
            print(f"  Total Tasks: {len(tasks)}")
            
            # Count by priority
            priority_counts = {}
            type_counts = {}
            for task in tasks:
                priority = task.get('priority', 'Unknown')
                task_type = task.get('type', 'Unknown')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                type_counts[task_type] = type_counts.get(task_type, 0) + 1
            
            print(f"  By Priority: {dict(priority_counts)}")
            print(f"  By Type: {dict(type_counts)}")
        
        print("\n✓ Test completed successfully!")
        
    except ConsultantError as e:
        print(f"✗ Error generating roadmap: {e}")
        print("\nTip: Check that your GEMINI_API_KEY is correct in .env")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function"""
    print("=" * 60)
    print("Gemini Consultant - Terminal Test")
    print("=" * 60)
    print()
    
    # Initialize consultant
    try:
        consultant = GeminiConsultant()
        print("✓ Gemini Consultant initialized successfully")
    except ConsultantError as e:
        print(f"✗ Failed to initialize consultant: {e}")
        print("\nMake sure to set GEMINI_API_KEY in .env file")
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
    print("  - Type 'roadmap' to generate a roadmap")
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
            
            if question.lower() == 'roadmap':
                print("\nGenerating roadmap... (this may take a moment)")
                try:
                    roadmap = consultant.generate_program_roadmap()
                    print("\n✓ Roadmap generated successfully!\n")
                    print(json.dumps(roadmap, indent=2))
                    print()
                except ConsultantError as e:
                    print(f"\n✗ Error: {e}\n")
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
    import sys
    
    # Check if user wants to run roadmap test
    if len(sys.argv) > 1:
        if sys.argv[1] == "roadmap":
            test_generate_roadmap()
        elif sys.argv[1] == "programs":
            test_generate_program_roadmap()
        else:
            print("Usage: python test_consultant.py [roadmap|programs]")
    else:
        main()
