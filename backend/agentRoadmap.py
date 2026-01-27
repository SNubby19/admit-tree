"""
Agent Roadmap module - Calls DigitalOcean Agent to generate personalized roadmaps.
"""
import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

AGENT_ENDPOINT = os.getenv("AGENT_ROADMAP_ENDPOINT")
AGENT_ACCESS_KEY = os.getenv("AGENT_ROADMAP_ACCESS_KEY")


class AgentRoadmapError(Exception):
    """Custom exception for agent roadmap errors"""
    pass


def format_roadmap_prompt(student_profile: Dict[str, Any], selected_programs: List[Dict[str, str]]) -> str:
    """
    Format student profile and selected programs into a prompt for the roadmap agent.
    
    Args:
        student_profile: Dictionary with student information
        selected_programs: List of dicts with 'university' and 'program' keys
    
    Returns:
        Formatted prompt string
    """
    # Format extracurriculars
    ec_text = ""
    if student_profile.get('extra_curriculars'):
        ec_list = []
        for ec in student_profile['extra_curriculars']:
            if isinstance(ec, list) and len(ec) >= 2:
                name, level = ec[0], ec[1]
                ec_list.append(f"  - {name} (Leadership Level: {level})")
        if ec_list:
            ec_text = "\nExtracurriculars:\n" + "\n".join(ec_list)
    
    # Format courses
    courses_text = ""
    if student_profile.get('courses_taken'):
        courses_list = []
        for course in student_profile['courses_taken']:
            if isinstance(course, list) and len(course) >= 2:
                code, grade = course[0], course[1]
                courses_list.append(f"  - {code}: {grade}%")
        if courses_list:
            courses_text = "\nCourses Taken:\n" + "\n".join(courses_list)
    
    # Format interests
    interests_text = ""
    if student_profile.get('major_interests'):
        interests_text = f"\nInterests: {', '.join(student_profile['major_interests'])}"
    
    # Format selected programs
    programs_text = "\n".join([
        f"  - {prog['university']}: {prog['program']}"
        for prog in selected_programs
    ])
    
    prompt = f"""Student Profile:
Grade Level: {student_profile.get('grade_level', 'N/A')}
Current Average: {student_profile.get('average', 'N/A')}%
Wants Co-op: {'Yes' if student_profile.get('wants_coop') else 'No'}{ec_text}{interests_text}{courses_text}

Selected Programs:
{programs_text}

Generate a personalized roadmap for each selected program. Use your knowledge base to determine requirements, deadlines, and create actionable tasks.

CRITICAL: Output ONLY valid JSON in this EXACT format with NO markdown, NO code fences, NO explanations:

{{
  "roadmaps": [
    {{
      "school": "University Name",
      "program": "Program Name",
      "tasks": [
        {{
          "content": "Actionable task description starting with a verb",
          "deadline": "YYYY-MM-DD or empty string if unknown",
          "status": "to do"
        }}
      ],
      "progress": 0,
      "deadline": "YYYY-MM-DD or empty string",
      "done": [],
      "toDo": [0, 1, 2],
      "inProgress": []
    }}
  ]
}}

Requirements:
- Generate 8-16 tasks per program
- Tasks must be specific and actionable
- Use ISO date format (YYYY-MM-DD) or empty string for deadlines
- Include tasks for: prerequisites, OUAC application, supplementary materials, extracurriculars, co-op prep (if wanted)
- Order tasks chronologically
- done/toDo/inProgress are 0-based indices into tasks array
- All tasks start as "to do" with progress=0

OUTPUT ONLY THE JSON OBJECT. NO OTHER TEXT."""
    
    return prompt


def generate_roadmaps(student_profile: Dict[str, Any], selected_programs: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Call the DigitalOcean Agent to generate roadmaps for selected programs.
    
    Args:
        student_profile: Dictionary with student information
        selected_programs: List of dicts with 'university' and 'program' keys
    
    Returns:
        List of roadmap dictionaries in UniversityProgram format
    
    Raises:
        AgentRoadmapError: If the agent call fails
    """
    if not AGENT_ENDPOINT or not AGENT_ACCESS_KEY:
        raise AgentRoadmapError("AGENT_ROADMAP_ENDPOINT or AGENT_ROADMAP_ACCESS_KEY not configured in .env")
    
    if not selected_programs:
        raise AgentRoadmapError("No programs selected")
    
    # Format the prompt
    prompt = format_roadmap_prompt(student_profile, selected_programs)
    
    # Prepare the request
    headers = {
        "Authorization": f"Bearer {AGENT_ACCESS_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build messages array
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    payload = {
        "messages": messages,
        "stream": False,
        "include_functions_info": True,
        "include_retrieval_info": True,
        "include_guardrails_info": False
    }
    
    try:
        # Ensure endpoint ends with /api/v1/chat/completions
        endpoint = AGENT_ENDPOINT.rstrip('/')
        if not endpoint.endswith('/api/v1/chat/completions'):
            endpoint = endpoint + '/api/v1/chat/completions'
        
        response = requests.post(endpoint, json=payload, headers=headers, timeout=90)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract the message content
        if not result.get("choices"):
            raise AgentRoadmapError(f"No response from agent. Full response: {result}")
        
        message = result["choices"][0]["message"]
        answer = message.get("content", "")
        
        # If content is empty, check reasoning_content
        if not answer or not answer.strip():
            answer = message.get("reasoning_content", "")
        
        # Debug: print raw response
        print(f"Roadmap agent response (content): {answer[:200] if answer else 'EMPTY'}...")
        
        if not answer or not answer.strip():
            raise AgentRoadmapError(f"Agent returned empty response")
        
        # Parse the JSON response
        try:
            # Remove markdown code fences if present
            if "```json" in answer:
                start = answer.find("```json") + 7
                end = answer.find("```", start)
                answer = answer[start:end].strip()
            elif "```" in answer:
                start = answer.find("```") + 3
                end = answer.find("```", start)
                answer = answer[start:end].strip()
            
            # Find JSON object in the response
            start_idx = answer.find("{")
            end_idx = answer.rfind("}")
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                answer = answer[start_idx:end_idx+1]
            else:
                raise AgentRoadmapError(f"No JSON object found in response")
            
            roadmap_data = json.loads(answer)
            
            if not isinstance(roadmap_data, dict) or "roadmaps" not in roadmap_data:
                raise AgentRoadmapError(f"Expected JSON with 'roadmaps' key, got {type(roadmap_data)}")
            
            roadmaps = roadmap_data["roadmaps"]
            
            if not isinstance(roadmaps, list):
                raise AgentRoadmapError(f"Expected 'roadmaps' to be a list, got {type(roadmaps)}")
            
            # Transform to UniversityProgram format
            university_programs = []
            for i, roadmap in enumerate(roadmaps):
                # Convert tasks to ApplicationStep format
                steps = []
                for j, task in enumerate(roadmap.get("tasks", [])):
                    # Map status: "to do" -> "todo", "in progress" -> "in-progress"
                    status = task.get("status", "to do")
                    if status == "to do":
                        status = "todo"
                    elif status == "in progress":
                        status = "in-progress"
                    
                    # Determine priority based on deadline or task content
                    priority = "medium"
                    content_lower = task.get("content", "").lower()
                    if "missing" in content_lower or "required" in content_lower or "prerequisite" in content_lower:
                        priority = "high"
                    elif "optional" in content_lower or "bonus" in content_lower:
                        priority = "low"
                    
                    step = {
                        "id": f"step-{i}-{j}",
                        "title": task.get("content", ""),
                        "description": task.get("content", ""),
                        "status": status,
                        "dueDate": task.get("deadline", "") if task.get("deadline") else None,
                        "priority": priority
                    }
                    steps.append(step)
                
                # Convert bonus tasks to BonusTask format
                bonus_tasks = []
                for k, bonus in enumerate(roadmap.get("bonusTasks", [])):
                    category = bonus.get("category", "academic")
                    # Validate category
                    if category not in ["extracurricular", "academic", "leadership", "community"]:
                        category = "academic"
                    
                    bonus_task = {
                        "id": f"bonus-{i}-{k}",
                        "title": bonus.get("content", ""),
                        "description": bonus.get("content", ""),
                        "status": "todo",
                        "category": category
                    }
                    bonus_tasks.append(bonus_task)
                
                # Calculate progress
                progress = roadmap.get("progress", 0)
                
                program = {
                    "id": f"program-{i+1}",
                    "universityName": roadmap.get("school", ""),
                    "programName": roadmap.get("program", ""),
                    "deadline": roadmap.get("deadline", ""),
                    "steps": steps,
                    "bonusTasks": bonus_tasks,
                    "overallProgress": progress
                }
                university_programs.append(program)
            
            return university_programs
            
        except json.JSONDecodeError as e:
            raise AgentRoadmapError(f"Failed to parse agent JSON response: {str(e)}. Response preview: {answer[:500] if answer else 'empty'}")
        
    except requests.exceptions.Timeout:
        raise AgentRoadmapError("Agent request timed out (60s)")
    except requests.exceptions.RequestException as e:
        raise AgentRoadmapError(f"Agent request failed: {str(e)}")
    except ValueError as e:
        raise AgentRoadmapError(f"Failed to parse agent response: {str(e)}")
