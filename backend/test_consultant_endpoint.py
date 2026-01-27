"""
Test script for the consultant chat endpoint
"""
import requests
import json

# Test data
test_payload = {
    "message": "What should I focus on right now for my Waterloo Software Engineering application?",
    "intake_data": {
        "name": "Alex Chen",
        "email": "alex.chen@example.com",
        "grade": "Grade 11",
        "wants_coop": True,
        "extra_curriculars": [
            {"name": "Robotics Club", "leadership_level": 3},
            {"name": "Math Team", "leadership_level": 2}
        ],
        "interests": ["software development", "artificial intelligence", "robotics"],
        "courses_taken": [
            {"course": "MHF4U", "grade": 95},
            {"course": "MCV4U", "grade": 93},
            {"course": "SPH4U", "grade": 90}
        ]
    },
    "programs": [
        {
            "id": "program-1",
            "universityName": "University of Waterloo",
            "programName": "Software Engineering",
            "deadline": "2025-02-01",
            "steps": [
                {
                    "id": "step-1",
                    "title": "Complete OUAC Application",
                    "description": "Submit application through OUAC",
                    "status": "complete",
                    "dueDate": "2024-11-15",
                    "priority": "high"
                },
                {
                    "id": "step-2",
                    "title": "Complete AIF Form",
                    "description": "Submit Admission Information Form with experiences",
                    "status": "in-progress",
                    "dueDate": "2025-01-25",
                    "priority": "high"
                },
                {
                    "id": "step-3",
                    "title": "Euclid Math Contest",
                    "description": "Register and prepare for the Euclid Mathematics Contest",
                    "status": "todo",
                    "dueDate": "2025-04-08",
                    "priority": "medium"
                }
            ],
            "bonusTasks": [
                {
                    "id": "bonus-1",
                    "title": "Complete side project",
                    "description": "Build a portfolio project to showcase skills",
                    "status": "in-progress",
                    "category": "academic"
                }
            ],
            "overallProgress": 40
        },
        {
            "id": "program-2",
            "universityName": "University of Toronto",
            "programName": "Computer Science",
            "deadline": "2025-01-15",
            "steps": [
                {
                    "id": "step-1",
                    "title": "Complete OUAC Application",
                    "description": "Submit application through OUAC",
                    "status": "complete",
                    "dueDate": "2024-11-15",
                    "priority": "high"
                },
                {
                    "id": "step-2",
                    "title": "Submit Supplementary Application",
                    "description": "Complete the Engineering Student Profile",
                    "status": "todo",
                    "dueDate": "2025-01-10",
                    "priority": "high"
                }
            ],
            "bonusTasks": [],
            "overallProgress": 25
        }
    ]
}

def test_consultant_endpoint():
    """Test the consultant chat endpoint"""
    url = "http://localhost:5001/api/consultant/chat"
    
    print("="*80)
    print("TESTING CONSULTANT ENDPOINT")
    print("="*80)
    print(f"\nURL: {url}")
    print(f"\nStudent: {test_payload['intake_data']['name']}")
    print(f"Programs: {len(test_payload['programs'])}")
    print(f"Question: {test_payload['message']}")
    print("\n" + "="*80)
    
    try:
        print("\nSending request...")
        response = requests.post(url, json=test_payload, timeout=30)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "="*80)
            print("CONSULTANT RESPONSE:")
            print("="*80)
            print(result.get('response', 'No response'))
            print("="*80)
            print("\n✓ Test PASSED!")
        else:
            print("\n" + "="*80)
            print("ERROR RESPONSE:")
            print("="*80)
            print(json.dumps(response.json(), indent=2))
            print("="*80)
            print("\n✗ Test FAILED!")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to backend.")
        print("   Make sure Flask is running: python app.py")
    except requests.exceptions.Timeout:
        print("\n✗ ERROR: Request timed out after 30 seconds")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_consultant_endpoint()
