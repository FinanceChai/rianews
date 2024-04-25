# test_env.py
from dotenv import load_dotenv
import os


load_dotenv()

# Print the value of TELEGRAM_TOKEN environment variable
print("TELEGRAM_TOKEN:", os.getenv("TELEGRAM_TOKEN"))
