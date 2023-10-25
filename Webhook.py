import openai
import os
from flask import Flask, request, jsonify
import sys

# Initialize Flask app
app = Flask(__name__)

# Function to handle streaming from OpenAI API
def handle_stream(response):
    collected_message = ""
    for chunk in response:
        delta = chunk.get('choices', [{}])[0].get('delta', {})
        content = delta.get('content', None)

        if content is not None:
            print(content, end="")
            sys.stdout.flush()
            collected_message += content
    return collected_message

# Function to call OpenAI API and process text
def call_openai_api():
    try:
        openai.api_key = os.environ.get('OPENAI_API_KEY', 'your-fallback-api-key')
        
        if not openai.api_key:
            return jsonify({"error": "API key not found"}), 500
        
        prompt_text = 'Please just formulate a long text that takes you more than 1 min to generate'
        role = "You will help me test the limits of the Azure timeout"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt_text},
                {"role": "assistant", "content": ""}
            ],
            stream=True  # Turn on streaming
        )
        
        assistant_message = handle_stream(response)
        
        print("\nComplete Message:")
        print(assistant_message)
        
        return assistant_message
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/Webhook', methods=['POST'])
def webhook():
    processed_text = call_openai_api()
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=False)
