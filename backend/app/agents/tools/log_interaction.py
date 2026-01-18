"""
Tool #1: Log Interaction
Extracts structured HCP interaction data from natural language.
"""
import json
from datetime import datetime
from app.utils.llm_utils import llm


def log_interaction(user_message: str) -> dict:
    """
    Extract structured interaction data from natural language.
    
    This is the PRIMARY tool for logging new HCP interactions.
    It uses the LLM to extract all relevant fields from a user's 
    natural language description.
    
    Args:
        user_message: Natural language description of HCP interaction
        
    Example Input:
        "Today I met with Dr. Smith and discussed product X efficiency. 
         The sentiment was positive, and I shared the brochures."
    
    Returns:
        Dictionary with extracted fields:
        {
            'hcp_name': 'Dr. Smith',
            'date': '2026-01-18',
            'sentiment': 'Positive',
            'materials_shared': ['brochures'],
            'discussion_summary': 'Discussed product X efficiency',
            'products_discussed': ['product X'],
            'success': True
        }
    """
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    prompt = f"""You are an expert medical sales assistant. Extract structured information from the user's message about their HCP interaction.

User message: "{user_message}"

Today's date is {today}.

Extract the following information and return ONLY valid JSON (no markdown, no code blocks, no explanation):

1. hcp_name: The doctor/healthcare professional's name (e.g., "Dr. Smith", "Dr. John Patel")
2. date: The date of meeting in YYYY-MM-DD format. If not specified, use today's date: {today}
3. sentiment: The overall sentiment (must be one of: "Positive", "Negative", or "Neutral")
4. materials_shared: Array of materials/documents shared (e.g., ["brochures", "samples", "clinical data"])
5. discussion_summary: Brief summary of what was discussed
6. products_discussed: Array of product names mentioned (e.g., ["product X", "diabetes medication"])

Return ONLY this JSON format, nothing else:
{{
    "hcp_name": "extracted name or null",
    "date": "YYYY-MM-DD",
    "sentiment": "Positive|Negative|Neutral",
    "materials_shared": ["item1", "item2"],
    "discussion_summary": "brief summary",
    "products_discussed": ["product1", "product2"]
}}

IMPORTANT: 
- If a field cannot be extracted, use null for strings or [] for arrays
- Always return valid JSON
- Do not include any text before or after the JSON
"""
    
    try:
        result = llm.extract_json(prompt, temperature=0.1)
        
        # Ensure all required fields exist
        result['success'] = True
        
        # Provide defaults for missing fields
        if not result.get('hcp_name'):
            result['hcp_name'] = None
        if not result.get('date'):
            result['date'] = today
        if not result.get('sentiment'):
            result['sentiment'] = 'Neutral'
        if not result.get('materials_shared'):
            result['materials_shared'] = []
        if not result.get('discussion_summary'):
            result['discussion_summary'] = None
        if not result.get('products_discussed'):
            result['products_discussed'] = []
        
        return result
        
    except Exception as e:
        print(f"❌ Error in log_interaction tool: {e}")
        return {
            'success': False,
            'error': str(e),
            'hcp_name': None,
            'date': today,
            'sentiment': 'Neutral',
            'materials_shared': [],
            'discussion_summary': None,
            'products_discussed': []
        }
