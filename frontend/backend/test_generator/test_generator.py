from .ai_service import AIService

class TestGenerator:
    def __init__(self, code_analysis, use_case):
        self.code_analysis = code_analysis
        self.use_case = use_case
        self.ai_service = AIService()

    def generate(self):
        # Now passing code and intent separately
        test_code = self.ai_service.generate_tests(self.code_analysis, self.use_case)
        return test_code
