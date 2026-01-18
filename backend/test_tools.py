"""Test script to verify all 5 LangGraph tools work correctly."""
from app.agents.tools.log_interaction import log_interaction
from app.agents.tools.edit_interaction import edit_interaction
from app.agents.tools.schedule_followup import schedule_followup
from app.agents.tools.extract_insights import extract_insights
from app.agents.tools.validate_hcp import validate_hcp
import json

print("\n" + "="*70)
print("🧪 Testing All 5 LangGraph Tools")
print("="*70 + "\n")

# Test 1: Log Interaction
print("Test 1: Log Interaction Tool")
print("-" * 70)
message = "Today I met with Dr. Smith and discussed product X efficiency. The sentiment was positive, and I shared the brochures."
result = log_interaction(message)
print(f"Input: {message}")
print(f"Output: {json.dumps(result, indent=2)}")
print(f"Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
print()

# Test 2: Edit Interaction
print("Test 2: Edit Interaction Tool")
print("-" * 70)
current_data = {
    'hcp_name': 'Dr. Smith',
    'date': '2026-01-18',
    'sentiment': 'Positive',
    'materials_shared': ['brochures'],
    'discussion_summary': 'Discussed product X',
    'products_discussed': ['product X']
}
edit_message = "Sorry, the name was actually Dr. John, and the sentiment was negative."
result = edit_interaction(current_data, edit_message)
print(f"Current data: {json.dumps(current_data, indent=2)}")
print(f"Edit request: {edit_message}")
print(f"Updated data: {json.dumps(result, indent=2)}")
print(f"Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
print(f"Changed fields: hcp_name={result.get('hcp_name')}, sentiment={result.get('sentiment')}")
print()

# Test 3: Schedule Follow-up
print("Test 3: Schedule Follow-up Tool")
print("-" * 70)
followup_message = "Schedule a follow-up with Dr. Patel next week to discuss clinical trial results"
result = schedule_followup("Dr. Patel", followup_message)
print(f"Input: {followup_message}")
print(f"Output: {json.dumps(result, indent=2)}")
print(f"Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
print()

# Test 4: Extract Insights
print("Test 4: Extract Insights Tool")
print("-" * 70)
interaction = {
    'hcp_name': 'Dr. Williams',
    'sentiment': 'Positive',
    'discussion_summary': 'Very interested in new diabetes medication, asked about pricing and clinical data',
    'products_discussed': ['GlucoControl'],
    'materials_shared': ['brochures', 'clinical studies']
}
result = extract_insights(interaction)
print(f"Interaction: {json.dumps(interaction, indent=2)}")
print(f"Insights: {json.dumps(result, indent=2)}")
print(f"Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
print()

# Test 5: Validate HCP
print("Test 5: Validate HCP Tool")
print("-" * 70)
hcp_names = ["dr smith", "Dr. John Patel", "Prof. Williams"]
for name in hcp_names:
    result = validate_hcp(name)
    print(f"Input: '{name}'")
    print(f"  Valid: {result.get('is_valid')}")
    print(f"  Formatted: {result.get('formatted_name')}")
    print(f"  Specialty: {result.get('likely_specialty')}")
    print(f"  Status: {'✅ PASS' if result.get('success') else '❌ FAIL'}")
    print()

print("="*70)
print("✅ All Tool Tests Completed!")
print("="*70 + "\n")
