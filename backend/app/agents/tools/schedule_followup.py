"""
Tool #3: Schedule Follow-up
Creates follow-up meetings with AI-generated talking points.
"""
from datetime import datetime, timedelta
from app.utils.llm_utils import llm
import json


def schedule_followup(hcp_name: str, user_message: str) -> dict:
    """
    Schedule a follow-up meeting with AI-generated talking points.
    
    Args:
        hcp_name: The HCP's name
        user_message: User's follow-up request
        
    Example Input:
        hcp_name = "Dr. Smith"
        user_message = "Schedule a follow-up with Dr. Smith next week to discuss trial results"
    
    Returns:
        {
            'follow_up_date': '2026-01-25',
            'talking_points': ['Discuss trial results', 'Share new data', 'Address concerns'],
            'preparation_notes': 'Prepare trial data presentation',
            'hcp_name': 'Dr. Smith',
            'success': True
        }
    """
    
    today = datetime.now().strftime('%Y-%m-%d')
    next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    next_month = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    prompt = f"""You are a medical sales coach helping schedule follow-up meetings.

HCP Name: {hcp_name}
User request: "{user_message}"
Today's date: {today}

Extract follow-up scheduling information:

1. follow_up_date: Infer the date from the user's message in YYYY-MM-DD format
   - "next week" = approximately {next_week}
   - "next month" = approximately {next_month}
   - "tomorrow" = one day from today
   - If no specific time mentioned, default to one week from today

2. talking_points: Generate 3-4 key topics to discuss in the follow-up
   - Based on the user's message
   - Be specific and actionable

3. preparation_notes: What should be prepared before the meeting
   - Materials needed
   - Data to gather
   - Questions to prepare

Return ONLY valid JSON (no markdown):
{{
    "follow_up_date": "YYYY-MM-DD",
    "talking_points": ["point1", "point2", "point3"],
    "preparation_notes": "what to prepare"
}}
"""
    
    try:
        result = llm.extract_json(prompt, temperature=0.2)
        
        result['success'] = True
        result['hcp_name'] = hcp_name
        
        # Provide defaults
        if not result.get('follow_up_date'):
            result['follow_up_date'] = next_week
        if not result.get('talking_points'):
            result['talking_points'] = ['Follow-up discussion', 'Address questions', 'Next steps']
        if not result.get('preparation_notes'):
            result['preparation_notes'] = 'Review previous interaction notes'
        
        return result
        
    except Exception as e:
        print(f"❌ Error in schedule_followup tool: {e}")
        return {
            'success': False,
            'error': str(e),
            'hcp_name': hcp_name,
            'follow_up_date': next_week,
            'talking_points': [],
            'preparation_notes': None
        }
