import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.matcher import UniversityMatcher
from agentPrograms import get_program_recommendations, AgentProgramsError
from agentRoadmap import generate_roadmaps, AgentRoadmapError
from consultant.consultant import ask_consultant, ConsultantError

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure CORS from environment variables
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:8080,http://localhost:3000").split(",")
CORS(app, origins=cors_origins)

@app.route("/")
def home():
    return "<p>Hello from Flask via uv!</p>"


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    POST endpoint to get ranked university program recommendations using DigitalOcean Agent.
    
    Expected JSON payload:
    {
        "grade_level": int,
        "average": float,
        "wants_coop": bool,
        "extra_curriculars": [("name", level), ...],
        "major_interests": ["interest1", "interest2", ...],
        "courses_taken": [("course_code", grade), ...]
    }
    """
    try:
        # Get JSON payload
        student_profile = request.get_json()
        
        print(f"Received student profile: {student_profile}")
        
        # Validate required fields
        required_fields = ['grade_level', 'average', 'wants_coop', 'extra_curriculars', 
                          'major_interests', 'courses_taken']
        missing_fields = [field for field in required_fields if field not in student_profile]
        
        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing": missing_fields
            }), 400
        
    #      # Instantiate matcher and get rankings
    #     matcher = UniversityMatcher(student_profile)
    #     rankings = matcher.get_ranked_programs()
        
    #     return jsonify({
    #         "success": True,
    #         "rankings": rankings,
    #         "total_programs": len(rankings)
    #     }), 200
        
    # except Exception as e:
    #     return jsonify({
    #         "error": "Internal server error",
    #         "message": str(e)
    #     }), 500
        
        # Call the DigitalOcean Agent to get recommendations
        print("Calling agent...")
        rankings = get_program_recommendations(student_profile)
        
        # Print agent response to console
        print("\n" + "="*80)
        print("AGENT RESPONSE (Rankings):")
        print("="*80)
        print(json.dumps(rankings, indent=2))
        print("="*80 + "\n")
        
        return jsonify({
            "success": True,
            "rankings": rankings,
            "total_programs": len(rankings)
        }), 200
        
    except AgentProgramsError as e:
        print(f"Agent error: {e}")
        return jsonify({
            "error": "Agent error",
            "message": str(e)
        }), 500
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route("/api/generate-roadmap", methods=["POST"])
def generate_roadmap():
    """
    POST endpoint to generate personalized roadmaps for selected programs.
    
    Expected JSON payload:
    {
        "student_profile": {
            "grade_level": int,
            "average": float,
            "wants_coop": bool,
            "extra_curriculars": [[name, level], ...],
            "major_interests": ["interest1", ...],
            "courses_taken": [[code, grade], ...]
        },
        "selected_programs": [
            {"university": "University Name", "program": "Program Name"},
            ...
        ]
    }
    """
    try:
        # Get JSON payload
        data = request.get_json()
        
        print(f"Received roadmap request: {json.dumps(data, indent=2)}")
        
        # Validate required fields
        if not data or 'student_profile' not in data or 'selected_programs' not in data:
            return jsonify({
                "error": "Missing required fields: student_profile and selected_programs"
            }), 400
        
        student_profile = data['student_profile']
        selected_programs = data['selected_programs']
        
        if not isinstance(selected_programs, list) or len(selected_programs) == 0:
            return jsonify({
                "error": "selected_programs must be a non-empty list"
            }), 400
        
        # Call the DigitalOcean Agent to generate roadmaps
        print("Calling roadmap agent...")
        university_programs = generate_roadmaps(student_profile, selected_programs)
        
        # Print roadmap response to console
        print("\n" + "="*80)
        print("ROADMAP AGENT RESPONSE:")
        print("="*80)
        print(json.dumps(university_programs, indent=2))
        print("="*80 + "\n")
        
        return jsonify({
            "success": True,
            "programs": university_programs
        }), 200
        
    except AgentRoadmapError as e:
        print(f"Roadmap agent error: {e}")
        return jsonify({
            "error": "Roadmap agent error",
            "message": str(e)
        }), 500
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route("/api/consultant/chat", methods=["POST"])
def consultant_chat():
    """
    POST endpoint for consultant chatbot that receives user context with each message.
    
    Expected JSON payload:
    {
        "message": "User's question",
        "intake_data": {
            "name": "Student Name",
            "email": "email@example.com",
            "grade": "Grade 11",
            "wants_coop": true,
            "extra_curriculars": [...],
            "interests": [...],
            "courses_taken": [...]
        },
        "programs": [
            {
                "id": "program-1",
                "universityName": "University Name",
                "programName": "Program Name",
                "deadline": "2025-01-15",
                "steps": [...],
                "bonusTasks": [...],
                "overallProgress": 50
            },
            ...
        ]
    }
    """
    try:
        # Get JSON payload
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing required field: message"
            }), 400
        
        message = data['message']
        intake_data = data.get('intake_data')
        programs = data.get('programs')
        
        print(f"\n{'='*80}")
        print(f"CONSULTANT CHAT REQUEST")
        print(f"{'='*80}")
        print(f"Message: {message}")
        print(f"Has intake data: {bool(intake_data)}")
        print(f"Number of programs: {len(programs) if programs else 0}")
        print(f"{'='*80}\n")
        
        # Call consultant function with all context
        response = ask_consultant(
            message=message,
            intake_data=intake_data,
            programs=programs
        )
        
        print(f"\n{'='*80}")
        print(f"CONSULTANT RESPONSE")
        print(f"{'='*80}")
        print(response)
        print(f"{'='*80}\n")
        
        return jsonify({
            "success": True,
            "response": response
        }), 200
        
    except ConsultantError as e:
        print(f"Consultant error: {e}")
        return jsonify({
            "error": "Consultant error",
            "message": str(e)
        }), 500
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5001))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host=host, port=port, debug=debug)
