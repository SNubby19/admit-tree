"""
Gemini Consultant Chatbot
A wrapper around Google's Gemini API that provides personalized academic consulting.
"""

import os
import re
from typing import List, Dict, Optional
from pathlib import Path
import google.generativeai as genai
from consultant.mockdata.user import User, Grade12OrAbove, BelowGrade12, Task, Subtask, IssueType


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
    AI-powered consultant that provides personalized academic guidance using Gemini API.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the consultant with Gemini API credentials.
        
        Args:
            api_key: Google Gemini API key. If None, reads from GEMINI_API_KEY env var.
        
        Raises:
            ConsultantError: If API key is missing or invalid
        """
        # Load .env file
        load_env()
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ConsultantError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            raise ConsultantError(f"Failed to initialize Gemini API: {str(e)}")
        
        self.conversation_history: List[Dict[str, str]] = []
        self.user_profile: User = None
        self.pending_subtasks: Optional[Dict] = None  # Store proposed subtasks awaiting confirmation
    
    def set_user_profile(self, user: User):
        """
        Set the user profile for personalized responses.
        
        Args:
            user: User object containing academic and extracurricular data
        """
        self.user_profile = user
    
    def _format_user_context(self) -> str:
        """
        Format user profile data into a structured context string for Gemini.
        
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
    
    def _classify_issue(self, question: str) -> IssueType:
        """
        Use Gemini to classify the question into an issue type.
        
        Args:
            question: User's question
        
        Returns:
            IssueType enum value
        """
        try:
            classification_prompt = f"""Classify this question into ONE of these categories:

1. DIFFICULT_TASK: The user is struggling with or asking for help with a specific task, assignment, test, or activity AND the task can be broken down into smaller, actionable steps.

2. NONE: General question, advice request, or a task that cannot be meaningfully broken down into smaller steps.

Question: "{question}"

Consider: Can this task be broken down into smaller steps? If yes, answer DIFFICULT_TASK. If not, answer NONE.

Respond with ONLY one word: either "DIFFICULT_TASK" or "NONE"."""

            response = self.model.generate_content(classification_prompt)
            classification = response.text.strip().upper()
            
            if "DIFFICULT_TASK" in classification:
                return IssueType.DIFFICULT_TASK
            else:
                return IssueType.NONE
        except Exception:
            # If classification fails, default to NONE (fallback to wrapper)
            return IssueType.NONE
    
    def _find_related_task(self, question: str) -> Optional[Task]:
        """
        Find which task from the user's roadmap the question is about.
        
        Args:
            question: User's question
        
        Returns:
            Matching Task or None
        """
        if not self.user_profile or not self.user_profile.roadmap:
            return None
        
        question_lower = question.lower()
        
        # Simple keyword matching
        for task in self.user_profile.roadmap.tasks:
            task_keywords = task.content.lower().split()
            # Check if any significant words from the task appear in the question
            for keyword in task_keywords:
                if len(keyword) > 3 and keyword in question_lower:
                    return task
        
        return None
    
    def _generate_subtasks(self, task: Task) -> List[str]:
        """
        Use Gemini to break down a task into smaller subtasks.
        
        Args:
            task: The task to break down
        
        Returns:
            List of subtask descriptions
        """
        try:
            user_context = self._format_user_context()
            
            breakdown_prompt = f"""You are helping a student break down a difficult task into smaller, manageable steps.

{user_context}

Task to break down:
- Content: {task.content}
- Deadline: {task.deadline}
- Current Status: {task.status}

Please provide 3-5 specific, actionable subtasks that will help the student complete this task.
Each subtask should be:
- Clear and specific
- Achievable in a reasonable timeframe
- Directly related to completing the main task

Format your response as a numbered list (1., 2., 3., etc.) with just the subtask description on each line.
Do not include any other text, explanations, or formatting."""

            response = self.model.generate_content(breakdown_prompt)
            subtasks_text = response.text.strip()
            
            # Parse the numbered list
            subtasks = []
            for line in subtasks_text.split('\n'):
                line = line.strip()
                # Match lines starting with number and period (1., 2., etc.)
                match = re.match(r'^\d+\.\s*(.+)$', line)
                if match:
                    subtasks.append(match.group(1))
            
            return subtasks if subtasks else []
        
        except Exception as e:
            raise ConsultantError(f"Failed to generate subtasks: {str(e)}")
    
    def _format_subtask_proposal(self, task: Task, subtasks: List[Subtask]) -> str:
        """
        Format the subtask proposal for user confirmation.
        
        Args:
            task: The main task
            subtasks: List of proposed subtasks
        
        Returns:
            Formatted proposal string
        """
        lines = [
            "I can help you break down this task into smaller, manageable steps:",
            "",
            f"Main Task: {task.content}",
            f"Deadline: {task.deadline}",
            f"Status: {task.status}",
            "",
            "Here's a breakdown:",
            ""
        ]
        
        for i, subtask in enumerate(subtasks, 1):
            lines.append(f"{i}. [ ] {subtask.content}")
        
        lines.append("")
        lines.append("Do you want to add these subtasks to the current task? Yes / Cancel")
        
        return "\n".join(lines)
    
    def _handle_difficult_task(self, question: str, task: Task) -> str:
        """
        Execute the DifficultTask strategy: break down the task into subtasks.
        
        Args:
            question: User's question
            task: The task they're struggling with
        
        Returns:
            Response with subtask breakdown and confirmation prompt
        """
        try:
            # Generate subtasks using Gemini
            subtask_descriptions = self._generate_subtasks(task)
            
            if not subtask_descriptions:
                # If no subtasks generated, fall back to wrapper
                return self._gemini_wrapper(question)
            
            # Create Subtask objects
            proposed_subtasks = [
                Subtask(content=desc, status="to do")
                for desc in subtask_descriptions
            ]
            
            # Store pending subtasks for confirmation
            self.pending_subtasks = {
                'task': task,
                'subtasks': proposed_subtasks
            }
            
            # Return formatted proposal
            return self._format_subtask_proposal(task, proposed_subtasks)
        
        except Exception as e:
            raise ConsultantError(f"Failed to handle difficult task: {str(e)}")
    
    def _confirm_subtasks(self) -> str:
        """Add pending subtasks to the task."""
        if not self.pending_subtasks:
            return "No pending subtasks to confirm."
        
        task = self.pending_subtasks['task']
        task.subtasks = self.pending_subtasks['subtasks']
        task_name = task.content.split('-')[0].strip()  # Get short name
        
        self.pending_subtasks = None
        
        return f"✓ Subtasks added to \"{task_name}\"! You can now track your progress on each step."
    
    def _cancel_subtasks(self) -> str:
        """Cancel adding subtasks."""
        self.pending_subtasks = None
        return "Subtasks not added. Let me know if you need anything else!"
    
    def _gemini_wrapper(self, question: str) -> str:
        """
        Original Gemini wrapper logic - general purpose response generation.
        
        Args:
            question: User's question
        
        Returns:
            Gemini's response
        """
        # Build the full prompt with context
        prompt_parts = []
        
        # Add user profile context
        user_context = self._format_user_context()
        if user_context:
            prompt_parts.append("You are an academic consultant helping a student. Here is their profile:")
            prompt_parts.append(user_context)
            prompt_parts.append("")
            prompt_parts.append("Provide personalized advice based on this profile.")
            prompt_parts.append("")
        
        # Add conversation history
        if self.conversation_history:
            prompt_parts.append("Previous conversation:")
            for msg in self.conversation_history:
                prompt_parts.append(f"{msg['role']}: {msg['content']}")
            prompt_parts.append("")
        
        # Add current question
        prompt_parts.append(f"Student: {question}")
        
        full_prompt = "\n".join(prompt_parts)
        
        # Call Gemini API
        response = self.model.generate_content(full_prompt)
        
        if not response or not response.text:
            raise ConsultantError("Received empty response from Gemini API")
        
        return response.text
    
    def ask(self, question: str) -> str:
        """
        Ask the consultant a question and get a personalized response.
        
        Args:
            question: User's question or message
        
        Returns:
            Consultant's response based on user profile and conversation history
        
        Raises:
            ConsultantError: If API call fails or other errors occur
        """
        if not question or not question.strip():
            raise ConsultantError("Question cannot be empty")
        
        try:
            question_lower = question.lower().strip()
            
            # Check if user is responding to subtask confirmation
            if self.pending_subtasks:
                if question_lower in ['yes', 'y']:
                    answer = self._confirm_subtasks()
                    self.conversation_history.append({"role": "Student", "content": question})
                    self.conversation_history.append({"role": "Consultant", "content": answer})
                    return answer
                elif question_lower in ['cancel', 'no', 'n']:
                    answer = self._cancel_subtasks()
                    self.conversation_history.append({"role": "Student", "content": question})
                    self.conversation_history.append({"role": "Consultant", "content": answer})
                    return answer
                else:
                    # User asked a new question, clear pending subtasks
                    self.pending_subtasks = None
            
            # Classify the issue
            issue_type = self._classify_issue(question)
            
            # Route based on issue type
            if issue_type == IssueType.DIFFICULT_TASK:
                task = self._find_related_task(question)
                if task:
                    answer = self._handle_difficult_task(question, task)
                    self.conversation_history.append({"role": "Student", "content": question})
                    self.conversation_history.append({"role": "Consultant", "content": answer})
                    return answer
            
            # Fallback to Gemini wrapper
            answer = self._gemini_wrapper(question)
            
            # Update conversation history
            self.conversation_history.append({"role": "Student", "content": question})
            self.conversation_history.append({"role": "Consultant", "content": answer})
            
            return answer
        
        except Exception as e:
            if "API key" in str(e):
                raise ConsultantError("Invalid API key. Please check your credentials.")
            elif "quota" in str(e).lower() or "rate limit" in str(e).lower():
                raise ConsultantError("API rate limit exceeded. Please try again later.")
            else:
                raise ConsultantError(f"Failed to generate response: {str(e)}")
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        self.pending_subtasks = None
