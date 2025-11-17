from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv('URL')

def env(x: str):
    return os.getenv(x)