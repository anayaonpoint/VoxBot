# chatbot/gemini_utils.py
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def get_emotion_response(user_input):
    prompt = f"""
    You are a chatbot. A user has asked the following:

    "{user_input}"

    1. Reply to the user in a helpful and human way.
    2. Classify the **emotion** behind their question as one of these: [neutral, happy, sad, angry, anxious, curious, excited].
    3. Respond in this format (strictly JSON):

    {{
        "response": "<your helpful response here>",
        "emotion": "<emotion label>"
    }}
    """

    result = model.generate_content(prompt)
    
    import json
    try:
        return json.loads(result.text)
    except json.JSONDecodeError:
        return {"response": result.text, "emotion": "neutral"}
