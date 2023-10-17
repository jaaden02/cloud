
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
    openai.api_key = os.getenv('OPENAI_API_KEY', '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')
    
    # The prompt you want the model to complete
    prompt_text = 'i am going to visit Berlin'
    role = "You will be my personal travel guide to provide me with a tailor made travel plan"
    
    # The model you want to use, eg. 'text-davinci-003' for GPT-3
    '''
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": role},
        {"role": "user", "content": prompt_text},
        {"role": "assistant", "content": ""}
      ]
    )
    '''
    

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",    "content": "You are my personal tour guide, responsible to create an individual, tailor made travel plan that is in line with my trip outline and personal preferences."},

            {"role": "assistant", "content": '''An example day with one activity can look like this, with empty text: \
                Day 1: “Weekday”\
                \
                10:00 AM - 'Description of the activity.' \
                - Cost: “Cost breakdown”\
                - Time: “Time estimate”\
                - Navigation: “Navigation details”\
                - Insider Tip (if applicable): “Insider Tip”\
                - Additional Links'''},
            {"role": "user",      "content": "I am visiting Berlin for the upcoming weekend. I've been to the city many times, so I'm familiar with the main attractions. I'm looking for something off the beaten path, something that only locals would know about"},
            {"role": "user",      "content": "I'm a 21-year-old male, a fan of independent films, techno music, vintage items, small cafés, and old rustic bars. I'm active, not vegetarian, and on a student budget. I'll be staying near S Warschauer Brücke and am comfortable using public transit."},
            {"role": "assistant", "content": "If you are not sure of the exact navigation, do not provide any, give an address instead. Make sure not to be wrong, especially with navigation. If you are not sure about costs, use estimates. Make sure to clearly delimit each segment of the answer to ensure better post-processing. Make sure to follow the outlined structure for the answer. If you cannot come up with something useful, provide a link for further reading."},
            {"role": "user",      "content": "Could you provide a detailed itinerary for my trip, complete with up-to-date events, time and cost estimates for each activity, navigation instructions, and any local events or festivals I might be interested in? I'm also interested in any insider tips or local knowledge that could enhance my experience. Rather say more than too little."}
            ],
        temperature=0, #This should stay
        #name = 'USERNAME'
            max_tokens=3413,
        top_p=1,
        #stream = True, #Output Stream
        frequency_penalty=0.4,
        presence_penalty=0.5
        )
    
    assistant_message = response['choices'][0]['message']['content']
    return assistant_message

@app.route('/webhook', methods=['POST'])
def webhook():
    processed_text = call_openai_api()
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=True)

