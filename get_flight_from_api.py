import requests
from xml.etree import ElementTree as ET

def get_access_token():
    url = "https://aero-suite-stage4-airarabia.isaaviation.net/api/auth/authenticate"
    headers = {"content-type": "application/json"}  # If needed
    data = {"login": "admin@mail.com", "password": "Qwerty1!"}  # If needed

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201 or 200:
        access_token = response.json()['tokenPair']['accessToken']
        return access_token
    else:
        print(f"Error creating post: {response.status_code}")
        return ""

def get_selected_flights(origin, destination, date):
    try:
        # origin = "HBE"
        # destination = "BAH"
        # date = "2024-02-12"

        access_token = get_access_token()
        # print(access_token)

        url = "https://aero-search-best-offer-soap-api-service-stage4-airarabia.isaaviation.net/best-offer/AirShopping/17.2/V1/"
        headers = {"Content-Type": "text/xml; charset=utf-8",
                   "Authorization": "Bearer " + access_token}
        body = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:get="http://www.iata.org/IATA/EDIST/2017.2">
           <soapenv:Header />
           <soapenv:Body>
              <AirShoppingRQ xmlns="http://www.iata.org/IATA/EDIST/2017.2" Version="17.2" PrimaryLangID="EN" AltLangID="EN">
                 <CoreQuery>
                    <OriginDestinations>
                       <OriginDestination>
                          <Departure>
                             <AirportCode>{ob_departure_code}</AirportCode>
                             <Date>{ob_departure_date}</Date>
                          </Departure>
                          <Arrival>
                             <AirportCode>{ob_arrival_code}</AirportCode>
                          </Arrival>
                          <CalendarDates DaysBefore="0" DaysAfter="0" />
                       </OriginDestination>
                    </OriginDestinations>
                 </CoreQuery>
                 <DataLists>
                    <PassengerList>
                       <Passenger PassengerID="T1">
                          <PTC>ADT</PTC>
                       </Passenger>
                       <Passenger PassengerID="T2">
                          <PTC>CHD</PTC>
                       </Passenger>
                       <Passenger PassengerID="T3">
                          <PTC>INF</PTC>
                        </Passenger>
                    </PassengerList>
                 </DataLists>
              </AirShoppingRQ>
           </soapenv:Body>
        </soapenv:Envelope>"""

        filled_body = body.format(
            ob_departure_code=origin,
            ob_departure_date=date,
            ob_arrival_code=destination
        )
        response = requests.post(url, headers=headers, data=filled_body)

        xml_tree = ET.ElementTree(ET.fromstring(response.text))
        ns = {'ns2': 'http://www.iata.org/IATA/EDIST/2017.2'}  # Define the namespace
        # Find all ns2:Offer elements
        offers = xml_tree.findall('.//ns2:Offer', namespaces=ns)
        selected_flight_Map = {}
        priceCalendar = xml_tree.find('.//ns2:PriceCalendar', namespaces=ns)
        totalPrice = priceCalendar.find('.//ns2:TotalPrice', namespaces=ns).text

        for offer in offers:
            offer_id = offer.get('OfferID')
            total_price = offer.find('.//ns2:TotalPrice', namespaces=ns).find('.//ns2:SimpleCurrencyPrice',
                                                                              namespaces=ns).text
            # print(offer_id)
            # print(total_price)
            if total_price == totalPrice:
                offerItems = offer.findall('.//ns2:OfferItem', namespaces=ns)
                selected_offer = offerItems[0]
                fareComponent = selected_offer.find('.//ns2:FareDetail', namespaces=ns).find('.//ns2:FareComponent',
                                                                                             namespaces=ns)
                selected_flight = fareComponent.find('.//ns2:SegmentRefs', namespaces=ns).text
                selected_flight_Map[selected_flight] = total_price

        results = []
        count = 0
        for key, value in selected_flight_Map.items():
            count+=1
            if(count>3):
                break
            print(f"{key}: {value}")
            obj = {
                "origin": origin,
                "destination": destination,
                "flight_time": key,
                "fare": value + " AED"
            }
            results.append(obj)
    except Exception as e:
        results = []
        return results

    return results
