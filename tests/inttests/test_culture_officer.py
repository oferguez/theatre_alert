import os
from pprint import PrettyPrinter
import datetime
from dotenv import load_dotenv
from culture_officer import handler

load_dotenv()

if __name__ == "__main__":
    result = handler(None)  # Call the handle function to run the tests
