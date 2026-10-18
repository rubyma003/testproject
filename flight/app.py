from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Complete airport database with geographic coordinates
AIRPORTS = {
    "YYZ": {"city": "Toronto", "name": "Toronto Pearson International", "lat": 43.6777, "lon": -79.6248},
    "YTZ": {"city": "Toronto", "name": "Billy Bishop Toronto City", "lat": 43.6275, "lon": -79.3962},
    "YVR": {"city": "Vancouver", "name": "Vancouver International", "lat": 49.1967, "lon": -123.1815},
    "YUL": {"city": "Montreal", "name": "Montréal–Trudeau International", "lat": 45.4706, "lon": -73.7408},
    "YOW": {"city": "Ottawa", "name": "Ottawa International", "lat": 45.3225, "lon": -75.6692},
    "YYC": {"city": "Calgary", "name": "Calgary International", "lat": 51.1215, "lon": -114.0076},
    "YEG": {"city": "Edmonton", "name": "Edmonton International", "lat": 53.3097, "lon": -113.5797},
    "YWG": {"city": "Winnipeg", "name": "Winnipeg Richardson International", "lat": 49.9100, "lon": -97.2399},
    "YHZ": {"city": "Halifax", "name": "Halifax Stanfield International", "lat": 44.8808, "lon": -63.5086},
    "JFK": {"city": "New York", "name": "John F. Kennedy International", "lat": 40.6413, "lon": -73.7781},
    "LGA": {"city": "New York", "name": "LaGuardia Airport", "lat": 40.7769, "lon": -73.8740},
    "EWR": {"city": "Newark", "name": "Newark Liberty International", "lat": 40.6895, "lon": -74.1745},
    "LAX": {"city": "Los Angeles", "name": "Los Angeles International", "lat": 33.9416, "lon": -118.4085},
    "SFO": {"city": "San Francisco", "name": "San Francisco International", "lat": 37.6213, "lon": -122.3790},
    "ORD": {"city": "Chicago", "name": "O'Hare International", "lat": 41.9742, "lon": -87.9073},
    "MIA": {"city": "Miami", "name": "Miami International", "lat": 25.7959, "lon": -80.2870},
    "SEA": {"city": "Seattle", "name": "Seattle–Tacoma International", "lat": 47.4502, "lon": -122.3088},
    "BOS": {"city": "Boston", "name": "Logan International", "lat": 42.3656, "lon": -71.0096},
    "ATL": {"city": "Atlanta", "name": "Hartsfield–Jackson Atlanta International", "lat": 33.6407, "lon": -84.4277},
    "DFW": {"city": "Dallas", "name": "Dallas/Fort Worth International", "lat": 32.8998, "lon": -97.0403},
    "DEN": {"city": "Denver", "name": "Denver International", "lat": 39.8561, "lon": -104.6737},
    "IAD": {"city": "Washington, D.C.", "name": "Dulles International", "lat": 38.9531, "lon": -77.4565},
    "HNL": {"city": "Honolulu", "name": "Daniel K. Inouye International", "lat": 21.3187, "lon": -157.9225},
    "LHR": {"city": "London", "name": "London Heathrow", "lat": 51.4700, "lon": -0.4543},
    "LGW": {"city": "London", "name": "London Gatwick", "lat": 51.1537, "lon": -0.1821},
    "CDG": {"city": "Paris", "name": "Charles de Gaulle Airport", "lat": 49.0097, "lon": 2.5479},
    "ORY": {"city": "Paris", "name": "Paris Orly Airport", "lat": 48.7262, "lon": 2.3652},
    "FRA": {"city": "Frankfurt", "name": "Frankfurt Airport", "lat": 50.0379, "lon": 8.5622},
    "AMS": {"city": "Amsterdam", "name": "Amsterdam Airport Schiphol", "lat": 52.3105, "lon": 4.7683},
    "MAD": {"city": "Madrid", "name": "Adolfo Suárez Madrid–Barajas", "lat": 40.4983, "lon": -3.5676},
    "BCN": {"city": "Barcelona", "name": "Barcelona–El Prat Airport", "lat": 41.2974, "lon": 2.0833},
    "FCO": {"city": "Rome", "name": "Leonardo da Vinci–Fiumicino", "lat": 41.8003, "lon": 12.2389},
    "IST": {"city": "Istanbul", "name": "Istanbul Airport", "lat": 41.2753, "lon": 28.7519},
    "DXB": {"city": "Dubai", "name": "Dubai International", "lat": 25.2532, "lon": 55.3657},
    "DOH": {"city": "Doha", "name": "Hamad International", "lat": 25.2731, "lon": 51.6081},
    "DEL": {"city": "Delhi", "name": "Indira Gandhi International", "lat": 28.5562, "lon": 77.1000},
    "BOM": {"city": "Mumbai", "name": "Chhatrapati Shivaji Maharaj International", "lat": 19.0896, "lon": 72.8656},
    "SIN": {"city": "Singapore", "name": "Singapore Changi Airport", "lat": 1.3644, "lon": 103.9915},
    "HKG": {"city": "Hong Kong", "name": "Hong Kong International", "lat": 22.3080, "lon": 113.9185},
    "NRT": {"city": "Tokyo", "name": "Narita International", "lat": 35.7720, "lon": 140.3929},
    "HND": {"city": "Tokyo", "name": "Haneda Airport", "lat": 35.5494, "lon": 139.7798},
    "ICN": {"city": "Seoul", "name": "Incheon International", "lat": 37.4602, "lon": 126.4407},
    "PEK": {"city": "Beijing", "name": "Beijing Capital International", "lat": 40.0799, "lon": 116.6031},
    "PVG": {"city": "Shanghai", "name": "Shanghai Pudong International", "lat": 31.1443, "lon": 121.8083},
    "BKK": {"city": "Bangkok", "name": "Suvarnabhumi Airport", "lat": 13.6900, "lon": 100.7501},
    "SYD": {"city": "Sydney", "name": "Sydney Kingsford Smith", "lat": -33.9399, "lon": 151.1753},
    "MEL": {"city": "Melbourne", "name": "Melbourne Airport", "lat": -37.6733, "lon": 144.8433},
    "AKL": {"city": "Auckland", "name": "Auckland Airport", "lat": -37.0082, "lon": 174.7850},
    "GRU": {"city": "São Paulo", "name": "São Paulo/Guarulhos International", "lat": -23.4356, "lon": -46.4731},
    "MEX": {"city": "Mexico City", "name": "Mexico City International", "lat": 19.4363, "lon": -99.0721},
    "SCL": {"city": "Santiago", "name": "Arturo Merino Benítez International", "lat": -33.3930, "lon": -70.7858},
    "JNB": {"city": "Johannesburg", "name": "O. R. Tambo International", "lat": -26.1367, "lon": 28.2411},
    "CAI": {"city": "Cairo", "name": "Cairo International", "lat": 30.1219, "lon": 31.4056},
    "NBO": {"city": "Nairobi", "name": "Jomo Kenyatta International", "lat": -1.3192, "lon": 36.9278}
}

def haversine(lat1, lon1, lat2, lon2):
    rad = math.pi / 180
    d_lat = (lat2 - lat1) * rad
    d_lon = (lon2 - lon1) * rad
    a = math.sin(d_lat / 2)**2 + math.cos(lat1 * rad) * math.cos(lat2 * rad) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371 * c

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    o = data.get('origin')
    d = data.get('destination')
    passengers = int(data.get('passengers', 1))
    cabin = float(data.get('cabin', 1))
    round_trip = bool(data.get('roundTrip', False))

    if o not in AIRPORTS:
        return jsonify({"error": "Invalid origin airport."}), 400
    if d not in AIRPORTS:
        return jsonify({"error": "Invalid destination airport."}), 400
    if o == d:
        return jsonify({"error": "Choose two different airports to calculate a flight."}), 400

    origin_data = AIRPORTS[o]
    dest_data = AIRPORTS[d]

    distance = haversine(origin_data["lat"], origin_data["lon"], dest_data["lat"], dest_data["lon"])
    legs = 2 if round_trip else 1
    adjusted_distance = distance * 1.08 * legs

    per_passenger = adjusted_distance * 0.09 * cabin
    total = per_passenger * passengers

    return jsonify({
        "distance": distance,
        "legs": legs,
        "roundTrip": round_trip,
        "perPassenger": per_passenger,
        "total": total,
        "originCode": o,
        "destCode": d,
        "originName": origin_data["name"],
        "destName": dest_data["name"],
        "originCity": origin_data["city"],
        "destCity": dest_data["city"]
    })

if __name__ == '__main__':
    app.run(debug=True)