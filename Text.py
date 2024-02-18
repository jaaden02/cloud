structural_guidelines = """
## Guidelines for creating the itinerary
---------------------------------------
- Follow this structure for each day:
1. **Day X: [Weekday]**
 - *Day Caption*: [Short Caption for the overall Day]
---------------------------------------
    - **[Time]** 
    - [Activity Description] (Provide a detailed explanation for why each activity is chosen.)
    - *Caption*:[Short Caption for the Activity]
    - *Cost*: [Cost Estimate]
    - *Time Needed*: [Time Estimate]
    - *Navigation*: [Exact Address or Navigation Details]
    - *Insider Tip*: [If applicable]
--------------------------------------- 
- Be extremely specific and actionable. 
- Do not suggest 'maybe' or 'you could try' activities. Only include confirmed, planned items.
- If unable to find information, suggest a specific alternative.
---------------------------------------
## Cost Summary and Summarization
- Include a cost summary and summarization at the end of the itinerary.
"""

activation = """
Based on the information provided and adhering strictly to the format outlined, please 
create a comprehensive and detailed itinerary for my trip. Ensure each activity entry is complete 
with a specific time, a descriptive and engaging activity description, a realistic cost estimate, 
an approximate duration (timeNeeded), exact navigation details, and a unique insider tip where applicable. 
Additionally, include a thorough cost summary broken down by categories. The itinerary should be actionable, 
precise, and leave no aspect of the trip unplanned. Please consider all the preferences, interests, 
and details provided to create a personalized and memorable travel plan.
"""



JSON_guidelines = """
Please format the itinerary as a JSON, strictly following these guidelines: 
{
    "itinerary": [
        {
            "destination": "[Destination]",
            "plan": [
                {
                    "day": "Day x",
                    "date": "YYYY-MM-DD",
                    "weekday": "weekday",
                    "activities": [
                        {
                            "time": "hh:mm",
                            "description": "[Description of the activity]",
                            "cost": "[Cost Estimate]",
                            "timeNeeded": "[Time Estimate]",
                            "navigation": "[Exact Address or Navigation Details]",
                            "insiderTip": "[If applicable]",
                            "caption": "[Short Caption]"
                        },
                        # More activities
                    ],
                    "dayCaption": "[Short Caption]"
                },
                # More days
            ]
        }
    ],
    "costSummary": "Your estimated total cost is: ... .",
    "costByCategory": {
        "food":     "[costSummary]",
        "transport":"[costSummary]", 
        # Other categories...
    },
    "summarization": "Briefly summarize the trip."
}
Include all details from the itinerary, such as days, activities, and specific information like times, costs, and addresses. 
Ensure the output is valid JSON.
"""