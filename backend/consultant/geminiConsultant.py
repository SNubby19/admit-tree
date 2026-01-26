# """
# Gemini Consultant Chatbot
# A wrapper around Google's Gemini API that provides personalized academic consulting.
# """

# import os
# from typing import List, Dict
# from pathlib import Path
# import google.generativeai as genai
# from consultant.mockdata.user import User, Grade12OrAbove, BelowGrade12


# def load_env():
#     """Load environment variables from .env file"""
#     env_path = Path(__file__).parent.parent / '.env'
#     if env_path.exists():
#         with open(env_path) as f:
#             for line in f:
#                 line = line.strip()
#                 if line and not line.startswith('#') and '=' in line:
#                     key, value = line.split('=', 1)
#                     os.environ[key.strip()] = value.strip()


# class ConsultantError(Exception):
#     """Base exception for consultant errors"""
#     pass


# class Consultant:
#     """
#     AI-powered consultant that provides personalized academic guidance using Gemini API.
#     """
    
#     def __init__(self, api_key: str = None):
#         """
#         Initialize the consultant with Gemini API credentials.
        
#         Args:
#             api_key: Google Gemini API key. If None, reads from GEMINI_API_KEY env var.
        
#         Raises:
#             ConsultantError: If API key is missing or invalid
#         """
#         # Load .env file
#         load_env()
        
#         self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
#         if not self.api_key:
#             raise ConsultantError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
        
#         try:
#             genai.configure(api_key=self.api_key)
#             self.model = genai.GenerativeModel('gemini-2.5-flash')
#         except Exception as e:
#             raise ConsultantError(f"Failed to initialize Gemini API: {str(e)}")
        
#         self.conversation_history: List[Dict[str, str]] = []
#         self.user_profile: User = None
    
#     def set_user_profile(self, user: User):
#         """
#         Set the user profile for personalized responses.
        
#         Args:
#             user: User object containing academic and extracurricular data
#         """
#         self.user_profile = user
    
#     def _format_user_context(self) -> str:
#         """
#         Format user profile data into a structured context string for Gemini.
        
#         Returns:
#             Formatted context string describing the user's profile
#         """
#         if not self.user_profile:
#             return ""
        
#         user = self.user_profile
#         context_parts = [
#             f"Student Profile:",
#             f"Name: {user.name}",
#             f"Email: {user.email}",
#             "",
#             "Academic Information:"
#         ]
        
#         # Format academic info based on grade level
#         if isinstance(user.academic, Grade12OrAbove):
#             context_parts.append(f"- Grade Level: 12 or above")
#             context_parts.append(f"- GPA/Average: {user.academic.gpa_or_average}")
#             context_parts.append(f"- Courses Taken:")
#             for course in user.academic.courses_taken:
#                 grade_str = f" (Grade: {course.grade})" if course.grade else ""
#                 code_str = f" [{course.course_code}]" if course.course_code else ""
#                 context_parts.append(f"  * {course.course_name}{code_str}{grade_str}")
        
#         elif isinstance(user.academic, BelowGrade12):
#             context_parts.append(f"- Grade Level: {user.academic.grade_level}")
#             if user.academic.current_average:
#                 context_parts.append(f"- Current Average: {user.academic.current_average}")
            
#             context_parts.append(f"- Courses Completed:")
#             for course in user.academic.courses_so_far:
#                 grade_str = f" (Grade: {course.grade})" if course.grade else ""
#                 code_str = f" [{course.course_code}]" if course.course_code else ""
#                 context_parts.append(f"  * {course.course_name}{code_str}{grade_str}")
            
#             if user.academic.planned_courses:
#                 context_parts.append(f"- Planned Courses:")
#                 for course in user.academic.planned_courses:
#                     code_str = f" [{course.course_code}]" if course.course_code else ""
#                     reason_str = f" - {course.reason}" if course.reason else ""
#                     context_parts.append(f"  * {course.course_name}{code_str}{reason_str}")
        
#         # Format extracurriculars
#         if user.extracurriculars:
#             context_parts.append("")
#             context_parts.append("Extracurricular Activities:")
#             for activity in user.extracurriculars:
#                 role_str = f" - {activity.role_title}" if activity.role_title else ""
#                 context_parts.append(f"- {activity.name}{role_str}")
#                 context_parts.append(f"  * Leadership Level: {activity.leadership_level}/5")
#                 if activity.impact_level:
#                     context_parts.append(f"  * Impact Level: {activity.impact_level}/5")
#                 if activity.hours_per_week:
#                     context_parts.append(f"  * Time Commitment: {activity.hours_per_week} hours/week")
#                 if activity.months:
#                     context_parts.append(f"  * Duration: {activity.months} months")
#                 if activity.notes:
#                     context_parts.append(f"  * Notes: {activity.notes}")
        
#         # Format interests
#         if user.interests:
#             context_parts.append("")
#             context_parts.append(f"Interests: {', '.join(user.interests)}")
        
#         # Format pathway preferences
#         context_parts.append("")
#         context_parts.append("Pathway Preferences:")
#         context_parts.append(f"- Co-op Importance: {user.pathway_preference.coop_importance}/10")
#         context_parts.append(f"- Research Importance: {user.pathway_preference.research_importance}/10")
        
#         # Format links if available
#         if user.links.resume_url or user.links.linkedin_url or user.links.github_url:
#             context_parts.append("")
#             context_parts.append("Additional Links:")
#             if user.links.resume_url:
#                 context_parts.append(f"- Resume: {user.links.resume_url}")
#             if user.links.linkedin_url:
#                 context_parts.append(f"- LinkedIn: {user.links.linkedin_url}")
#             if user.links.github_url:
#                 context_parts.append(f"- GitHub: {user.links.github_url}")
        
#         # Format roadmap if available
#         if user.roadmap and user.roadmap.tasks:
#             context_parts.append("")
#             context_parts.append(f"Application Roadmap ({user.roadmap.school} - {user.roadmap.program}):")
#             context_parts.append(f"- Progress: {user.roadmap.progress}% complete")
#             context_parts.append(f"- Application Deadline: {user.roadmap.deadline}")
#             context_parts.append("- Tasks:")
#             for i, task in enumerate(user.roadmap.tasks):
#                 status_emoji = "✓" if task.status == "done" else "→" if task.status == "in progress" else "○"
#                 context_parts.append(f"  {i+1}. [{status_emoji}] {task.content}")
#                 context_parts.append(f"     Deadline: {task.deadline} | Status: {task.status}")
        
#         return "\n".join(context_parts)
    
#     def ask(self, question: str) -> str:
#         """
#         Ask the consultant a question and get a personalized response.
        
#         Args:
#             question: User's question or message
        
#         Returns:
#             Consultant's response based on user profile and conversation history
        
#         Raises:
#             ConsultantError: If API call fails or other errors occur
#         """
#         if not question or not question.strip():
#             raise ConsultantError("Question cannot be empty")
        
#         try:
#             # Build the full prompt with context
#             prompt_parts = []
            
#             # Add user profile context
#             user_context = self._format_user_context()
#             if user_context:
#                 prompt_parts.append("You are an academic consultant helping a student. Here is their profile:")
#                 prompt_parts.append(user_context)
#                 prompt_parts.append("")
#                 prompt_parts.append("Provide personalized advice based on this profile.")
#                 prompt_parts.append("")
            
#             # Add conversation history
#             if self.conversation_history:
#                 prompt_parts.append("Previous conversation:")
#                 for msg in self.conversation_history:
#                     prompt_parts.append(f"{msg['role']}: {msg['content']}")
#                 prompt_parts.append("")
            
#             # Add current question
#             prompt_parts.append(f"Student: {question}")
            
#             full_prompt = "\n".join(prompt_parts)
            
#             # Call Gemini API
#             response = self.model.generate_content(full_prompt)
            
#             if not response or not response.text:
#                 raise ConsultantError("Received empty response from Gemini API")
            
#             answer = response.text
            
#             # Update conversation history
#             self.conversation_history.append({"role": "Student", "content": question})
#             self.conversation_history.append({"role": "Consultant", "content": answer})
            
#             return answer
        
#         except Exception as e:
#             if "API key" in str(e):
#                 raise ConsultantError("Invalid API key. Please check your credentials.")
#             elif "quota" in str(e).lower() or "rate limit" in str(e).lower():
#                 raise ConsultantError("API rate limit exceeded. Please try again later.")
#             else:
#                 raise ConsultantError(f"Failed to generate response: {str(e)}")
    
#     def clear_history(self):
#         """Clear the conversation history."""
#         self.conversation_history = []

























"""
Gemini API Fallback Consultant
Direct integration with Google's Gemini API as a fallback when DigitalOcean Agent is unavailable.
"""

import os
import json
import google.generativeai as genai
from typing import List, Dict
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


class GeminiConsultant:
    """
    AI-powered consultant using Google's Gemini API directly.
    """
    
    def __init__(self):
        """Initialize the consultant with Gemini API key."""
        load_env()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ConsultantError("GEMINI_API_KEY is required in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.conversation_history: List[Dict[str, str]] = []
        self.user_profile: User = None
    
    def set_user_profile(self, user: User):
        """Set the user profile for personalized responses."""
        self.user_profile = user
    
    def _format_user_context(self) -> str:
        """Format user profile data into a structured context string."""
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
        
        return "\n".join(context_parts)
    
    def ask(self, question: str) -> str:
        """Ask the consultant a question and get a personalized response."""
        if not question or not question.strip():
            raise ConsultantError("Question cannot be empty")
        
        try:
            # Build the full prompt with context
            user_context = self._format_user_context()
            
            if user_context:
                system_prompt = f"""You are an expert university admissions consultant. Here is the student's profile:

{user_context}

Provide personalized advice based on this profile. Be specific, actionable, and encouraging."""
                
                full_prompt = f"{system_prompt}\n\nStudent Question: {question}"
            else:
                full_prompt = question
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            answer = response.text
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            return answer
        
        except Exception as e:
            raise ConsultantError(f"Failed to generate response: {str(e)}")
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def generate_program_roadmap(self, programs: List) -> Dict:
        """Generate a roadmap for a list of programs."""
        if not programs:
            raise ConsultantError("Programs list cannot be empty")
        
        programs_text = "\n".join([f"- {p.school}: {p.program}" for p in programs])
        
        prompt = f"""Generate a comprehensive application roadmap for these Ontario engineering programs:
{programs_text}

YOU MUST OUTPUT ONLY VALID JSON in this EXACT format:
{{
  "admissionsCycle": "2025-2026",
  "schools": [
    {{
      "schoolName": "General (OUAC)",
      "schoolCode": "OUAC",
      "tasks": [
        {{
          "taskId": "ouac-001",
          "title": "Create OUAC Account",
          "description": "Create your account on the Ontario Universities' Application Centre (OUAC) website.",
          "deadlineISO": "2025-11-01",
          "priority": "High",
          "type": "Administrative"
        }}
      ]
    }},
    {{
      "schoolName": "University Name",
      "schoolCode": "CODE",
      "programName": "Program Name",
      "tasks": [...]
    }}
  ]
}}

Include realistic deadlines: OUAC Jan 15 2026, McMaster supp Jan 29 2026, Waterloo AIF Jan 30 2026, UofT OSP Jan 15 2026, York Boost Mar 20 2026.
Priority levels: Critical, High, Medium, Low
Task types: Administrative, Supplementary, Interview, Submission, Financial, Milestone

OUTPUT ONLY THE JSON OBJECT."""

        try:
            response = self.model.generate_content(prompt)
            roadmap_text = response.text
            
            # Extract JSON from markdown code blocks if present
            if "```json" in roadmap_text:
                start = roadmap_text.find("```json") + 7
                end = roadmap_text.find("```", start)
                roadmap_text = roadmap_text[start:end].strip()
            elif "```" in roadmap_text:
                start = roadmap_text.find("```") + 3
                end = roadmap_text.find("```", start)
                roadmap_text = roadmap_text[start:end].strip()
            
            # Try to find JSON object in the text
            if not roadmap_text.strip().startswith("{"):
                start_idx = roadmap_text.find("{")
                end_idx = roadmap_text.rfind("}")
                if start_idx != -1 and end_idx != -1:
                    roadmap_text = roadmap_text[start_idx:end_idx+1]
            
            roadmap_data = json.loads(roadmap_text)
            return roadmap_data
        
        except json.JSONDecodeError as e:
            raise ConsultantError(f"Failed to parse roadmap JSON: {str(e)}")
        except Exception as e:
            raise ConsultantError(f"Failed to generate roadmap: {str(e)}")
