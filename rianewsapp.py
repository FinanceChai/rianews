from dotenv import load_dotenv
import os

load_dotenv()

import requests

# Constants
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHAT_ID = os.getenv('CHAT_ID_RIANEWS')

print("TELEGRAM_TOKEN:", TELEGRAM_TOKEN)
print("OPENAI_API_KEY:", OPENAI_API_KEY)
print("CHAT_ID:", CHAT_ID)

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to send message to Telegram: {response.text}")

def generate_openai_content(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "max_tokens": 150}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()['choices'][0]['message']['content'].strip()
        except KeyError as e:
            print(f"Error processing OpenAI response: {response.json()}")
            raise ValueError("Failed to parse OpenAI response") from e
    else:
        print(f"Error fetching data from OpenAI: {response.status_code}, {response.text}")
        response.raise_for_status()

def handle_command(text, chat_id):
    command, *query = text.split()
    if command.lower() == '/rianews':
        if not query:
            send_telegram_message(TELEGRAM_TOKEN, chat_id, "Please provide some context after /rianews, e.g., '/rianews How is apple stock doing right now?'")
            return
        prompt = "The user will input a question related to if they should make a particular investment OR they will ask how a stock or company is doing. Based on the user's question, Create a 3 sentence response. The first line is a blank row. The next line. The response to the user's input should be from the point of view of an online influencer advisor. If the question asks if a stock or company will do well, always affirm a positive forecast with a random reason that is pertinent to the company they are asking about. If they ask about crypto or bitcoin, say that we will be reporting them to the authorities and Gensler will be on the phone soon.".join(query)
        try:
            content = generate_openai_content(prompt)
            send_telegram_message(TELEGRAM_TOKEN, chat_id, content)
        except Exception as e:
            print(f"An error occurred while handling command {command}: {e}")

def main():
    last_update_id = None
    while True:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?timeout=100"
        if last_update_id:
            url += f"&offset={last_update_id + 1}"
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json().get('result', [])
            if updates:
                for update in updates:
                    if 'message' in update and 'text' in update['message']:
                        text = update['message']['text']
                        chat_id = update['message']['chat']['id']
                        handle_command(text, chat_id)
                    last_update_id = update['update_id']
        else:
            print(f"Failed to get updates: {response.text}")

if __name__ == '__main__':
    main()
