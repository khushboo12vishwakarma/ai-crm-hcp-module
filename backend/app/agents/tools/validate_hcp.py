"""
Tool #5: Validate HCP
Validates and enriches HCP information.
"""
from app.utils.llm_utils import llm
import json


def validate_hcp(hcp_name: str) -> dict:
    """
    Validate and enrich HCP information.
    
    Verifies HCP name format and provides additional context
    like likely specialty based on naming patterns.
    
    Args:
        hcp_name: The HCP's name to validate
    
    Example Input:
        "dr smith"
    
    Returns:
        {
            'is_valid': True,
            'formatted_name': 'Dr. Smith',
            'likely_specialty': 'General Practice',
            'validation_notes': 'Name format corrected to proper case',
            'requires_verification': False,
            'success': True
        }
    """
    
    if not hcp_name or len(hcp_name.strip()) == 0:
        return {
            'success': False,
            'error': 'HCP name is empty',
            'is_valid': False,
            'formatted_name': None,
            'requires_verification': True
        }
    
    prompt = f"""You are a healthcare database expert. Validate and enrich this HCP name.

HCP Name: "{hcp_name}"

Analyze and return:

1. is_valid: Is this a valid HCP name format? (true/false)
   - Valid examples: "Dr. Smith", "Dr. John Patel", "Prof. Williams"
   - Invalid examples: "doctor", "xyz", "123"

2. formatted_name: Properly formatted name with correct capitalization and title
   - Add "Dr." prefix if missing but clearly a doctor's name
   - Proper case for names (e.g., "smith" → "Smith")
   - Keep existing titles (Dr., Prof., etc.)

3. likely_specialty: Best guess of medical specialty based on common naming patterns or context
   - Options: "Cardiology", "Neurology", "Oncology", "Pediatrics", "General Practice", "Surgery", "Unknown"
   - If no context, use "General Practice"

4. validation_notes: Any issues found or corrections made
   - Examples: "Name format corrected", "Added Dr. prefix", "No issues found"

5. requires_verification: Should this be manually verified? (true/false)
   - True if name is very short, unusual, or incomplete

Return ONLY valid JSON (no markdown):
{{
    "is_valid": true,
    "formatted_name": "Dr. Name",
    "likely_specialty": "Cardiology",
    "validation_notes": "notes here",
    "requires_verification": false
}}
"""
    
    try:
        result = llm.extract_json(prompt, temperature=0.1)
        
        result['success'] = True
        result['hcp_name'] = hcp_name  # Original name
        
        # Provide defaults
        if 'is_valid' not in result:
            result['is_valid'] = True
        if not result.get('formatted_name'):
            result['formatted_name'] = hcp_name.title()
        if not result.get('likely_specialty'):
            result['likely_specialty'] = 'General Practice'
        if not result.get('validation_notes'):
            result['validation_notes'] = 'Name validated'
        if 'requires_verification' not in result:
            result['requires_verification'] = False
        
        return result
        
    except Exception as e:
        print(f"❌ Error in validate_hcp tool: {e}")
        return {
            'success': False,
            'error': str(e),
            'hcp_name': hcp_name,
            'is_valid': None,
            'formatted_name': hcp_name,
            'likely_specialty': 'Unknown',
            'validation_notes': f'Error: {str(e)}',
            'requires_verification': True
        }
