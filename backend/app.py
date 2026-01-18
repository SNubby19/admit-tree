from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Constants
INTEREST_OPTIONS = [
    "Computer Science",
    "Software Engineering",
    "Civil Engineering",
    "Business",
    "Psychology"
]

SUBJECT_OPTIONS = [
    "Math",
    "Physics",
    "Chemistry",
    "Biology",
    "English"
]

CITIZENSHIP_OPTIONS = [
    "Canadian",
    "Permanent Resident",
    "International"
]

def validate_intake_data(data):
    """Validate the intake form data and return (is_valid, errors)"""
    errors = []
    
    if not data or "student_profile" not in data:
        return False, ["Missing 'student_profile' in request body"]
    
    profile = data["student_profile"]
    
    # Validate current_grade (required string)
    if "current_grade" not in profile:
        errors.append("'current_grade' is required")
    elif not isinstance(profile["current_grade"], str):
        errors.append("'current_grade' must be a string")
    elif not profile["current_grade"].strip():
        errors.append("'current_grade' cannot be empty")
    
    # Validate gpa_average (required integer)
    if "gpa_average" not in profile:
        errors.append("'gpa_average' is required")
    elif not isinstance(profile["gpa_average"], int):
        errors.append("'gpa_average' must be an integer")
    elif profile["gpa_average"] < 0 or profile["gpa_average"] > 100:
        errors.append("'gpa_average' must be between 0 and 100")
    
    # Validate major_interests (required list, each item must be from INTEREST_OPTIONS enum)
    if "major_interests" not in profile:
        errors.append("'major_interests' is required")
    elif not isinstance(profile["major_interests"], list):
        errors.append("'major_interests' must be a list")
    elif len(profile["major_interests"]) == 0:
        errors.append("'major_interests' cannot be empty")
    elif not all(isinstance(item, str) for item in profile["major_interests"]):
        errors.append("'major_interests' must be a list of strings")
    else:
        invalid_interests = [i for i in profile["major_interests"] if i not in INTEREST_OPTIONS]
        if invalid_interests:
            errors.append(f"Invalid major_interests: {invalid_interests}. Must be one of: {INTEREST_OPTIONS}")
    
    # Validate strongest_subjects (required list, each item must be from SUBJECT_OPTIONS enum)
    if "strongest_subjects" not in profile:
        errors.append("'strongest_subjects' is required")
    elif not isinstance(profile["strongest_subjects"], list):
        errors.append("'strongest_subjects' must be a list")
    elif len(profile["strongest_subjects"]) == 0:
        errors.append("'strongest_subjects' cannot be empty")
    elif not all(isinstance(item, str) for item in profile["strongest_subjects"]):
        errors.append("'strongest_subjects' must be a list of strings")
    else:
        invalid_subjects = [s for s in profile["strongest_subjects"] if s not in SUBJECT_OPTIONS]
        if invalid_subjects:
            errors.append(f"Invalid strongest_subjects: {invalid_subjects}. Must be one of: {SUBJECT_OPTIONS}")
    
    # Validate subjects_taken (required list, each item must be from SUBJECT_OPTIONS enum)
    # This is used for prerequisite checking for university programs
    if "subjects_taken" not in profile:
        errors.append("'subjects_taken' is required")
    elif not isinstance(profile["subjects_taken"], list):
        errors.append("'subjects_taken' must be a list")
    elif len(profile["subjects_taken"]) == 0:
        errors.append("'subjects_taken' cannot be empty")
    elif not all(isinstance(item, str) for item in profile["subjects_taken"]):
        errors.append("'subjects_taken' must be a list of strings")
    else:
        invalid_subjects = [s for s in profile["subjects_taken"] if s not in SUBJECT_OPTIONS]
        if invalid_subjects:
            errors.append(f"Invalid subjects_taken: {invalid_subjects}. Must be one of: {SUBJECT_OPTIONS}")
    
    # Validate citizenship (required, must be from CITIZENSHIP_OPTIONS enum)
    if "citizenship" not in profile:
        errors.append("'citizenship' is required")
    elif not isinstance(profile["citizenship"], str):
        errors.append("'citizenship' must be a string")
    elif profile["citizenship"] not in CITIZENSHIP_OPTIONS:
        errors.append(f"Invalid citizenship: '{profile['citizenship']}'. Must be one of: {CITIZENSHIP_OPTIONS}")
    
    return len(errors) == 0, errors

@app.route("/")
def home():
    return "<p>Hello from Flask via uv!</p>"

@app.route("/api/submit-intake", methods=["POST"])
def submit_intake():
    try:
        data = request.get_json()
        
        # Validate the data
        is_valid, errors = validate_intake_data(data)
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": "Validation failed",
                "errors": errors
            }), 400
        
        # Parse the validated data into the expected structure
        profile = data["student_profile"]
        student_profile = {
            "current_grade": profile["current_grade"],
            "gpa_average": profile["gpa_average"],
            "major_interests": profile["major_interests"],
            "strongest_subjects": profile["strongest_subjects"],
            "subjects_taken": profile["subjects_taken"],
            "citizenship": profile["citizenship"]
        }
        
        # Print the received JSON to console for debugging
        print("Received JSON:")
        print(json.dumps({"student_profile": student_profile}, indent=2))
        
        return jsonify({
            "status": "success",
            "message": "Intake form submitted successfully",
            "data": {"student_profile": student_profile}
        }), 200
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == "__main__":
    app.run(port=5001, debug=True)
