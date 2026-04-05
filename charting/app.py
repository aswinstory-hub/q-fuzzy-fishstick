from flask import Flask
from flask import jsonify 
from flask import request

def generate_signal(price):
    if price > 100:
        return "SELL"
    return "BUY"

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is Flask"

@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json()
    price = data.get("price")

    signal = generate_signal(price)

    return jsonify({
        "price": price,
        "signal": signal
    })

if __name__ == "__main__":
    app.run(debug=True)
