"""
Tool #4: Extract Insights
AI-powered analysis of interaction opportunities and concerns.
"""
from app.utils.llm_utils import llm
import json


def extract_insights(interaction_data: dict) -> dict:
    """
    Extract key insights from an HCP interaction.
    
    Analyzes the interaction to identify sales opportunities,
    concerns, and recommended next actions.
    
    Args:
        interaction_data: The interaction dictionary
    
    Example Input:
        {
            'hcp_name': 'Dr. Smith',
            'sentiment': 'Positive',
            'discussion_summary': 'Discussed new diabetes medication efficacy',
            'products_discussed': ['GlucoControl']
        }
    
    Returns:
        {
            'opportunities': ['High interest in diabetes portfolio', 'Potential for pilot program'],
            'concerns': ['Asked about side effects', 'Pricing concerns'],
            'recommended_actions': ['Send clinical trial data', 'Arrange specialist call'],
            'priority_level': 'High',
            'success': True
        }
    """
    
    # Extract key fields for analysis
    hcp_name = interaction_data.get('hcp_name', 'Unknown HCP')
    sentiment = interaction_data.get('sentiment', 'Neutral')
    discussion = interaction_data.get('discussion_summary', 'No discussion summary')
    products = interaction_data.get('products_discussed', [])
    materials = interaction_data.get('materials_shared', [])
    
    prompt = f"""You are a medical sales analyst. Analyze this HCP interaction and extract strategic insights.

Interaction Details:
- HCP: {hcp_name}
- Sentiment: {sentiment}
- Discussion: {discussion}
- Products Discussed: {', '.join(products) if products else 'None'}
- Materials Shared: {', '.join(materials) if materials else 'None'}

Analyze this interaction and provide:

1. opportunities: 2-3 sales opportunities or positive signals identified
2. concerns: Any concerns, objections, or negative signals (or empty array if none)
3. recommended_actions: 2-3 specific next actions to move the opportunity forward
4. priority_level: Overall priority ("High", "Medium", or "Low") based on opportunity potential

Consider:
- Sentiment indicates interest level
- Materials shared show engagement depth
- Discussion topics reveal needs

Return ONLY valid JSON (no markdown):
{{
    "opportunities": ["opportunity1", "opportunity2"],
    "concerns": ["concern1"],
    "recommended_actions": ["action1", "action2"],
    "priority_level": "High|Medium|Low"
}}
"""
    
    try:
        result = llm.extract_json(prompt, temperature=0.3)
        
        result['success'] = True
        
        # Provide defaults
        if not result.get('opportunities'):
            result['opportunities'] = []
        if not result.get('concerns'):
            result['concerns'] = []
        if not result.get('recommended_actions'):
            result['recommended_actions'] = ['Follow up with HCP']
        if not result.get('priority_level'):
            # Auto-determine priority from sentiment
            if sentiment == 'Positive':
                result['priority_level'] = 'High'
            elif sentiment == 'Negative':
                result['priority_level'] = 'Low'
            else:
                result['priority_level'] = 'Medium'
        
        return result
        
    except Exception as e:
        print(f"❌ Error in extract_insights tool: {e}")
        return {
            'success': False,
            'error': str(e),
            'opportunities': [],
            'concerns': [],
            'recommended_actions': [],
            'priority_level': 'Medium'
        }
