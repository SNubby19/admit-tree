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
        "Software Engineering": {
            "recommended_average": [95, 99],
            "ec_quality": 3,
            "interest_fields": ["software", "programming", "algorithms", "systems"],
            "required_courses": ["MHF4U", "MCV4U", "SPH4U"],
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
        },
        "Electrical Engineering": {
            "recommended_average": [90, 96],
            "ec_quality": 3,
            "interest_fields": ["circuits", "electronics", "power", "signals"],
            "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"],
            "co-op": ["yes", "no"]
        }
    },
    "McMaster University": {
        "Computer Science": {
            "recommended_average": [85, 92],
            "ec_quality": 2,
            "interest_fields": ["software", "programming", "algorithms"],
            "required_courses": ["MHF4U"],
            "co-op": ["yes", "no"]
        },
        "Software Engineering": {
            "recommended_average": [87, 94],
            "ec_quality": 2,
            "interest_fields": ["software", "engineering", "systems"],
            "required_courses": ["MHF4U", "MCV4U", "SPH4U"],
            "co-op": ["yes"]
        },
        "Health Sciences": {
            "recommended_average": [90, 96],
            "ec_quality": 3,
            "interest_fields": ["health", "medicine", "biology", "research"],
            "required_courses": ["MHF4U", "SCH4U", "SPH4U"],
            "co-op": ["no"]
        }
    },
    "Queen's University": {
        "Computer Science": {
            "recommended_average": [83, 90],
            "ec_quality": 2,
            "interest_fields": ["software", "programming", "theory"],
            "required_courses": ["MHF4U"],
            "co-op": ["yes", "no"]
        },
        "Engineering": {
            "recommended_average": [85, 93],
            "ec_quality": 2,
            "interest_fields": ["engineering", "design", "problem-solving"],
            "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"],
            "co-op": ["yes"]
        }
    },
    "University of British Columbia": {
        "Computer Science": {
            "recommended_average": [92, 97],
            "ec_quality": 3,
            "interest_fields": ["software", "ai", "data", "systems"],
            "required_courses": ["MHF4U"],
            "co-op": ["yes", "no"]
        },
        "Engineering": {
            "recommended_average": [88, 95],
            "ec_quality": 3,
            "interest_fields": ["engineering", "design", "physics"],
            "required_courses": ["MHF4U", "MCV4U", "SPH4U", "SCH4U"],
            "co-op": ["yes"]
        }
    }
}

