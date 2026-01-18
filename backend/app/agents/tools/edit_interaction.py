"""
Tool #2: Edit Interaction
Updates interaction by identifying ONLY changed fields.
"""
import json
from app.utils.llm_utils import llm


def edit_interaction(current_data: dict, user_message: str) -> dict:
    """
    Update interaction by identifying which fields changed.
    
    This tool is crucial for the "edit via conversation" feature.
    It identifies ONLY the fields the user wants to change and
    preserves all other fields.
    
    Args:
        current_data: Current interaction dictionary with all fields
        user_message: User's correction/edit instruction
        
    Example Input:
        current_data = {
            'hcp_name': 'Dr. Smith',
            'sentiment': 'Positive',
            'materials_shared': ['brochures']
        }
        user_message = "Sorry, the name was actually Dr. John, and sentiment was negative"
    
    Returns:
        Updated dictionary with ONLY changed fields merged:
        {
            'hcp_name': 'Dr. John',  # ← Changed
            'sentiment': 'Negative',  # ← Changed
            'materials_shared': ['brochures'],  # ← Preserved
            'success': True
        }
    """
    
    prompt = f"""You are an expert medical sales assistant. The user wants to correct/update an existing HCP interaction record.

Current interaction data:
{json.dumps(current_data, indent=2)}

User's correction message: "{user_message}"

Identify ONLY the fields that the user wants to change and extract their new values.

Return ONLY valid JSON (no markdown, no explanation) with ONLY the fields that changed:

Example: If user says "sentiment was negative", return: {{"sentiment": "Negative"}}
Example: If user says "name was Dr. John and I shared samples", return: {{"hcp_name": "Dr. John", "materials_shared": ["samples"]}}

Available fields you can change:
- hcp_name (string)
- date (YYYY-MM-DD format)
- sentiment ("Positive", "Negative", or "Neutral")
- materials_shared (array of strings)
- discussion_summary (string)
- products_discussed (array of strings)
- follow_up_date (YYYY-MM-DD format or null)

Return ONLY the changed fields as JSON. If nothing changed, return {{}}.
"""
    
    try:
        changes = llm.extract_json(prompt, temperature=0.1)
        
        # If LLM returned error or empty
        if 'error' in changes or not changes:
            changes = {}
        
        # Merge changes with current data (changes override)
        updated_data = {**current_data, **changes}
        updated_data['success'] = True
        
        return updated_data
        
    except Exception as e:
        print(f"❌ Error in edit_interaction tool: {e}")
        # Return original data on error
        return {
            'success': False,
            'error': str(e),
            **current_data
        }
