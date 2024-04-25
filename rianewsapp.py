# test_env.py
from dotenv import load_dotenv
import os

# Specify the path to the .env file
dotenv_path = "/home/rianews/rianewsapp.env"

# Load environment variables from the .env file
load_dotenv(dotenv_path)

# Print the value of TELEGRAM_TOKEN environment variable
print("TELEGRAM_TOKEN:", os.getenv("TELEGRAM_TOKEN"))
