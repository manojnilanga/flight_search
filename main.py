import vertexai
from vertexai.preview.generative_models import (
    Content,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
from google.oauth2 import service_account
import json
import google.generativeai as genai
from config import *

genai.configure(api_key=GOOGLE_API_KEY)

genai_model = genai.GenerativeModel('gemini-pro')

key_path = VERTEXAI_KEY_PATH

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

vertexai.init(project=VERTEXTAI_PROJECT_ID, location=VERTEXTAI_LOCATION, credentials=credentials)
model = GenerativeModel("gemini-pro")

get_flights_func = FunctionDeclaration(
    name="get_flights",
    description="Get available flights",
    parameters={
        "type": "object",
        "properties": {
            "origin": {"type": "string", "description": "origin location"},
            "destination": {"type": "string", "description": "destination location"},
            "date": {"type": "string", "description": "date"},
        },
    },
)

flights_tool = Tool(
    function_declarations=[get_flights_func],
)

prompt = "We wanted to go on a vacation from long time. So we decided to go finally. we want to go from Sri lanka to England next Monday"
prompt = "We wanted to go on a vacation from long time. So we decided to go finally. we want to go from Alexandria, Egypt to Bahrain next Monday"
prompt = "We wanted to go on a vacation from long time. So we decided to go finally. we want to go from Alexandria, Egypt to Bahrain on 2024-02-12"
prompt = "We are in Bahrain. we need to go to Alexandria, Egypt on 2024-02-25"
# prompt = "We wanted to go on a vacation from long time."

response = model.generate_content(
    prompt,
    generation_config={"temperature": 0},
    tools=[flights_tool],
)

def get_nearby_airports(location):
    get_nearby_airports_response = model.generate_content("give airport codes near to this area -> " + location +". only IATA code. comma seperated. single string.")
    print(get_nearby_airports_response.text)
    airport_codes = get_nearby_airports_response.text.replace(" ","").split(",")
    print(airport_codes)


results = response.candidates[0].content.parts[0].function_call
print(results)

result_content = response.candidates[0].content.parts[0].function_call
result_func_name = result_content.name
print("result_func_name: " + result_func_name)
if(result_func_name != ""):
    origin = str(result_content.args.pb["origin"])
    print("origin: " + origin)
    origin_airports = get_nearby_airports(origin)

    destination = str(result_content.args.pb["destination"])
    print("destination: " + destination)
    destination_airports = get_nearby_airports(destination)

    date = str(result_content.args.pb["date"])
    print("date: " + date)
else:
    print("no function identified")


