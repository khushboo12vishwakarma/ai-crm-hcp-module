"""
LangGraph Agent for HCP Interaction Management
Orchestrates 5 tools: log, edit, schedule, insights, validate
"""
from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph, END
from app.utils.llm_utils import llm
from app.agents.tools.log_interaction import log_interaction
from app.agents.tools.edit_interaction import edit_interaction
from app.agents.tools.schedule_followup import schedule_followup
from app.agents.tools.extract_insights import extract_insights
from app.agents.tools.validate_hcp import validate_hcp
import json


class AgentState(TypedDict):
    """State that flows through the graph."""
    user_input: str
    current_form_data: dict
    form_data: dict
    tool_results: dict
    intent: str
    chat_response: str
    error: str


class HCPAgent:
    """
    LangGraph agent that manages HCP interactions.
    
    Flow:
    1. User input → Router (classifies intent)
    2. Router → One of 5 tool nodes
    3. Tool node → Updates form_data
    4. Formatter → Creates friendly response
    5. Return form_data + chat_response
    """
    
    def __init__(self):
        """Initialize the agent and build the graph."""
        self.graph = self._build_graph()
        print("✅ HCP Agent initialized with 5 tools")
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph."""
        
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", self._router_node)
        workflow.add_node("log_interaction", self._log_interaction_node)
        workflow.add_node("edit_interaction", self._edit_interaction_node)
        workflow.add_node("schedule_followup", self._schedule_followup_node)
        workflow.add_node("extract_insights", self._extract_insights_node)
        workflow.add_node("validate_hcp", self._validate_hcp_node)
        workflow.add_node("formatter", self._formatter_node)
        
        # Set entry point
        workflow.set_entry_point("router")
        
        # Add conditional edges from router to tool nodes
        workflow.add_conditional_edges(
            "router",
            self._route_to_tool,
            {
                "log": "log_interaction",
                "edit": "edit_interaction",
                "schedule": "schedule_followup",
                "insights": "extract_insights",
                "validate": "validate_hcp",
                "error": "formatter"
            }
        )
        
        # All tool nodes go to formatter
        workflow.add_edge("log_interaction", "formatter")
        workflow.add_edge("edit_interaction", "formatter")
        workflow.add_edge("schedule_followup", "formatter")
        workflow.add_edge("extract_insights", "formatter")
        workflow.add_edge("validate_hcp", "formatter")
        
        # Formatter ends the workflow
        workflow.add_edge("formatter", END)
        
        return workflow.compile()
    
    def _router_node(self, state: AgentState) -> AgentState:
        """
        Router node: Classifies user intent.
        
        Decides which tool to use based on user's message.
        """
        user_input = state["user_input"]
        has_existing_data = state.get("current_form_data") and state["current_form_data"].get("hcp_name")
        
        prompt = f"""You are an intent classifier for a medical sales CRM system.

User message: "{user_input}"

Existing data present: {"Yes" if has_existing_data else "No"}

Classify the user's intent into ONE of these categories:

1. "log" - User wants to LOG a new interaction
   - Examples: "I met with Dr. Smith", "Today's meeting was positive", "Just had a call with..."
   - Use when: Creating NEW interaction from scratch

2. "edit" - User wants to EDIT/CORRECT existing data
   - Examples: "Actually the name was...", "Change sentiment to...", "Sorry, I meant..."
   - Use when: Correcting or updating previously entered information
   - IMPORTANT: Only use if existing data is present

3. "schedule" - User wants to SCHEDULE a follow-up
   - Examples: "Schedule follow-up next week", "Book a meeting with...", "Plan next visit..."
   - Use when: Explicitly scheduling future meetings

4. "insights" - User wants ANALYSIS/INSIGHTS
   - Examples: "What are the opportunities?", "Analyze this interaction", "Give me insights..."
   - Use when: Requesting AI analysis of interaction

5. "validate" - User wants to VALIDATE HCP information
   - Examples: "Is Dr. Smith's name correct?", "Verify this doctor", "Check HCP details..."
   - Use when: Validating or checking HCP information

Return ONLY the intent name, nothing else: log, edit, schedule, insights, or validate
"""
        
        try:
            intent = llm.call_llm(prompt, temperature=0.1, max_tokens=20).strip().lower()
            
            # Normalize response
            if "log" in intent:
                intent = "log"
            elif "edit" in intent or "update" in intent or "change" in intent:
                intent = "edit"
            elif "schedule" in intent or "follow" in intent:
                intent = "schedule"
            elif "insight" in intent or "analyz" in intent or "opportun" in intent:
                intent = "insights"
            elif "validat" in intent or "verify" in intent or "check" in intent:
                intent = "validate"
            else:
                # Default to log for new interactions, edit if data exists
                intent = "edit" if has_existing_data else "log"
            
            state["intent"] = intent
            print(f"🔀 Router: Classified intent as '{intent}'")
            
        except Exception as e:
            print(f"❌ Router error: {e}")
            state["intent"] = "error"
            state["error"] = str(e)
        
        return state
    
    def _route_to_tool(self, state: AgentState) -> str:
        """Return the next node based on intent."""
        return state.get("intent", "log")
    
    def _log_interaction_node(self, state: AgentState) -> AgentState:
        """Log new interaction using Tool #1."""
        print("🔧 Running: log_interaction tool")
        
        try:
            result = log_interaction(state["user_input"])
            state["tool_results"] = result
            
            if result.get("success"):
                state["form_data"] = {
                    "hcp_name": result.get("hcp_name"),
                    "date": result.get("date"),
                    "sentiment": result.get("sentiment"),
                    "materials_shared": result.get("materials_shared", []),
                    "discussion_summary": result.get("discussion_summary"),
                    "products_discussed": result.get("products_discussed", []),
                    "follow_up_date": result.get("follow_up_date"),
                    "key_insights": result.get("key_insights")
                }
            else:
                state["error"] = result.get("error", "Unknown error")
                
        except Exception as e:
            print(f"❌ Error in log_interaction_node: {e}")
            state["error"] = str(e)
        
        return state
    
    def _edit_interaction_node(self, state: AgentState) -> AgentState:
        """Edit existing interaction using Tool #2."""
        print("🔧 Running: edit_interaction tool")
        
        try:
            current_data = state.get("current_form_data", {})
            result = edit_interaction(current_data, state["user_input"])
            state["tool_results"] = result
            
            if result.get("success"):
                state["form_data"] = result
            else:
                state["error"] = result.get("error", "Unknown error")
                state["form_data"] = current_data  # Keep original on error
                
        except Exception as e:
            print(f"❌ Error in edit_interaction_node: {e}")
            state["error"] = str(e)
            state["form_data"] = state.get("current_form_data", {})
        
        return state
    
    def _schedule_followup_node(self, state: AgentState) -> AgentState:
        """Schedule follow-up using Tool #3."""
        print("🔧 Running: schedule_followup tool")
        
        try:
            # Get HCP name from current data or extract from message
            hcp_name = state.get("current_form_data", {}).get("hcp_name", "HCP")
            result = schedule_followup(hcp_name, state["user_input"])
            state["tool_results"] = result
            
            if result.get("success"):
                # Merge with existing data
                form_data = state.get("current_form_data", {}).copy()
                form_data["follow_up_date"] = result.get("follow_up_date")
                
                # Store talking points in key_insights
                talking_points = result.get("talking_points", [])
                prep_notes = result.get("preparation_notes", "")
                insights = f"Follow-up planned:\n- {chr(10).join(talking_points)}\n\nPreparation: {prep_notes}"
                form_data["key_insights"] = insights
                
                state["form_data"] = form_data
            else:
                state["error"] = result.get("error", "Unknown error")
                
        except Exception as e:
            print(f"❌ Error in schedule_followup_node: {e}")
            state["error"] = str(e)
        
        return state
    
    def _extract_insights_node(self, state: AgentState) -> AgentState:
        """Extract insights using Tool #4."""
        print("🔧 Running: extract_insights tool")
        
        try:
            interaction_data = state.get("current_form_data", {})
            result = extract_insights(interaction_data)
            state["tool_results"] = result
            
            if result.get("success"):
                # Format insights as text
                opportunities = result.get("opportunities", [])
                concerns = result.get("concerns", [])
                actions = result.get("recommended_actions", [])
                priority = result.get("priority_level", 'Medium')
                
                insights = f"Priority: {priority}\n\n"
                if opportunities:
                    insights += f"Opportunities:\n- {chr(10).join(['- ' + o for o in opportunities])}\n\n"
                if concerns:
                    insights += f"Concerns:\n- {chr(10).join(['- ' + c for c in concerns])}\n\n"
                if actions:
                    insights += f"Recommended Actions:\n- {chr(10).join(['- ' + a for a in actions])}"
                
                # Merge with existing data
                form_data = state.get("current_form_data", {}).copy()
                form_data["key_insights"] = insights
                state["form_data"] = form_data
            else:
                state["error"] = result.get("error", "Unknown error")
                
        except Exception as e:
            print(f"❌ Error in extract_insights_node: {e}")
            state["error"] = str(e)
        
        return state
    
    def _validate_hcp_node(self, state: AgentState) -> AgentState:
        """Validate HCP using Tool #5."""
        print("🔧 Running: validate_hcp tool")
        
        try:
            hcp_name = state.get("current_form_data", {}).get("hcp_name", "")
            if not hcp_name:
                # Try to extract from user input
                hcp_name = state["user_input"]
            
            result = validate_hcp(hcp_name)
            state["tool_results"] = result
            
            if result.get("success") and result.get("is_valid"):
                # Update HCP name with formatted version
                form_data = state.get("current_form_data", {}).copy()
                form_data["hcp_name"] = result.get("formatted_name")
                
                # Add validation info to insights
                specialty = result.get("likely_specialty", 'Unknown')
                notes = result.get("validation_notes", '')
                insights = f"HCP Validation:\n- Specialty: {specialty}\n- Notes: {notes}"
                form_data["key_insights"] = insights
                
                state["form_data"] = form_data
            else:
                state["error"] = result.get("error", "Validation failed")
                
        except Exception as e:
            print(f"❌ Error in validate_hcp_node: {e}")
            state["error"] = str(e)
        
        return state
    
    def _formatter_node(self, state: AgentState) -> AgentState:
        """Format the final response for the user."""
        print("💬 Formatting response...")
        
        intent = state.get("intent", "unknown")
        error = state.get("error")
        tool_results = state.get("tool_results", {})
        form_data = state.get("form_data", {})
        
        if error:
            state["chat_response"] = f"❌ Sorry, I encountered an error: {error}"
            return state
        
        # Build friendly response based on intent
        if intent == "log":
            hcp_name = form_data.get("hcp_name", "the HCP")
            sentiment = form_data.get("sentiment", "neutral")
            response = f"✓ I've logged your interaction with {hcp_name}.\n\n"
            response += f"📋 Details captured:\n"
            response += f"- Date: {form_data.get('date', 'N/A')}\n"
            response += f"- Sentiment: {sentiment}\n"
            if form_data.get("materials_shared"):
                response += f"- Materials: {', '.join(form_data['materials_shared'])}\n"
            if form_data.get("products_discussed"):
                response += f"- Products: {', '.join(form_data['products_discussed'])}\n"
            response += f"\nYour interaction has been recorded successfully!"
        
        elif intent == "edit":
            response = "✓ I've updated the interaction with your changes.\n\n"
            response += f"📝 Current data:\n"
            response += f"- HCP: {form_data.get('hcp_name', 'N/A')}\n"
            response += f"- Sentiment: {form_data.get('sentiment', 'N/A')}\n"
            response += f"The form has been updated."
        
        elif intent == "schedule":
            follow_up = tool_results.get("follow_up_date", "soon")
            talking_points = tool_results.get("talking_points", [])
            response = f"✓ Follow-up scheduled for {follow_up}!\n\n"
            if talking_points:
                response += f"📅 Talking points:\n"
                for point in talking_points:
                    response += f"  • {point}\n"
            prep = tool_results.get("preparation_notes")
            if prep:
                response += f"\n📌 Preparation: {prep}"
        
        elif intent == "insights":
            priority = tool_results.get("priority_level", 'Medium')
            opportunities = tool_results.get("opportunities", [])
            actions = tool_results.get("recommended_actions", [])
            
            response = f"🔍 Analysis complete! Priority: {priority}\n\n"
            if opportunities:
                response += f"✨ Opportunities:\n"
                for opp in opportunities:
                    response += f"  • {opp}\n"
            if actions:
                response += f"\n🎯 Recommended actions:\n"
                for action in actions:
                    response += f"  • {action}\n"
        
        elif intent == "validate":
            formatted = tool_results.get("formatted_name", "Unknown")
            specialty = tool_results.get("likely_specialty", "Unknown")
            response = f"✓ HCP information validated!\n\n"
            response += f"👨‍⚕️ Name: {formatted}\n"
            response += f"🏥 Likely specialty: {specialty}\n"
            if tool_results.get("requires_verification"):
                response += f"\n⚠️ Manual verification recommended."
        
        else:
            response = "✓ Request processed successfully!"
        
        state["chat_response"] = response
        return state
    
    def process(self, user_input: str, current_form_data: dict = None) -> dict:
        """
        Main entry point for processing user messages.
        
        Args:
            user_input: User's natural language message
            current_form_data: Current form data (for edits) or None (for new)
        
        Returns:
            {
                'form_data': {...},  # Updated form data
                'chat_response': '...',  # Friendly response
                'intent': '...',  # Detected intent
                'success': True/False
            }
        """
        print(f"\n{'='*70}")
        print(f"🤖 HCP Agent Processing Request")
        print(f"{'='*70}")
        print(f"Input: {user_input}")
        print(f"Has existing data: {bool(current_form_data and current_form_data.get('hcp_name'))}")
        
        # Initialize state
        initial_state: AgentState = {
            "user_input": user_input,
            "current_form_data": current_form_data or {},
            "form_data": {},
            "tool_results": {},
            "intent": "",
            "chat_response": "",
            "error": ""
        }
        
        try:
            # Run the graph
            final_state = self.graph.invoke(initial_state)
            
            print(f"\n✅ Processing complete!")
            print(f"Intent: {final_state.get('intent', 'unknown')}")
            print(f"{'='*70}\n")
            
            return {
                "form_data": final_state.get("form_data", {}),
                "chat_response": final_state.get("chat_response", ""),
                "intent": final_state.get("intent", ""),
                "success": not bool(final_state.get("error"))
            }
            
        except Exception as e:
            print(f"❌ Agent error: {e}")
            return {
                "form_data": current_form_data or {},
                "chat_response": f"❌ Sorry, I encountered an error: {str(e)}",
                "intent": "error",
                "success": False
            }


# Global agent instance
agent = HCPAgent()
