import openai
import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

#openai.api_key='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'

# Function to call OpenAI API and process text
def call_openai_api():
    try:
        openai.api_key = os.environ.get('OPENAI_API_KEY', 'your-fallback-api-key')
        
        if not openai.api_key:
            return jsonify({"error": "API key not found"}), 500
        
        prompt_text = 'i am going to visit Berlin'
        role = "You will be my personal travel guide to provide me with a tailor made travel plan"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt_text},
                {"role": "assistant", "content": ""}
            ]
        )
        
        assistant_message = response['choices'][0]['message']['content']
        return assistant_message
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    processed_text = call_openai_api()
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=False)
