
import openai
import requests
import json
import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Function to call OpenAI API and process text
def call_openai_api():
    # Replace 'your-api-key' with your actual API key, ideally from an environment variable
    #openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    openai.api_key='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'

    if not openai.api_key:
        return jsonify({"error": "API key not found"}), 500

    # The prompt you want the model to complete
    prompt_text = 'i am going to visit Berlin'
    role = "You will be my personal travel guide to provide me with a tailor made travel plan"
    
    # The model you want to use, eg. 'text-davinci-003' for GPT-3
    
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
    

@app.route('/webhook', methods=['POST'])
def webhook():
    processed_text = call_openai_api()
    return jsonify({'processed_text': processed_text})
    #return processed_text

if __name__ == '__main__':
    app.run(debug=True)

