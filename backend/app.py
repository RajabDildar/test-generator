from flask import Flask, request, jsonify
from flask_cors import CORS
from test_generator.analyzer import CodeAnalyzer
from test_generator.test_generator import TestGenerator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Verify API key is present
if not os.getenv('GROQ_API_KEY'):
    raise ValueError("GROQ_API_KEY not found in environment variables")

app = Flask(__name__)
CORS(app)

# Add a health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/generate-tests', methods=['POST'])
def generate_tests():
    data = request.json
    code = data.get('code')
    use_case = data.get('useCase')
    
    if not code or not use_case:
        return jsonify({'error': 'Code and use case are required'}), 400
    
    try:
        analyzer = CodeAnalyzer(code)
        code_analysis = analyzer.analyze()
        
        test_generator = TestGenerator(code_analysis, use_case)
        tests = test_generator.generate()
        
        return jsonify({
            'tests': tests,
            'message': 'Tests generated successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 