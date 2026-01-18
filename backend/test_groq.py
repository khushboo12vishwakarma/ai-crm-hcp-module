"""Test script to verify Groq API connection."""
from app.utils.llm_utils import llm

print("\n" + "="*60)
print("🧪 Testing Groq API Connection...")
print("="*60 + "\n")

# Test 1: Simple connection test
print("Test 1: Connection Test")
success = llm.test_connection()

if success:
    print("\n✅ Connection test passed!\n")
else:
    print("\n❌ Connection test failed!\n")
    exit(1)

# Test 2: Extract JSON
print("Test 2: JSON Extraction Test")
prompt = """
Extract information from this text and return ONLY valid JSON (no markdown, no explanation):
"I met with Dr. Smith today to discuss Product X. The sentiment was positive."

Return JSON with fields: hcp_name, product, sentiment

IMPORTANT: Return ONLY the JSON object, nothing else.
"""

try:
    result = llm.extract_json(prompt, temperature=0.1)
    print(f"✅ JSON extraction successful!")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ JSON extraction failed: {e}")

print("\n" + "="*60)
print("✅ All tests completed!")
print("="*60 + "\n")
