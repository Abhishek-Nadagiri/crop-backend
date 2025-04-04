from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Crop Recommendation API is running."

@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    data = request.get_json()
    print("Received data:", data)

    soil = data.get('soil_type')
    water = float(data.get('water_content', 0))
    moisture = float(data.get('moisture_content', 0))
    ph = float(data.get('ph_value', 0))
    rain = float(data.get('rain_availability', 0))

    # --- Step 1: Recommend Crop ---
    def get_crop(soil, water, moisture, ph, rain):
        if soil == "loamy" and 6.0 <= ph <= 7.5 and moisture >= 30:
            return "Wheat"
        elif soil == "clay" and moisture >= 50:
            return "Rice"
        elif soil == "sandy" and rain >= 75:
            return "Maize"
        else:
            return "Millet"

    # --- Step 2: Recommend Fertilizer & Pesticide ---
    def get_recommendations(crop):
        recommendations = {
            "Wheat": {
                "fertilizer": "Urea (NPK 46-0-0)",
                "pesticide": "Chlorpyrifos or Malathion"
            },
            "Rice": {
                "fertilizer": "DAP (18-46-0) + Potash",
                "pesticide": "Carbofuran or Buprofezin"
            },
            "Maize": {
                "fertilizer": "NPK (20-20-0) or Compost",
                "pesticide": "Atrazine or Pendimethalin"
            },
            "Millet": {
                "fertilizer": "Farm Yard Manure + NPK (10-26-26)",
                "pesticide": "Neem oil or Lambda-cyhalothrin"
            }
        }
        return recommendations.get(crop, {
            "fertilizer": "General NPK mix",
            "pesticide": "General neem-based spray"
        })

    recommended_crop = get_crop(soil, water, moisture, ph, rain)
    recommendations = get_recommendations(recommended_crop)

    print("Recommended crop:", recommended_crop)
    print("Fertilizer:", recommendations["fertilizer"])
    print("Pesticide:", recommendations["pesticide"])

    return jsonify({
        'recommended_crop': recommended_crop,
        'fertilizer': recommendations['fertilizer'],
        'pesticide': recommendations['pesticide']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
