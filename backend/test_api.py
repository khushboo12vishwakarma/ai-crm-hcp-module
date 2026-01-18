"""Test all API endpoints."""
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("\n" + "="*70)
print("🧪 Testing FastAPI Endpoints")
print("="*70 + "\n")

# Test 1: Chat endpoint (new interaction)
print("Test 1: POST /api/chat (New Interaction)")
print("-" * 70)
response = requests.post(
    f"{BASE_URL}/chat",
    json={
        "message": "Today I met with Dr. Johnson and discussed diabetes medication. Sentiment was positive, shared clinical data."
    }
)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Form data: {json.dumps(data['form_data'], indent=2)}")
print(f"Response: {data['chat_response'][:100]}...")
print(f"Status: {'✅ PASS' if response.status_code == 200 else '❌ FAIL'}\n")

# Save form data for creating interaction
form_data = data['form_data']

# Test 2: Create interaction
print("Test 2: POST /api/interactions (Create)")
print("-" * 70)
response = requests.post(
    f"{BASE_URL}/interactions",
    json={
        "hcp_name": form_data.get("hcp_name"),
        "date": form_data.get("date"),
        "sentiment": form_data.get("sentiment", "Neutral"),
        "materials_shared": form_data.get("materials_shared", []),
        "discussion_summary": form_data.get("discussion_summary"),
        "products_discussed": form_data.get("products_discussed", [])
    }
)
print(f"Status: {response.status_code}")
if response.status_code == 201:
    interaction = response.json()
    interaction_id = interaction['id']
    print(f"Created interaction ID: {interaction_id}")
    print(f"HCP: {interaction['hcp_name']}")
    print(f"Status: ✅ PASS\n")
else:
    print(f"Error: {response.text}")
    print(f"Status: ❌ FAIL\n")
    interaction_id = None

# Test 3: Get interaction
if interaction_id:
    print("Test 3: GET /api/interactions/{id} (Read)")
    print("-" * 70)
    response = requests.get(f"{BASE_URL}/interactions/{interaction_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Retrieved: {data['hcp_name']}")
        print(f"Status: ✅ PASS\n")
    else:
        print(f"Status: ❌ FAIL\n")

# Test 4: Chat with edit
if interaction_id:
    print("Test 4: POST /api/chat (Edit Existing)")
    print("-" * 70)
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": "Actually, the sentiment was negative",
            "interaction_id": interaction_id
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Updated sentiment: {data['form_data'].get('sentiment')}")
        print(f"Response: {data['chat_response'][:100]}...")
        print(f"Status: ✅ PASS\n")
    else:
        print(f"Status: ❌ FAIL\n")

# Test 5: Update interaction
if interaction_id:
    print("Test 5: PATCH /api/interactions/{id} (Update)")
    print("-" * 70)
    response = requests.patch(
        f"{BASE_URL}/interactions/{interaction_id}",
        json={"sentiment": "Positive"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Updated sentiment: {data['sentiment']}")
        print(f"Status: ✅ PASS\n")
    else:
        print(f"Status: ❌ FAIL\n")

# Test 6: List interactions
print("Test 6: GET /api/interactions (List)")
print("-" * 70)
response = requests.get(f"{BASE_URL}/interactions")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Total interactions: {len(data)}")
    if data:
        print(f"First interaction: {data[0]['hcp_name']}")
    print(f"Status: ✅ PASS\n")
else:
    print(f"Status: ❌ FAIL\n")

print("="*70)
print("✅ All API Tests Completed!")
print("="*70 + "\n")
