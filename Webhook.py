import openai
import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)


# Function to call OpenAI API and process text


# GPT-3.5 Turbo API call

def call_openai_api():
    try:
        openai.api_key = os.environ.get('OPENAI_API_KEY', 'your-fallback-api-key')
        
        if not openai.api_key:
            return jsonify({"error": "API key not found"}), 500
        
        model= "gpt-3.5-turbo-16k"
        token= 16000

        # Role definition
        role = "You are a personal tour guide responsible for creating a detailed, all-inclusive, step-by-step itinerary."

        # Static Parameters (Personal Profile, Travel Preferences, etc.)
        static_params = {
            'age': 21,
            'gender': 'male',
            'relationship_status': 'single',
            'travel_companions': 'none',
            'travel_type': 'solo',
            'budget': 'student budget',
            'activity_level': 'active'
        }

        # Interests
        interests = ['independent films', 'techno music', 'vintage items', 'small cafes', 'old rustic bars']

        # Varying Parameters (Specific to each trip)
        varying_params = {
            'destination': 'Berlin',
            'location': 'near S Warschauer Brücke',
            'transport': 'comfortable using public transit',
            'duration': 'Thursday to Sunday'  # Adding the duration of the trip
        }

        # Assistant guidelines and formatting template
        assistant_guidelines = """## Guidelines for creating the itinerary
        ---------------------------------------
        - Follow this structure for each day:
        1. **Day X: [Weekday]**
        ---------------------------------------
            - **[Time] - [Activity Description]** (Provide a detailed explanation for why each activity is chosen.)
                - *Cost*: [Cost Estimate]
                - *Time Needed*: [Time Estimate]
                - *Navigation*: [Exact Address or Navigation Details]
                - *Insider Tip*: [If applicable]
        - Be extremely specific and actionable. 
        - Do not suggest 'maybe' or 'you could try' activities. Only include confirmed, planned items.
        - If unable to find information, suggest a specific alternative.
        ---------------------------------------
        ## Cost Summary and Summarization
        - Include a cost summary and summarization at the end of the itinerary.
        """

        print("API Call...")
        response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "assistant", "content": assistant_guidelines},
            {
                "role": "user",
                "content": f"I am a {static_params['age']}-year-old {static_params['gender']} visiting {varying_params['destination']} from {varying_params['duration']}. I am a {static_params['travel_type']} traveler on a {static_params['budget']}, staying {varying_params['location']}, and am {varying_params['transport']}."
            },
            {
                "role": "user",
                "content": f"Create an itinerary where each day features at least one activity that aligns with my interests: {', '.join(interests)}. Elaborate on why each activity is chosen and aligns with my interests. Also, include a cost summary and a summarization at the end of the itinerary."
            }
            ],
            temperature=0,
            max_tokens=token,
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.6
        )
        
        assistant_message = response['choices'][0]['message']['content']
        return assistant_message
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/Webhook', methods=['POST'])
def webhook():
    processed_text = call_openai_api()
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=False)