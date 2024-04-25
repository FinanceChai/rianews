from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Iterate over environment variables and print each one
for key, value in os.environ.items():
    print(f"{key}: {value}")
