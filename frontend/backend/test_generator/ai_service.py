import os
import requests
from dotenv import load_dotenv

class AIService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
        
        # Using Hugging Face's API endpoint for text generation
        self.api_url = "https://api-inference.huggingface.co/models/bigcode/starcoder"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate_tests(self, prompt):
        try:
            # Prepare the system message and user prompt
            full_prompt = f"""You are a Python testing expert. Generate comprehensive test cases using pytest.

Generate test cases for the following:
{prompt}

Respond with only the test code, no explanations:"""

            # Make request to Hugging Face API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "inputs": full_prompt,
                    "parameters": {
                        "max_new_tokens": 1000,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "do_sample": True,
                        "return_full_text": False
                    }
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status code: {response.status_code}")

            # Extract the generated test code from the response
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Clean up the response to extract only the code part
                code_start = generated_text.find('```python')
                code_end = generated_text.rfind('```')
                if code_start != -1 and code_end != -1:
                    return generated_text[code_start + 8:code_end].strip()
                return generated_text.strip()
            
            raise Exception("No valid response from the API")
            
        except Exception as e:
            raise Exception(f'Failed to generate tests: {str(e)}')