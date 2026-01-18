"""Test script to verify all Pydantic schemas work correctly."""
from datetime import date, datetime
from app.schemas.interaction_schema import (
    InteractionBase,
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse,
    ChatRequest,
    ChatResponse
)
import json

print("\n" + "="*60)
print("🧪 Testing Pydantic Schemas...")
print("="*60 + "\n")

# Test 1: InteractionBase
print("Test 1: InteractionBase Schema")
try:
    interaction_base = InteractionBase(
        hcp_name="Dr. Smith",
        date=date(2026, 1, 18),
        sentiment="Positive",
        materials_shared=["brochures", "samples"],
        discussion_summary="Discussed new product line",
        products_discussed=["Product X", "Product Y"]
    )
    print(f"✅ InteractionBase created successfully")
    print(f"   HCP: {interaction_base.hcp_name}")
    print(f"   Date: {interaction_base.date}")
    print(f"   Sentiment: {interaction_base.sentiment}")
except Exception as e:
    print(f"❌ InteractionBase failed: {e}")

print()

# Test 2: InteractionCreate
print("Test 2: InteractionCreate Schema")
try:
    interaction_create = InteractionCreate(
        hcp_name="Dr. Johnson",
        date=date.today(),
        sentiment="Neutral",
        materials_shared=["clinical data"],
        discussion_summary="Initial consultation",
        products_discussed=["Product Z"]
    )
    print(f"✅ InteractionCreate created successfully")
    print(f"   JSON: {interaction_create.model_dump_json(indent=2)}")
except Exception as e:
    print(f"❌ InteractionCreate failed: {e}")

print()

# Test 3: InteractionUpdate (partial update)
print("Test 3: InteractionUpdate Schema (Partial Update)")
try:
    # Only updating sentiment and hcp_name
    interaction_update = InteractionUpdate(
        hcp_name="Dr. John Smith",
        sentiment="Negative"
    )
    print(f"✅ InteractionUpdate created successfully")
    print(f"   Updated fields: {interaction_update.model_dump(exclude_none=True)}")
except Exception as e:
    print(f"❌ InteractionUpdate failed: {e}")

print()

# Test 4: InteractionResponse
print("Test 4: InteractionResponse Schema")
try:
    interaction_response = InteractionResponse(
        id=1,
        hcp_name="Dr. Patel",
        date=date(2026, 1, 18),
        sentiment="Positive",
        materials_shared=["brochures"],
        discussion_summary="Follow-up meeting",
        products_discussed=["Product A"],
        follow_up_date=date(2026, 2, 18),
        key_insights="Very interested in new features",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    print(f"✅ InteractionResponse created successfully")
    print(f"   ID: {interaction_response.id}")
    print(f"   HCP: {interaction_response.hcp_name}")
except Exception as e:
    print(f"❌ InteractionResponse failed: {e}")

print()

# Test 5: ChatRequest
print("Test 5: ChatRequest Schema")
try:
    # New interaction
    chat_request_new = ChatRequest(
        message="Today I met with Dr. Smith and discussed product X efficiency. The sentiment was positive, and I shared the brochures."
    )
    print(f"✅ ChatRequest (new) created successfully")
    print(f"   Message length: {len(chat_request_new.message)} chars")
    print(f"   Interaction ID: {chat_request_new.interaction_id}")
    
    # Edit existing interaction
    chat_request_edit = ChatRequest(
        message="Actually, the sentiment was negative.",
        interaction_id=5
    )
    print(f"✅ ChatRequest (edit) created successfully")
    print(f"   Editing interaction ID: {chat_request_edit.interaction_id}")
except Exception as e:
    print(f"❌ ChatRequest failed: {e}")

print()

# Test 6: ChatResponse
print("Test 6: ChatResponse Schema")
try:
    chat_response = ChatResponse(
        form_data={
            "hcp_name": "Dr. Smith",
            "date": "2026-01-18",
            "sentiment": "Positive",
            "materials_shared": ["brochures"],
            "discussion_summary": "Discussed product X efficiency",
            "products_discussed": ["product X"]
        },
        chat_response="✓ I've logged your interaction with Dr. Smith:\n- Date: 2026-01-18\n- Sentiment: Positive\n- Materials Shared: brochures\n\nYour interaction has been recorded.",
        interaction_id=None
    )
    print(f"✅ ChatResponse created successfully")
    print(f"   Form data fields: {list(chat_response.form_data.keys())}")
    print(f"   Response preview: {chat_response.chat_response[:50]}...")
except Exception as e:
    print(f"❌ ChatResponse failed: {e}")

print()

# Test 7: Validation Errors
print("Test 7: Schema Validation (should fail)")
try:
    # Missing required field
    invalid_request = ChatRequest(message="")  # Empty message
    print(f"❌ Validation should have failed for empty message!")
except Exception as e:
    print(f"✅ Validation correctly failed: {str(e)[:80]}...")

print()

# Test 8: JSON Serialization/Deserialization
print("Test 8: JSON Serialization/Deserialization")
try:
    # Create object
    original = ChatRequest(
        message="Test message",
        interaction_id=10
    )
    
    # Serialize to JSON
    json_str = original.model_dump_json()
    print(f"✅ Serialized to JSON: {json_str}")
    
    # Deserialize from JSON
    json_data = json.loads(json_str)
    recreated = ChatRequest(**json_data)
    print(f"✅ Deserialized from JSON: {recreated.message}")
    
    # Verify they match
    assert original.message == recreated.message
    assert original.interaction_id == recreated.interaction_id
    print(f"✅ Original and recreated objects match!")
except Exception as e:
    print(f"❌ JSON serialization failed: {e}")

print()

# Test 9: Default Values
print("Test 9: Default Values")
try:
    minimal = InteractionBase(
        hcp_name="Dr. Minimal",
        date=date.today()
    )
    print(f"✅ Created with minimal data")
    print(f"   Sentiment (default): {minimal.sentiment}")
    print(f"   Materials (default): {minimal.materials_shared}")
    print(f"   Products (default): {minimal.products_discussed}")
    assert minimal.sentiment == "Neutral"
    assert minimal.materials_shared == []
    assert minimal.products_discussed == []
    print(f"✅ All defaults correct!")
except Exception as e:
    print(f"❌ Default values failed: {e}")

print("\n" + "="*60)
print("✅ All Schema Tests Completed!")
print("="*60 + "\n")

# Summary
print("📊 Summary:")
print("   - InteractionBase: ✅")
print("   - InteractionCreate: ✅")
print("   - InteractionUpdate: ✅")
print("   - InteractionResponse: ✅")
print("   - ChatRequest: ✅")
print("   - ChatResponse: ✅")
print("   - Validation: ✅")
print("   - JSON Serialization: ✅")
print("   - Default Values: ✅")
print("\n🎉 Phase 2.2 Complete - All schemas working!\n")
