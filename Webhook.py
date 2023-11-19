from flask import Flask, request, jsonify
import openai
from datetime import datetime
import requests
import time
import sys as os

app = Flask(__name__)

#VARIABLES
openai.api_key = os.environ.get('OPENAI_API_KEY', 'your-api-key')
model= "gpt-3.5-turbo-16k"
token= 15000

def calculate_age(birthdate_str):
    try:
        # Adjusting the date format to match the payload
        birthdate = datetime.strptime(birthdate_str, "%d-%m-%Y")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    except ValueError:
        return 'Unknown age'
    
def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url)
        response_json = response.json()
        return response_json.get("display_name", "Unknown location")
    except Exception as e:
        return f"Error in reverse geocoding: {str(e)}"

#WEATHER DATA MAYBE

'''
PAYLOAD:
"profile": [
    "interests": profileViewModel.selectedInterests,
    "adjectives": profileViewModel.selectedAdjectives,
    "places": profileViewModel.selectedPlaces,
    "activities": profileViewModel.selectedActivities,
    "gender": profileViewModel.gender,
    "birthDate": birthDateString,
    "home": profileViewModel.home
],
"trip": [
    "preferences": newTripViewModel.selectedPreferences,
    "start": startDate,
    "end": endDate,
    "description": newTripViewModel.description,
    "budgetRange": sliderRangeString,
    "location": locationString
]
'''

@app.route('/LocalFlask', methods=['POST'])
def webhook():
    try:
        print("Request Headers:", request.headers)
        data = request.json
        print("Received Payload:", data)

        # Extract data from payload
        profile_data = data.get('profile', {})
        trip_data = data.get('trip', {})
        #==============================================================================
        # Mandatory fields for profile and trip data
        mandatory_profile_fields = ['birthDate', 'gender']
        mandatory_trip_fields = ['start', 'end', 'location', 'budgetRange']

        # List fields that shouldn't be empty in profile and trip data
        profile_list_fields = ['interests', 'places', 'activities']
        trip_list_fields = ['preferences']

        # Check for missing mandatory fields
        missing_fields = [field for field in mandatory_profile_fields if field not in profile_data]
        missing_fields += [field for field in mandatory_trip_fields if field not in trip_data]

        # Check for empty list fields
        missing_fields += [field for field in profile_list_fields if not profile_data.get(field)]
        missing_fields += [field for field in trip_list_fields if not trip_data.get(field)]

        if missing_fields:
            return jsonify({"error": f"Please fill in the following mandatory fields or ensure they are not empty: {', '.join(missing_fields)}."}), 400
        #==============================================================================
        birthDate_str = profile_data.get('birthDate', '')
        age = calculate_age(birthDate_str) if birthDate_str else 'Unknown age'
        gender = profile_data.get('gender', 'Not specified')
        # Define duration
        start_date = trip_data.get('start', 'start date')
        end_date = trip_data.get('end', 'end date')
        duration = f"{start_date} to {end_date}"

        # Processing coordinates with error handling
        destination = trip_data.get('location', 'Unknown location')
        if destination != 'Unknown location':
            coords = destination.split(',')
            if len(coords) == 2:
                lat = coords[0].split(':')[1].strip()
                lon = coords[1].split(':')[1].strip()
                destination_name = reverse_geocode(lat, lon)
                print(destination_name)
            else:
                destination_name = 'Invalid coordinate format'
        else:
            destination_name = 'Unknown location'
        #travel_type = profile_data.get('interests', ['general'])[0]  # Example, modify as needed
        budget = trip_data.get('budgetRange', 'Not specified')
        #staying_location = 'Unknown'  # You might need to add this to your data model
        transport = 'Unknown'  # You might need to add this to your data model
        interests =     profile_data.get('interests', [])
        places =        profile_data.get('places', [])
        adjectives =    profile_data.get('adjectives', [])
        activities =    profile_data.get('activities',[])
        preferences =   trip_data.get('preferences',[])
        home =          profile_data.get('home','Unknown location')
        description =   trip_data.get('description', 'not provided')
        

        print("API Call...")
        test_response = {
            "age": age,
            "gender": gender,
            "destination_name": destination_name,
            "duration": duration,
            #"travel_type": travel_type,
            "budget": budget,
            #"staying_location": staying_location,
            "transport": transport,
            "interests": interests
        }

        #==============================================================================
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
        user_info = f"I am a {age}-year-old {gender} interested in {', '.join(interests)}. A selection of places in enjoy is {','.join(places)}. My hometown is {home}. I chose these adjectives to describe my thought after travel experinece: {', '.join(adjectives)}."
        trip_info = f"I am planning to visit {destination_name} from {duration}. I am interested in activities like {', '.join(preferences)}. I have a budget from {budget} for this trip. This is how I would describe my trip in one sentence: {description}"

        response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Create a travel itinerary."},
            {"role": "assistant", "content": assistant_guidelines},
            {"role": "user", "content": user_info},
            {"role": "user", "content": trip_info},
            {"role": "user", "content": "Can you create a detailed itinerary for my trip based on this information? Include a cost summary and a summarization at the end of the itinerary."}
        ],
        temperature=0,
        max_tokens=token,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.6
    )

        return jsonify({"processed_parameters": test_response,"processed_text": response['choices'][0]['message']['content']})
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)


'''
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/LocalFlask', methods=['POST'])
def webhook():
    try:
        print("Request Headers:", request.headers)
        data = request.json
        print("Received Payload:", data)
        # Your existing response code...
        response = {
             "processed_text": "**Day 3: Saturday**\n\n- **10:00 AM - Breakfast at Commonground**\n    - *Cost*: €10-15\n    - *Time Needed*: 1 hour\n    - *Navigation*: Rosenthaler Str. 1, 10119 Berlin\n    - *Insider Tip*: Commonground is a trendy café known for its delicious breakfast options and stylish interior. Start your day with a satisfying meal before embarking on your vintage shopping adventure.\n\n- **11:30 AM - Vintage Shopping in Prenzlauer Berg**\n    - *Cost*: Free (unless you decide to purchase something)\n    - *Time Needed*: 3 hours\n    - *Navigation*: Kastanienallee, Oderberger Str., and surrounding streets in Prenzlauer Berg\n    - *Insider Tip*: Prenzlauer Berg is a neighborhood known for its vintage shops and boutiques. Explore the charming streets and discover unique clothing, accessories, and retro treasures.\n\n- **2:30 PM - Lunch at Prater Biergarten**\n    - *Cost*: €10-15\n    - *Time Needed*: 1 hour\n    - *Navigation*: Kastanienallee 7-9, 10435 Berlin\n    - *Insider Tip*: Prater Biergarten is a historic beer garden offering traditional German cuisine. Enjoy a hearty meal and soak up the relaxed atmosphere before continuing your exploration.\n\n- **4:00 PM - Visit Boxhagener Platz Flohmarkt**\n    - *Cost*: Free (unless you decide to purchase something)\n    - *Time Needed*: 2 hours\n    - *Navigation*: Boxhagener Platz, 10245 Berlin\n    - *Insider Tip*: The Boxhagener Platz Flohmarkt is a popular flea market where you can find a wide range of vintage items, antiques, and second-hand goods. Spend some time browsing through the stalls and bargaining for unique finds.\n\n- **6:30 PM - Dinner at Schwarzwaldstuben**\n    - *Cost*: €15-20\n    - *Time Needed*: 1 hour\n    - *Navigation*: Tucholskystraße 48, 10117 Berlin\n    - *Insider Tip*: Schwarzwaldstuben is a cozy restaurant serving traditional German dishes with a modern twist. Indulge in their delicious food while enjoying the rustic ambiance of this hidden gem.\n"
    }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''