import vertexai
from vertexai.preview.generative_models import (
    Content,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
from google.oauth2 import service_account

key_path = "storied-key.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

vertexai.init(project="storied-key-413908", location="us-central1", credentials=credentials)
model = GenerativeModel("gemini-pro")

get_current_weather_func = FunctionDeclaration(
    name="get_current_weather",
    description="Get the current weather in a given location",
    parameters={
        "type": "object",
        "properties": {"location": {"type": "string", "description": "Location"}},
    },
)

weather_tool = Tool(
    function_declarations=[get_current_weather_func],
)

prompt = "What is the weather like in Boston?"

response = model.generate_content(
    prompt,
    generation_config={"temperature": 0},
    tools=[weather_tool],
)

print(response.candidates[0].content.parts[0].function_call)