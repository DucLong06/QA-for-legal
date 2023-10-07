import os
from dotenv import load_dotenv

load_dotenv()

root_dir = os.path.dirname(os.path.abspath(__file__))
PATH_TO_CACHE = os.getenv(
    "PATH_TO_CACHE", os.path.join(root_dir, 'cache'))

MODEL_NAME = os.getenv(
    "MODEL_NAME", os.path.join(root_dir, 'cache'))

QUESTION_TYPE = os.getenv(
    "QUESTION_TYPE", ["true_false", "options", "free_text"])
