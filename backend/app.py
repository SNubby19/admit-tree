import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.matcher import UniversityMatcher
from agentPrograms import get_program_recommendations, AgentProgramsError

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


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5001))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host=host, port=port, debug=debug)
