import google.generativeai as genai
from config import *

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

# response = model.generate_content("give airport codes near to this area -> sharjah. only IATA code. comma seperated. single string.")
response = model.generate_content("tomorrows date in YYYY-MM-DD format")
print(response.text)