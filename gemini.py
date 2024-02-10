import vertexai
from vertexai.preview.generative_models import (
    Content,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
from google.oauth2 import service_account
import google.generativeai as genai
from config import *


class Gemini:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)

        genai_model = genai.GenerativeModel('gemini-pro')

        key_path = VERTEXAI_KEY_PATH

        credentials = service_account.Credentials.from_service_account_file(
            key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        vertexai.init(project=VERTEXTAI_PROJECT_ID, location=VERTEXTAI_LOCATION, credentials=credentials)
        self.model = GenerativeModel("gemini-pro")


    def get_nearby_airports(self, location):
        get_nearby_airports_response = self.model.generate_content(
            f"give airport codes near to this area -> {location}. Only IATA code, comma separated. Single string.")
        print(get_nearby_airports_response.text)
        airport_codes = get_nearby_airports_response.text.replace(" ", "").split(",")
        print(airport_codes)
        return airport_codes

    def get_iata(self, location):
        get_iata_response = self.model.generate_content(f"{location} airport IATA code")
        iata = get_iata_response.text.strip()
        print("iata: " + iata)
        return iata

    def get_flight_search_parameters(self, user_input):
        try:
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

            prompt = user_input

            response = self.model.generate_content(
                prompt,
                generation_config={"temperature": 0},
                tools=[flights_tool],
            )

            results = response.candidates[0].content.parts[0].function_call
            print(results)

            result_content = response.candidates[0].content.parts[0].function_call
            result_func_name = result_content.name
            print("result_func_name: " + result_func_name)

            if (result_func_name != ""):
                origin = str(result_content.args.pb["origin"])
                origin = origin.strip().replace("string_value:","").replace('"',"")
                print("origin: " + origin)
                origin_airport = self.get_iata(origin)
                print("-----")
                destination = str(result_content.args.pb["destination"])
                destination = destination.strip().replace("string_value:", "").replace('"', "")
                print("destination: " + destination)
                destination_airport = self.get_iata(destination)
                print("-----")
                date = str(result_content.args.pb["date"])
                date = date.strip().replace("string_value:", "").replace('"', "")
                print("date: " + date)
                print("-----")
                return [origin_airport, destination_airport, date]
            else:
                print("no function identified")
                return False


            # if (result_func_name != ""):
            #     origin = str(result_content.args.pb["origin"])
            #     origin = origin.strip().replace("string_value:","").replace('"',"")
            #     print("origin: " + origin)
            #     if(len(origin)==3):
            #         origin_airports = [origin]
            #     else:
            #         origin_airports = self.get_nearby_airports(origin)
            #     print("------")
            #
            #     destination = str(result_content.args.pb["destination"])
            #     destination = destination.strip().replace("string_value:", "").replace('"', "")
            #     print("destination: " + destination)
            #     if (len(origin) == 3):
            #         destination_airports = [destination]
            #     else:
            #         destination_airports = self.get_nearby_airports(destination)
            #
            #     date = str(result_content.args.pb["date"])
            #     date = date.strip().replace("string_value:", "").replace('"', "")
            #     print("date: " + date)
            #     return [origin_airports, destination_airports, date]
            # else:
            #     print("no function identified")
            #     return False

        except Exception as e:
            print("Error: " + str(e))
            return False
