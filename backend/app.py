from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.is_json:
        data = request.get_json()
        text = data.get('text', '')

        # Ensure the input is not empty
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Call the sentiment analysis script
        try:
            result = subprocess.run(
                ['python', 'sentiment_analysis.py'],
                input=text, text=True, capture_output=True, check=True
            )

            # Log and check if any output was received
            if result.stdout:
                result_data = json.loads(result.stdout)
                return jsonify(result_data)
            else:
                return jsonify({'error': 'No output from sentiment analysis script'}), 500

        except subprocess.CalledProcessError as e:
            return jsonify({'error': f'Process error: {str(e)}'}), 500
        except json.JSONDecodeError:
            return jsonify({'error': 'Error parsing JSON from script output'}), 500
    else:
        return jsonify({'error': 'Invalid request format. JSON expected.'}), 400

if __name__ == '__main__':
    # Do not use Flask's built-in server for production
    # The following line is only for development
    app.run(host='0.0.0.0', port=3000, debug=False)
