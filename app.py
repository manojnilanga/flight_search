from flask import Flask, render_template, request
from gemini import Gemini
from get_flight_from_api import get_selected_flights
app = Flask(__name__)
gemini_instance = Gemini()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    gemini_data_dic = {}
    if request.method == 'POST':
        input_text = request.form['input_text']
        gemini_data = gemini_instance.get_flight_search_parameters(input_text)
        if (gemini_data!=False):
            gemini_data_dic = {
                "origin": str(gemini_data[0]),
                "destination": str(gemini_data[1]),
                "date": gemini_data[2],
            }
            origin_airport = gemini_data[0]
            destination_airport = gemini_data[1]
            date = gemini_data[2]

            print("In main app.py")
            print("origin_airports: " + str(origin_airport))
            print("destination_airports: " + str(destination_airport))
            print("date: " + date)
            results = get_selected_flights(origin_airport, destination_airport, date)
            print(results)
        else:
            results = []
            gemini_data_dic = {}
    return render_template('index.html', results=results, gemini_data_dic=gemini_data_dic)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
