from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/LocalFlask', methods=['POST'])
def webhook():
    print("Request Headers:", request.headers)
    data = request.json
    print("Received Payload:", data)
    # Your existing response code...
    response = {
        "processed_text": "**Day 3: Saturday**\n\n- **10:00 AM - Breakfast at Commonground**\n    - *Cost*: €10-15\n    - *Time Needed*: 1 hour\n    - *Navigation*: Rosenthaler Str. 1, 10119 Berlin\n    - *Insider Tip*: Commonground is a trendy café known for its delicious breakfast options and stylish interior. Start your day with a satisfying meal before embarking on your vintage shopping adventure.\n\n- **11:30 AM - Vintage Shopping in Prenzlauer Berg**\n    - *Cost*: Free (unless you decide to purchase something)\n    - *Time Needed*: 3 hours\n    - *Navigation*: Kastanienallee, Oderberger Str., and surrounding streets in Prenzlauer Berg\n    - *Insider Tip*: Prenzlauer Berg is a neighborhood known for its vintage shops and boutiques. Explore the charming streets and discover unique clothing, accessories, and retro treasures.\n\n- **2:30 PM - Lunch at Prater Biergarten**\n    - *Cost*: €10-15\n    - *Time Needed*: 1 hour\n    - *Navigation*: Kastanienallee 7-9, 10435 Berlin\n    - *Insider Tip*: Prater Biergarten is a historic beer garden offering traditional German cuisine. Enjoy a hearty meal and soak up the relaxed atmosphere before continuing your exploration.\n\n- **4:00 PM - Visit Boxhagener Platz Flohmarkt**\n    - *Cost*: Free (unless you decide to purchase something)\n    - *Time Needed*: 2 hours\n    - *Navigation*: Boxhagener Platz, 10245 Berlin\n    - *Insider Tip*: The Boxhagener Platz Flohmarkt is a popular flea market where you can find a wide range of vintage items, antiques, and second-hand goods. Spend some time browsing through the stalls and bargaining for unique finds.\n\n- **6:30 PM - Dinner at Schwarzwaldstuben**\n    - *Cost*: €15-20\n    - *Time Needed*: 1 hour\n    - *Navigation*: Tucholskystraße 48, 10117 Berlin\n    - *Insider Tip*: Schwarzwaldstuben is a cozy restaurant serving traditional German dishes with a modern twist. Indulge in their delicious food while enjoying the rustic ambiance of this hidden gem.\n"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)


    #