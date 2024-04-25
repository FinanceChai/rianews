import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Constants
TELEGRAM_TOKEN = os.getenv('7018488271:AAFpadGFgh-y4js6mVdTaWvjGz9pofZFoHs')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHAT_ID = os.getenv('-1001997793892')


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
        prompt = "Respond to the question proposed by the user. The prompt must ask questions about companies in the S&P 500. Create a 1-2 sentence response, using short sentence structures. The first line in the resonse should eb the title $RIA NEWS - BREAKING REPORT. Then a space in between. Then the response to the user's input should be satirical funny. Make sure the response is relevant to the question and readdresses the company they are asking about".join(query)
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
