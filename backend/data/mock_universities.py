"""
Mock university database for testing the scoring engine.
Structure: University -> Program -> Details
"""

UNIVERSITY_DB = {
    "University of Waterloo": {
        "Computer Engineering": {
            "recommended_average": [92, 98],
            "ec_quality": 3,
            "interest_fields": ["circuits", "hardware", "physics", "robotics"],
            "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"],
            "co-op": ["yes"]  # Only Co-op available
        },
        "Arts and Business": {
            "recommended_average": [82, 88],
            "ec_quality": 2,
            "interest_fields": ["business", "culture", "writing", "management"],
            "required_courses": [],
            "co-op": ["yes", "no"]  # Both streams available
        }
    },
    "University of Toronto": {
        "Computer Science": {
            "recommended_average": [94, 99],
            "ec_quality": 3,
            "interest_fields": ["software", "theory", "math", "ai", "data"],
            "required_courses": ["MHF4U"],
            "co-op": ["yes", "no"]  # ASIP (Co-op) and Regular available
        },
        "Mechanical Engineering": {
            "recommended_average": [88, 95],
            "ec_quality": 3,
            "interest_fields": ["machines", "structures", "physics", "cars"],
            "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"],
            "co-op": ["yes"]  # PEY (Co-op) is effectively standard
        }
    }
}

