from .ai_service import AIService

class TestGenerator:
    def __init__(self, code_analysis, use_case):
        self.code_analysis = code_analysis
        self.use_case = use_case
        self.ai_service = AIService()

    def generate(self):
        prompt = self._create_prompt()
        test_code = self.ai_service.generate_tests(prompt)
        return test_code

    def _create_prompt(self):
        prompt = f"""Generate pytest test cases for the following code analysis:
        Code Analysis: {self.code_analysis}
        Use Case Description: {self.use_case}
        
        Requirements:
        1. Generate comprehensive test cases covering the main functionality
        2. Include edge cases and error scenarios
        3. Use pytest fixtures where appropriate
        4. Add clear test descriptions
        5. Follow testing best practices
        
        Please generate the complete test code:"""
        return prompt