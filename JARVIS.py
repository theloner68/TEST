import requests
from collections import defaultdict
import os
import json

API_KEY = os.getenv("XAI_API_KEY", "your_xai_api_key_here")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def send_message(message):
    payload = {
        "messages": [
            {"role": "user", "content": message}
        ],
        "stream": False
    }
    try:
        response = requests.post('https://api.x.ai/v1/chat/completions', headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

history = defaultdict(list)

def learn_and_respond(message):
    response = send_message(message)
    history['user'].append(message)
    history['jarvis'].append(response)
    
    if "how are you" in message.lower():
        response += " By the way, I've noticed you often ask how I am. I'm doing great, thank you for your interest!"
    
    return response

def handle_context(message):
    response = learn_and_respond(message)
    if "could you clarify" in response.lower():
        clarification = input("JARVIS: Could you please provide more context or clarify your question?\n")
        response = learn_and_respond(clarification)
    return response

def request_feedback(response):
    feedback = input("JARVIS: How was my response? (Good/Bad)\n")
    if feedback.lower() == "bad":
        learn_and_respond("I'm sorry, can you tell me how I could improve?")
    else:
        print("JARVIS: Thank you! I'm learning to serve you better.")

while True:
    message = input("You: ")
    if message.lower() == "exit":
        break
    response = handle_context(message)
    print(f"JARVIS: {response}")
    request_feedback(response)

