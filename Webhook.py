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
        
        prompt_text = (
    "Title: 'The Dance of the Cosmos: Exploring the Interplay between Chaos Theory "
    "and Quantum Mechanics in Predicting Celestial Mechanics'\n\n"
    "Prompt:\n\n"
    "The deterministic yet unpredictable nature of chaotic systems and the inherent "
    "uncertainty in quantum mechanics appear to be at odds, yet they both play crucial "
    "roles in understanding the behavior of celestial bodies. Your task is to delve into "
    "the interplay between Chaos Theory and Quantum Mechanics in the realm of celestial mechanics.\n\n"
    "1. Provide a comprehensive overview of Chaos Theory and Quantum Mechanics, elucidating "
    "their fundamental principles, mathematical frameworks, and historical evolution.\n"
    "2. Discuss how these theories have been utilized or juxtaposed in explaining and predicting "
    "the dynamics of celestial bodies, including planets, asteroids, comets, and other astronomical phenomena.\n"
    "3. Explore the challenges and limitations faced by physicists and astronomers in employing "
    "these theories for celestial predictions. How has the advent of quantum computing and advancements "
    "in numerical simulations aided in overcoming these challenges?\n"
    "4. Delve into speculative or emerging theories that attempt to bridge the gaps between Chaos Theory "
    "and Quantum Mechanics, and discuss their potential implications for future astronomical predictions "
    "and explorations.\n"
    "5. Reflect on the philosophical and practical implications of the interplay between determinism and "
    "uncertainty in our understanding of the universe. How does this interplay influence the scientific "
    "quest for a unified theory of physics?\n"
    "6. Finally, propose a hypothetical or real-world scenario where a melding of Chaos Theory and Quantum "
    "Mechanics could significantly advance our understanding or prediction of celestial mechanics. Discuss "
    "the potential impact on space exploration, astrophysical research, or technological advancements.\n\n"
    "Ensure your response is well-researched, thoroughly referenced, and delves deeply into the mathematical "
    "and physical intricacies involved, making connections to real-world applications and speculative future scenarios."
)

        role = "You will be my physics teacher"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt_text},
                {"role": "assistant", "content": ""}
            ],
            max_tokens=7000,
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
