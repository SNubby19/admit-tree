"""
DigitalOcean Agent Consultant
A wrapper around DigitalOcean Agent API that provides personalized academic consulting.
"""

import os
import json
import requests
from typing import List, Dict, Optional
from pathlib import Path
from consultant.mockdata.user import User, Grade12OrAbove, BelowGrade12


def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


class ConsultantError(Exception):
    """Base exception for consultant errors"""
    pass


class Consultant:
    """
    AI-powered consultant that provides personalized academic guidance using DigitalOcean Agent.
    """
    
    def __init__(self):
        """
        Initialize the consultant with DigitalOcean Agent credentials.
        
        Raises:
            ConsultantError: If credentials are missing or invalid
        """
        # Load .env file
        load_env()
        
        self.agent_endpoint = os.getenv("AGENT_ENDPOINT")
        self.agent_access_key = os.getenv("AGENT_ACCESS_KEY")
        
        if not self.agent_endpoint or not self.agent_access_key:
            raise ConsultantError("AGENT_ENDPOINT and AGENT_ACCESS_KEY are required in .env file")
        
        # Ensure endpoint has the correct format
        if not self.agent_endpoint.endswith('/api/v1/chat/completions'):
            if self.agent_endpoint.endswith('/'):
                self.agent_endpoint = self.agent_endpoint + 'api/v1/chat/completions'
            else:
                self.agent_endpoint = self.agent_endpoint + '/api/v1/chat/completions'
        
        self.conversation_history: List[Dict[str, str]] = []
        self.user_profile: User = None
    
    def set_user_profile(self, user: User):
        """
        Set the user profile for personalized responses.
        
        Args:
            user: User object containing academic and extracurricular data
        """
        self.user_profile = user
    
    def _format_user_context(self) -> str:
        """
        Format user profile data into a structured context string.
        
        Returns:
            Formatted context string describing the user's profile
        """
        if not self.user_profile:
            return ""
        
        user = self.user_profile
        context_parts = [
            f"Student Profile:",
            f"Name: {user.name}",
            f"Email: {user.email}",
            "",
            "Academic Information:"
        ]
        
        # Format academic info based on grade level
        if isinstance(user.academic, Grade12OrAbove):
            context_parts.append(f"- Grade Level: 12 or above")
            context_parts.append(f"- GPA/Average: {user.academic.gpa_or_average}")
            context_parts.append(f"- Courses Taken:")
            for course in user.academic.courses_taken:
                grade_str = f" (Grade: {course.grade})" if course.grade else ""
                code_str = f" [{course.course_code}]" if course.course_code else ""
                context_parts.append(f"  * {course.course_name}{code_str}{grade_str}")
        
        elif isinstance(user.academic, BelowGrade12):
            context_parts.append(f"- Grade Level: {user.academic.grade_level}")
            if user.academic.current_average:
                context_parts.append(f"- Current Average: {user.academic.current_average}")
            
            context_parts.append(f"- Courses Completed:")
            for course in user.academic.courses_so_far:
                grade_str = f" (Grade: {course.grade})" if course.grade else ""
                code_str = f" [{course.course_code}]" if course.course_code else ""
                context_parts.append(f"  * {course.course_name}{code_str}{grade_str}")
            
            if user.academic.planned_courses:
                context_parts.append(f"- Planned Courses:")
                for course in user.academic.planned_courses:
                    code_str = f" [{course.course_code}]" if course.course_code else ""
                    reason_str = f" - {course.reason}" if course.reason else ""
                    context_parts.append(f"  * {course.course_name}{code_str}{reason_str}")
        
                
        # Format extracurriculars
        if user.extracurriculars:
            context_parts.append("")
            context_parts.append("Extracurricular Activities:")
            for activity in user.extracurriculars:
                role_str = f" - {activity.role_title}" if activity.role_title else ""
                context_parts.append(f"- {activity.name}{role_str}")
                context_parts.append(f"  * Leadership Level: {activity.leadership_level}/5")
                if activity.impact_level:
                    context_parts.append(f"  * Impact Level: {activity.impact_level}/5")
                if activity.hours_per_week:
                    context_parts.append(f"  * Time Commitment: {activity.hours_per_week} hours/week")
                if activity.months:
                    context_parts.append(f"  * Duration: {activity.months} months")
                if activity.notes:
                    context_parts.append(f"  * Notes: {activity.notes}")
        
        # Format interests
        if user.interests:
            context_parts.append("")
            context_parts.append(f"Interests: {', '.join(user.interests)}")
        
        # Format pathway preferences
        context_parts.append("")
        context_parts.append("Pathway Preferences:")
        context_parts.append(f"- Co-op Importance: {user.pathway_preference.coop_importance}/10")
        context_parts.append(f"- Research Importance: {user.pathway_preference.research_importance}/10")
        
        
        # Format links if available
        if user.links.resume_url or user.links.linkedin_url or user.links.github_url:
            context_parts.append("")
            context_parts.append("Additional Links:")
            if user.links.resume_url:
                context_parts.append(f"- Resume: {user.links.resume_url}")
            if user.links.linkedin_url:
                context_parts.append(f"- LinkedIn: {user.links.linkedin_url}")
            if user.links.github_url:
                context_parts.append(f"- GitHub: {user.links.github_url}")
        
        # Format programs
        if user.programs:
            context_parts.append("")
            context_parts.append("Chosen Programs:")
            for program in user.programs:
                context_parts.append(f"- {program.school}: {program.program}")

        # Format roadmap if available
        if user.roadmap and user.roadmap.tasks:
            context_parts.append("")
            context_parts.append(f"Application Roadmap ({user.roadmap.school} - {user.roadmap.program}):")
            context_parts.append(f"- Progress: {user.roadmap.progress}% complete")
            context_parts.append(f"- Application Deadline: {user.roadmap.deadline}")
            context_parts.append("- Tasks:")
            for i, task in enumerate(user.roadmap.tasks):
                status_emoji = "✓" if task.status == "done" else "→" if task.status == "in progress" else "○"
                context_parts.append(f"  {i+1}. [{status_emoji}] {task.content}")
                context_parts.append(f"     Deadline: {task.deadline} | Status: {task.status}")
        
        return "\n".join(context_parts)
    
    def ask(self, question: str) -> str:
        """
        Ask the consultant a question and get a personalized response.
        
        Args:
            question: User's question or message
        
        Returns:
            Consultant's response from DigitalOcean Agent
        
        Raises:
            ConsultantError: If API call fails or other errors occur
        """
        if not question or not question.strip():
            raise ConsultantError("Question cannot be empty")
        
        try:
            # Build messages array
            messages = []
            
            # Add user profile context as system message
            user_context = self._format_user_context()
            if user_context:
                system_message = f"Here is the student's profile:\n\n{user_context}\n\nProvide personalized advice based on this profile."
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            # Add conversation history
            for msg in self.conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Add current question
            messages.append({
                "role": "user",
                "content": question
            })
            
            # Prepare request payload
            payload = {
                "messages": messages,
                "stream": False,
                "include_functions_info": True,
                "include_retrieval_info": True,
                "include_guardrails_info": False
            }
            
            # Set headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.agent_access_key}"
            }
            
            # Call DigitalOcean Agent API
            response = requests.post(
                self.agent_endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # Check for errors
            if response.status_code != 200:
                raise ConsultantError(f"Agent API returned status {response.status_code}: {response.text}")
            
            # Parse response
            response_data = response.json()
            
            if not response_data.get("choices"):
                raise ConsultantError("No response from agent")
            
            answer = response_data["choices"][0]["message"]["content"]
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            return answer
        
        except requests.exceptions.Timeout:
            raise ConsultantError("Request to agent timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise ConsultantError(f"Failed to connect to agent: {str(e)}")
        except Exception as e:
            raise ConsultantError(f"Failed to generate response: {str(e)}")
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
#     def generate_program_roadmap(self, programs: List) -> Dict:
#         """
#         Generate a roadmap for a list of programs without requiring a full user profile.
        
#         Args:
#             programs: List of Program objects with school and program fields
        
#         Returns:
#             Dictionary containing the admissions cycle and schools with their tasks
        
#         Raises:
#             ConsultantError: If programs list is empty or API call fails
#         """
#         if not programs:
#             raise ConsultantError("Programs list cannot be empty")
        
#         # Format programs for the prompt
#         programs_text = "\n".join([f"- {p.school}: {p.program}" for p in programs])
        
#         prompt = f"""I am building a tool that helps students itemize tasks and build a timeline for their university admissions process applying to engineering programs in Ontario. What I need help with from you is after a student selects programs of interest, I need your help in breaking the application process for each program down into atomic steps and then I need you to generate a json of these various tasks sorted by program and school.

# The student has selected the following programs:
# {programs_text}

# YOU MUST OUTPUT ONLY VALID JSON. Do not include any explanations, reasoning, or additional text.

# Generate a roadmap in this EXACT JSON format:
# {{
#   "admissionsCycle": "2025-2026",
#   "schools": [
#     {{
#       "schoolName": "General (OUAC)",
#       "schoolCode": "OUAC",
#       "tasks": [
#         {{
#           "taskId": "ouac-001",
#           "title": "Create OUAC Account",
#           "description": "Create your account on the Ontario Universities' Application Centre (OUAC) website.",
#           "deadlineISO": "2025-11-01",
#           "priority": "High",
#           "type": "Administrative"
#         }}
#       ]
#     }},
#     {{
#       "schoolName": "University Name",
#       "schoolCode": "CODE",
#       "programName": "Program Name",
#       "tasks": [
#         {{
#           "taskId": "unique-id",
#           "title": "Task Title",
#           "description": "Detailed description",
#           "deadlineISO": "YYYY-MM-DD",
#           "priority": "Critical|High|Medium|Low",
#           "type": "Administrative|Supplementary|Interview|Submission|Financial|Milestone"
#         }}
#       ]
#     }}
#   ]
# }}

# REQUIREMENTS:
# 1. Always include a "General (OUAC)" school entry with common OUAC tasks (create account, submit application, etc.)
# 2. Include a separate entry for each university the student selected
# 3. Break down each application into atomic, actionable steps
# 4. Use realistic deadlines: OUAC deadline Jan 15 2026, McMaster supp Jan 29 2026, Waterloo AIF Jan 30 2026, UofT OSP Jan 15 2026, York Boost Mar 20 2026
# 5. Task types: Administrative (account setup), Supplementary (essays, forms), Interview, Submission, Financial (scholarships), Milestone
# 6. Priority levels: Critical (must-do), High (important), Medium (recommended), Low (optional)
# 7. Use unique taskIds like "ouac-001", "uw-002", "uoft-003", "mac-004", "york-005"
# 8. Order tasks chronologically within each school

# OUTPUT ONLY THE JSON OBJECT. NO OTHER TEXT."""

#         try:
#             # Build messages for the API call
#             messages = [
#                 {
#                     "role": "system",
#                     "content": "You are an expert university admissions consultant for Ontario engineering programs. You MUST output ONLY valid JSON with no additional text, explanations, or reasoning. Your entire response must be parseable JSON."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
            
#             # Prepare request payload
#             payload = {
#                 "messages": messages,
#                 "stream": False,
#                 "include_functions_info": True,
#                 "include_retrieval_info": True,
#                 "include_guardrails_info": False
#             }
            
#             # Set headers
#             headers = {
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {self.agent_access_key}"
#             }
            
#             # Call DigitalOcean Agent API
#             response = requests.post(
#                 self.agent_endpoint,
#                 json=payload,
#                 headers=headers,
#                 timeout=60
#             )
            
#             # Check for errors
#             if response.status_code != 200:
#                 raise ConsultantError(f"Agent API returned status {response.status_code}: {response.text}")
            
#             # Parse response
#             response_data = response.json()
            
#             if not response_data.get("choices"):
#                 raise ConsultantError(f"No response from agent. Full response: {response_data}")
            
#             # Try to get content from either content or reasoning_content
#             message = response_data["choices"][0]["message"]
#             roadmap_text = message.get("content", "")
            
#             # If content is empty, check reasoning_content (some models put output there)
#             if not roadmap_text or not roadmap_text.strip():
#                 roadmap_text = message.get("reasoning_content", "")
            
#             # Debug: Print the raw response
#             if not roadmap_text or not roadmap_text.strip():
#                 raise ConsultantError(f"Agent returned empty response. Full API response: {json.dumps(response_data, indent=2)}")
            
#             # Extract JSON from markdown code blocks if present
#             original_text = roadmap_text
#             if "```json" in roadmap_text:
#                 start = roadmap_text.find("```json") + 7
#                 end = roadmap_text.find("```", start)
#                 roadmap_text = roadmap_text[start:end].strip()
#             elif "```" in roadmap_text:
#                 start = roadmap_text.find("```") + 3
#                 end = roadmap_text.find("```", start)
#                 roadmap_text = roadmap_text[start:end].strip()
            
#             # Try to find JSON object in the text
#             if not roadmap_text.strip().startswith("{"):
#                 # Look for the first { and last }
#                 start_idx = original_text.find("{")
#                 end_idx = original_text.rfind("}")
#                 if start_idx != -1 and end_idx != -1:
#                     roadmap_text = original_text[start_idx:end_idx+1]
#                 else:
#                     raise ConsultantError(f"No JSON object found in response. Response preview: {original_text[:500]}")
            
#             roadmap_data = json.loads(roadmap_text)
            
#             return roadmap_data
        
#         except json.JSONDecodeError as e:
#             raise ConsultantError(f"Failed to parse roadmap JSON: {str(e)}. Response preview: {roadmap_text[:500] if roadmap_text else 'empty'}")
#         except requests.exceptions.Timeout:
#             raise ConsultantError("Request to agent timed out. Please try again.")
#         except requests.exceptions.RequestException as e:
#             raise ConsultantError(f"Failed to connect to agent: {str(e)}")
#         except Exception as e:
#             raise ConsultantError(f"Failed to generate roadmap: {str(e)}")
    
#     def generate_roadmap(self) -> Dict:
#         """
#         Generate a comprehensive roadmap with timeline for each program in the user's context.
#         Breaks down the application process for each program into atomic steps.
        
#         Returns:
#             Dictionary containing the admissions cycle and schools with their tasks
        
#         Raises:
#             ConsultantError: If user profile is not set or API call fails
#         """
#         if not self.user_profile:
#             raise ConsultantError("User profile must be set before generating roadmap")
        
#         # Build the prompt for roadmap generation
#         user_context = self._format_user_context()
        
#         prompt = f"""Based on the following user context, generate a comprehensive roadmap with timeline for each program the student is applying to. Break down the application process for each program into atomic steps. 
# {user_context}

# YOU MUST OUTPUT ONLY VALID JSON. Do not include any explanations, reasoning, or additional text. Output ONLY the JSON object below:

# {{
#   "admissionsCycle": "2025-2026",
#   "schools": [
#     {{
#       "schoolName": "School Name",
#       "schoolCode": "CODE",
#       "programName": "Program Name (if applicable)",
#       "tasks": [
#         {{
#           "taskId": "unique-id",
#           "title": "Task Title",
#           "description": "Detailed description of what needs to be done",
#           "deadlineISO": "YYYY-MM-DD",
#           "priority": "Critical|High|Medium|Low",
#           "type": "Administrative|Supplementary|Interview|Submission|Financial|Milestone"
#         }}
#       ]
#     }}
#   ]
# }}

# CRITICAL INSTRUCTIONS:
# 1. Include all programs the student listed in their profile
# 2. Break down each application into atomic, actionable steps
# 3. Use realistic deadlines based on typical university timelines (OUAC: Jan 15, McMaster supp: Jan 29, York Boost: Mar 20, UofT supp: Jan 15)
# 4. Prioritize tasks appropriately (Critical for must-do items, High for important, Medium for recommended, Low for optional)
# 5. Include all relevant task types: Administrative (account setup), Supplementary (essays, forms), Interview, Submission, Financial (scholarships), and Milestones
# 6. Ensure taskIds are unique and follow a consistent naming pattern (e.g., "mc-001", "york-002", "uoft-003")
# 7. Order tasks chronologically within each school

# OUTPUT ONLY THE JSON OBJECT. NO OTHER TEXT."""

#         try:
#             # Build messages for the API call
#             messages = [
#                 {
#                     "role": "system",
#                     "content": "You are an expert university admissions consultant. You MUST output ONLY valid JSON with no additional text, explanations, or reasoning. Your entire response must be parseable JSON."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
            
#             # Prepare request payload
#             payload = {
#                 "messages": messages,
#                 "stream": False,
#                 "include_functions_info": True,
#                 "include_retrieval_info": True,
#                 "include_guardrails_info": False
#             }
            
#             # Set headers
#             headers = {
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {self.agent_access_key}"
#             }
            
#             # Call DigitalOcean Agent API
#             response = requests.post(
#                 self.agent_endpoint,
#                 json=payload,
#                 headers=headers,
#                 timeout=60  # Longer timeout for complex generation
#             )
            
#             # Check for errors
#             if response.status_code != 200:
#                 raise ConsultantError(f"Agent API returned status {response.status_code}: {response.text}")
            
#             # Parse response
#             response_data = response.json()
            
#             if not response_data.get("choices"):
#                 raise ConsultantError(f"No response from agent. Full response: {response_data}")
            
#             # Try to get content from either content or reasoning_content
#             message = response_data["choices"][0]["message"]
#             roadmap_text = message.get("content", "")
            
#             # If content is empty, check reasoning_content (some models put output there)
#             if not roadmap_text or not roadmap_text.strip():
#                 roadmap_text = message.get("reasoning_content", "")
            
#             # Debug: Print the raw response
#             if not roadmap_text or not roadmap_text.strip():
#                 raise ConsultantError(f"Agent returned empty response. Full API response: {json.dumps(response_data, indent=2)}")
            
#             # Extract JSON from markdown code blocks if present
#             original_text = roadmap_text
#             if "```json" in roadmap_text:
#                 start = roadmap_text.find("```json") + 7
#                 end = roadmap_text.find("```", start)
#                 roadmap_text = roadmap_text[start:end].strip()
#             elif "```" in roadmap_text:
#                 start = roadmap_text.find("```") + 3
#                 end = roadmap_text.find("```", start)
#                 roadmap_text = roadmap_text[start:end].strip()
            
#             # Try to find JSON object in the text
#             if not roadmap_text.strip().startswith("{"):
#                 # Look for the first { and last }
#                 start_idx = original_text.find("{")
#                 end_idx = original_text.rfind("}")
#                 if start_idx != -1 and end_idx != -1:
#                     roadmap_text = original_text[start_idx:end_idx+1]
#                 else:
#                     raise ConsultantError(f"No JSON object found in response. Response preview: {original_text[:500]}")
            
#             roadmap_data = json.loads(roadmap_text)
            
#             return roadmap_data
        
#         except json.JSONDecodeError as e:
#             raise ConsultantError(f"Failed to parse roadmap JSON: {str(e)}. Response preview: {roadmap_text[:500] if roadmap_text else 'empty'}")
#         except requests.exceptions.Timeout:
#             raise ConsultantError("Request to agent timed out. Please try again.")
#         except requests.exceptions.RequestException as e:
#             raise ConsultantError(f"Failed to connect to agent: {str(e)}")
#         except Exception as e:
#             raise ConsultantError(f"Failed to generate roadmap: {str(e)}")
