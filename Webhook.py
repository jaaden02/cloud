from flask import Flask, request, jsonify
from openai import OpenAI
from datetime import datetime
import os
import Text as c

app = Flask(__name__)


#VARIABLES
model1 = "gpt-4"
model2 = "gpt-3.5-turbo-16k"
token1 = 8000
token2 = 16000
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-api-key')
client = OpenAI(api_key = OPENAI_API_KEY)

def calculate_age(birthdate_str):
    try:
        # Adjusting the date format to match the payload
        birthdate = datetime.strptime(birthdate_str, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    except ValueError:
        return 'Unknown age'


@app.route('/Webhook', methods=['POST'])
def call_openai_api():
    try:
        print("Request Headers:", request.headers)
        data = request.json
        print("Received Payload:", data)

        # Extract data from payload
        profile_data = data.get('profile', {})
        trip_data = data.get('trip', {})
        #==============================================================================
        # Extract data from payload
        profile_data = data.get('profile', {})
        trip_data = data.get('trip', {})

        birthDate_str = profile_data.get('birthDate', '')
        age = calculate_age(birthDate_str) if birthDate_str else 'Unknown age'
        gender = profile_data.get('gender', 'Not specified')

        # Other extracted data
        destination_name = trip_data.get('location', 'Unknown location')
        start_date = trip_data.get('start', 'start date')
        end_date = trip_data.get('end', 'end date')
        duration = f"{start_date} to {end_date}"
        budget = trip_data.get('budgetRange', 'Not specified')
        interests = profile_data.get('interests', [])
        places = profile_data.get('places', [])
        adjectives = profile_data.get('adjectives', [])
        activities = profile_data.get('activities',[])
        preferences = trip_data.get('preferences',[])
        home = profile_data.get('home','Unknown location')
        description = trip_data.get('description', 'not provided')
        #timePreferences = trip_data.get('timePreferences','all day')    I would like to get detailed plans for these daytimes: {','.join(timePreferences)}.

    #==============================================================================
        #FIRST REQUEST
        role = "You are a personal tour guide responsible for creating a detailed, all-inclusive, step-by-step itinerary."

        content_guidelines = f"""
        - Be extremely specific and actionable in each entry of the itinerary. 
        - Do not suggest 'maybe' or 'you could try' activities. Include only confirmed, planned items with detailed descriptions.
        - If certain information like cost or time needed is not available, provide an estimated range or suggest a typical scenario.
        - Ensure that each field in the activity structure is filled with relevant and specific information.
        - Think about how the information about me connects and try to imagine how the combination of factors might result in specific preferences.
        - Try to infer a broader picture of my preferences by considering the interplay of all the information.
        - The itinerary should be a complete stand-alone plan that leaves no open questions. 
        - If this information about my preferences: {', '.join(preferences)} conflicts with the information about my interest: {', '.join(interests)}, weigh the Preferences higher.
        - Give high importance to the one-sentence description of the trip.
        - Do not rush to an answer but make carefull consideration.
        """

        user_info = f"""These are the User Details: I am a {age}-year-old {gender} interested in {', '.join(interests)}. 
                    A selection of places I enjoy is {','.join(places)}. My hometown is {home}. 
                    I chose these adjectives to describe my thought after travel experience: {', '.join(adjectives)}."""
        trip_info = f"""These are the Trip Details: I am planning to visit {destination_name} from {duration}. 
                    I am interested in activities like {', '.join(preferences)}. 
                    I have a budget of {budget} out of 10 for this trip. 
                    This is how I would describe my trip in one sentence: {description}"""

        structural_guidelines = c.structural_guidelines

        activation = c.activation

        print("API Call")
        response = client.chat.completions.create(
            model=model2,
            messages=[
                {"role": "system", "content": role},
                {"role": "system", "content": structural_guidelines},
                {"role": "assistant", "content": content_guidelines},
                {"role": "assistant", "content": user_info},
                {"role": "assistant", "content": trip_info},
                {"role": "user", "content": activation}
            ],
            temperature=0,
            max_tokens=token2 - 702,
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.6
        )
        assistant_message = response.choices[0].message.content
        token_1 = response.usage.total_tokens
    #==============================================================================
    #PERSONA
    #==============================================================================
    #JSON FORMATING
        JSON_guidelines = c.JSON_guidelines

        role_ = "Your task is to format the itinerary into JSON according to the provided guidelines."
        itinerary = f"This is the plan for the trip: {assistant_message}"
        formating = """Format the itinerary into JSON as per the guidelines. Be precise and thorough. The output must be complete, accurate, and in valid JSON format."""

        formated_response = client.chat.completions.create(
            model=model2,
            messages=[
                {"role": "system", "content": role_},
                {"role": "assistant", "content": itinerary},
                {"role": "assistant", "content": JSON_guidelines},
                {"role": "user", "content": formating}
            ],
            temperature=0.1,
            max_tokens=token2-token_1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        assistant_message = formated_response.choices[0].message.content
        token_2 = formated_response.usage.total_tokens
        print(assistant_message, "Token:", token_2)

        print("Token:", token_1+token_2, "\n Cost approx:", (token_1+token_2)/1000*0.002)
                
        return assistant_message
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/Webhook', methods=['POST'])
def webhook():
    processed_text = call_openai_api()
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=False)
