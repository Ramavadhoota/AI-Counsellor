import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.config import settings
import json

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class AICounsellor:
    """AI Counsellor using Google Gemini"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def _build_context(self, user_profile: Optional[Dict[str, Any]] = None) -> str:
        """Build context from user profile"""
        if not user_profile:
            return "No user profile available."
        
        context_parts = []
        
        if user_profile.get("academic_background"):
            context_parts.append(f"Academic Background: {json.dumps(user_profile['academic_background'])}")
        
        if user_profile.get("interests"):
            context_parts.append(f"Interests: {', '.join(user_profile['interests'])}")
        
        if user_profile.get("career_goals"):
            context_parts.append(f"Career Goals: {json.dumps(user_profile['career_goals'])}")
        
        if user_profile.get("preferences"):
            context_parts.append(f"Preferences: {json.dumps(user_profile['preferences'])}")
        
        return "\n".join(context_parts)
    
    def chat(
        self,
        message: str,
        user_profile: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Have a conversation with the AI counsellor
        
        Args:
            message: User's message
            user_profile: User profile data
            conversation_history: Previous conversation messages
        
        Returns:
            AI response
        """
        system_prompt = """You are an expert AI Career and Education Counsellor. Your role is to:
        - Provide personalized career guidance
        - Recommend suitable universities and courses
        - Help students make informed decisions about their education
        - Analyze academic profiles and suggest improvement areas
        - Be empathetic, supportive, and professional
        
        Always provide detailed, actionable advice tailored to the student's profile.
        """
        
        # Build context
        context = self._build_context(user_profile)
        
        # Build conversation
        prompt_parts = [system_prompt]
        
        if context:
            prompt_parts.append(f"\n**Student Profile:**\n{context}\n")
        
        # Add conversation history
        if conversation_history:
            prompt_parts.append("\n**Previous Conversation:**")
            for msg in conversation_history[-10:]:  # Last 10 messages
                role = "Student" if msg["role"] == "user" else "Counsellor"
                prompt_parts.append(f"{role}: {msg['content']}")
        
        # Add current message
        prompt_parts.append(f"\nStudent: {message}")
        prompt_parts.append("\nCounsellor:")
        
        full_prompt = "\n".join(prompt_parts)
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}"
    
    def recommend_universities(
        self,
        user_profile: Dict[str, Any],
        universities: List[Dict[str, Any]],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Recommend universities based on user profile
        
        Args:
            user_profile: User's profile data
            universities: List of universities to rank
            limit: Number of recommendations
        
        Returns:
            List of recommended universities with scores and reasoning
        """
        context = self._build_context(user_profile)
        
        universities_text = "\n".join([
            f"{i+1}. {uni['name']} - {uni['country']}"
            for i, uni in enumerate(universities)
        ])
        
        prompt = f"""Based on the following student profile, rank and recommend the top {limit} universities from the list below.

**Student Profile:**
{context}

**Universities:**
{universities_text}

Provide recommendations in JSON format:
[
  {{
    "university_name": "...",
    "match_score": 85,
    "reasoning": "Why this university is a good fit..."
  }}
]

Consider factors like:
- Academic fit
- Career goals alignment
- Location preferences
- Budget considerations (if mentioned)
- Program offerings
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from response
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                recommendations = json.loads(response_text[json_start:json_end])
                return recommendations[:limit]
            
            return []
        except Exception as e:
            print(f"Error in recommend_universities: {str(e)}")
            return []
    
    def suggest_career_paths(
        self,
        user_profile: Dict[str, Any],
        field_of_interest: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest career paths based on profile
        
        Args:
            user_profile: User's profile data
            field_of_interest: Specific field to explore
        
        Returns:
            List of career options
        """
        context = self._build_context(user_profile)
        
        field_clause = f" in the field of {field_of_interest}" if field_of_interest else ""
        
        prompt = f"""Based on the student profile below, suggest 5 suitable career paths{field_clause}.

**Student Profile:**
{context}

Provide suggestions in JSON format:
[
  {{
    "career_title": "...",
    "description": "Brief description...",
    "required_education": ["Degree 1", "Degree 2"],
    "average_salary_range": "$X - $Y",
    "growth_outlook": "High/Medium/Low with explanation",
    "key_skills": ["Skill 1", "Skill 2", "Skill 3"]
  }}
]
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                careers = json.loads(response_text[json_start:json_end])
                return careers
            
            return []
        except Exception as e:
            print(f"Error in suggest_career_paths: {str(e)}")
            return []
    
    def recommend_courses(
        self,
        user_profile: Dict[str, Any],
        career_goal: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Recommend courses/programs based on profile and career goals
        
        Args:
            user_profile: User's profile data
            career_goal: Target career
        
        Returns:
            List of course recommendations
        """
        context = self._build_context(user_profile)
        
        career_clause = f" to pursue a career as {career_goal}" if career_goal else ""
        
        prompt = f"""Based on the student profile, recommend 5 suitable courses/degree programs{career_clause}.

**Student Profile:**
{context}

Provide recommendations in JSON format:
[
  {{
    "course_name": "...",
    "institution_type": "University/College/Online",
    "duration": "X years",
    "description": "What the course covers...",
    "prerequisites": ["Requirement 1", "Requirement 2"],
    "career_outcomes": ["Career 1", "Career 2", "Career 3"]
  }}
]
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                courses = json.loads(response_text[json_start:json_end])
                return courses
            
            return []
        except Exception as e:
            print(f"Error in recommend_courses: {str(e)}")
            return []
    
    def analyze_document(
        self,
        document_text: str,
        document_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze uploaded documents (resume, SOP, etc.)
        
        Args:
            document_text: Text content of document
            document_type: Type of document
        
        Returns:
            Analysis with suggestions
        """
        prompt = f"""Analyze the following {document_type} document and provide detailed feedback.

**Document Content:**
{document_text}

Provide analysis in JSON format:
{{
  "analysis": "Overall assessment...",
  "strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "improvements": ["Improvement 1", "Improvement 2", "Improvement 3"],
  "suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                analysis = json.loads(response_text[json_start:json_end])
                return analysis
            
            return {
                "analysis": response.text,
                "strengths": [],
                "improvements": [],
                "suggestions": []
            }
        except Exception as e:
            print(f"Error in analyze_document: {str(e)}")
            return {
                "analysis": "Unable to analyze document.",
                "strengths": [],
                "improvements": [],
                "suggestions": []
            }

# Singleton instance
ai_counsellor = AICounsellor()
