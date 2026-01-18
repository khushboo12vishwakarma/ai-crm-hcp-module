"""Test the complete LangGraph HCP Agent."""
from app.agents.hcp_agent import agent
import json

print("\n" + "="*70)
print("🧪 Testing LangGraph HCP Agent")
print("="*70 + "\n")

# Test 1: Log new interaction
print("Test 1: Log New Interaction")
print("-" * 70)
result = agent.process(
    user_input="Today I met with Dr. Smith and discussed product X efficiency. The sentiment was positive, and I shared the brochures.",
    current_form_data=None
)
print(f"Intent detected: {result['intent']}")
print(f"Form data: {json.dumps(result['form_data'], indent=2)}")
print(f"Response: {result['chat_response']}")
print(f"Status: {'✅ PASS' if result['success'] else '❌ FAIL'}\n")

# Save data for next test
saved_data = result['form_data']

# Test 2: Edit interaction
print("Test 2: Edit Existing Interaction")
print("-" * 70)
result = agent.process(
    user_input="Actually, the sentiment was negative and the name was Dr. John Smith.",
    current_form_data=saved_data
)
print(f"Intent detected: {result['intent']}")
print(f"Updated HCP name: {result['form_data'].get('hcp_name')}")
print(f"Updated sentiment: {result['form_data'].get('sentiment')}")
print(f"Response: {result['chat_response']}")
print(f"Status: {'✅ PASS' if result['success'] else '❌ FAIL'}\n")

# Test 3: Schedule follow-up
print("Test 3: Schedule Follow-up")
print("-" * 70)
result = agent.process(
    user_input="Schedule a follow-up with this doctor next week to discuss trial results.",
    current_form_data=saved_data
)
print(f"Intent detected: {result['intent']}")
print(f"Follow-up date: {result['form_data'].get('follow_up_date')}")
print(f"Response: {result['chat_response']}")
print(f"Status: {'✅ PASS' if result['success'] else '❌ FAIL'}\n")

# Test 4: Extract insights
print("Test 4: Extract Insights")
print("-" * 70)
result = agent.process(
    user_input="What are the opportunities from this interaction?",
    current_form_data=saved_data
)
print(f"Intent detected: {result['intent']}")
print(f"Response: {result['chat_response']}")
print(f"Status: {'✅ PASS' if result['success'] else '❌ FAIL'}\n")

# Test 5: Validate HCP
print("Test 5: Validate HCP")
print("-" * 70)
result = agent.process(
    user_input="Verify the HCP information is correct.",
    current_form_data=saved_data
)
print(f"Intent detected: {result['intent']}")
print(f"Response: {result['chat_response']}")
print(f"Status: {'✅ PASS' if result['success'] else '❌ FAIL'}\n")

print("="*70)
print("✅ All Agent Tests Completed!")
print("="*70 + "\n")
