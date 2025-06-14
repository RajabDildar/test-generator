import os
import requests
from dotenv import load_dotenv

class AIService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Using Groq API endpoint for LLaMA 3.3 70B
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_tests(self, code: str, intent: str) -> str:
        try:
            full_prompt = (
                f"Here is a Python module:\n\n{code}\n\n"
                f"Based on the following user intent:\n{intent}\n\n"
                f"Write complete test cases using pytest or unittest. "
                f"Respond with ONLY the code, no explanations."
            )

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": "You are a senior Python developer who writes clean, professional test cases using pytest. Output only code."},
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 800
                }
            )

            result = response.json()
            if response.status_code != 200 or 'choices' not in result:
                raise Exception(f"API Error: {result.get('error', 'Unknown error')}")

            content = result['choices'][0]['message']['content']
            code_start = content.find('```python')
            code_end = content.rfind('```')

            if code_start == -1:
                code_start = content.find('```')  # fallback if no language tag
            if code_start != -1 and code_end != -1:
                return content[code_start + 8:code_end].strip()
            return content.strip()

        except Exception as e:
            raise Exception(f'Failed to generate tests: {str(e)}')