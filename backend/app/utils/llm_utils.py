"""Groq LLM utilities and wrapper for API calls."""
import json
from groq import Groq
from app.config import get_settings

settings = get_settings()


class GroqLLMWrapper:
    """
    Wrapper for Groq API calls.
    
    Handles:
    - API authentication
    - Model selection
    - JSON parsing from LLM responses
    - Error handling
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Groq client.
        
        Args:
            api_key: Optional API key. If not provided, reads from settings.
        """
        self.api_key = api_key or settings.GROQ_API_KEY
        
        if not self.api_key or self.api_key == "your_groq_api_key_will_go_here":
            raise ValueError(
                "❌ GROQ_API_KEY not configured! "
                "Please add your API key to backend/.env file"
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model_primary = settings.GROQ_MODEL_PRIMARY
        self.model_backup = settings.GROQ_MODEL_BACKUP
        
        print(f"✅ Groq LLM initialized with model: {self.model_primary}")
    
    def call_llm(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        model: str = None
    ) -> str:
        """
        Call Groq LLM with a prompt.
        
        Args:
            prompt: The prompt to send to LLM
            temperature: Temperature for generation (0.1 = deterministic, 1.0 = creative)
            max_tokens: Maximum tokens to generate
            model: Model to use (defaults to primary model)
        
        Returns:
            LLM response as string
        
        Raises:
            Exception: If API call fails
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model or self.model_primary,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            result = response.choices[0].message.content
            return result
            
        except Exception as e:
            print(f"❌ Error calling Groq LLM: {e}")
            raise Exception(f"LLM API call failed: {str(e)}")
    
    def extract_json(self, prompt: str, temperature: float = 0.1) -> dict:
        """
        Call LLM and parse JSON response.
        
        Args:
            prompt: The prompt to send (should ask for JSON output)
            temperature: Temperature (lower = more deterministic, better for extraction)
        
        Returns:
            Parsed JSON as dictionary
        
        Raises:
            Exception: If JSON parsing fails
        """
        response = self.call_llm(prompt, temperature=temperature)
        
        try:
            # Try to parse directly
            return json.loads(response)
        except json.JSONDecodeError:
            # If response contains markdown code blocks, extract JSON from them
            try:
                # Look for JSON between ```json and ```
                if '```json' in response:
                    start = response.find('```json') + 7  # Length of ```json
                    end = response.find('```', start)
                    if end != -1:
                        json_str = response[start:end].strip()
                        return json.loads(json_str)
                
                # Look for JSON between ``` and ``` (without json marker)
                if '```' in response:
                    parts = response.split('```')
                    for part in parts:
                        part = part.strip()
                        if part.startswith('{') and part.endswith('}'):
                            try:
                                return json.loads(part)
                            except:
                                continue
                
                # Find JSON between first { and last }
                start = response.find('{')
                end = response.rfind('}') + 1
                
                if start != -1 and end > start:
                    json_str = response[start:end]
                    return json.loads(json_str)
                else:
                    raise Exception("No JSON found in response")
                    
            except Exception as e:
                print(f"❌ Failed to parse JSON from LLM response: {e}")
                print(f"Raw response: {response}")
                return {
                    "error": "Failed to parse JSON",
                    "raw_response": response
                }

    
    def test_connection(self) -> bool:
        """
        Test if Groq API connection is working.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.call_llm(
                "Say 'Hello' if you can hear me.",
                temperature=0.1,
                max_tokens=10
            )
            print(f"✅ Groq API test successful! Response: {response}")
            return True
        except Exception as e:
            print(f"❌ Groq API test failed: {e}")
            return False


# Global instance (will be used by tools)
llm = GroqLLMWrapper()
