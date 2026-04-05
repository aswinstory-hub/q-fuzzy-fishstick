# Flask Cheatsheet (Basics → Intermediate)

## 1. Install

```bash
pip install flask
```

---

## 2. Minimal App

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask"

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 3. Routes

```python
@app.route("/about")
def about():
    return "About page"

@app.route("/user/<name>")
def user(name):
    return f"Hello {name}"
```

---

## 4. JSON Response

```python
from flask import jsonify

@app.route("/data")
def data():
    return jsonify({
        "price": 100,
        "signal": "BUY"
    })
```

---

## 5. Query Params (GET)

```python
from flask import request

@app.route("/trade")
def trade():
    symbol = request.args.get("symbol")
    return f"Trading {symbol}"
```

Example:

```
/trade?symbol=NIFTY
```

---

## 6. POST Request

```python
from flask import request, jsonify

@app.route("/trade", methods=["POST"])
def trade():
    data = request.get_json()

    symbol = data.get("symbol")
    qty = data.get("qty")

    return jsonify({
        "message": f"Order placed for {symbol}",
        "quantity": qty
    })
```

---

## 7. Validation + Status Codes

```python
@app.route("/trade", methods=["POST"])
def trade():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data"}), 400

    symbol = data.get("symbol")
    qty = data.get("qty")

    if not symbol or not qty:
        return jsonify({"error": "Missing fields"}), 400

    return jsonify({"status": "ok"})
```

---

## 8. Project Structure

```
project/
│
├── app.py
├── routes/
│   └── trade.py
├── services/
│   └── strategy.py
└── models/
    └── data.py
```

---

## 9. Blueprint (Modular Routes)

### routes/trade.py

```python
from flask import Blueprint, request, jsonify

trade_bp = Blueprint("trade", __name__)

@trade_bp.route("/trade", methods=["POST"])
def trade():
    return jsonify({"status": "ok"})
```

### app.py

```python
from flask import Flask
from routes.trade import trade_bp

app = Flask(__name__)
app.register_blueprint(trade_bp)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 10. Example: Connect Logic

```python
def generate_signal(price):
    if price > 100:
        return "SELL"
    return "BUY"

@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json()
    price = data.get("price")

    signal = generate_signal(price)

    return jsonify({
        "price": price,
        "signal": signal
    })
```

---

## 11. Testing (curl)

```bash
curl -X POST http://127.0.0.1:5000/trade \
-H "Content-Type: application/json" \
-d '{"symbol": "NIFTY", "qty": 50}'
```

---

## 12. Key Concepts Summary

* Routes map URL → function
* Functions return response
* GET = read (query params)
* POST = send data (JSON body)
* Use jsonify for APIs
* Validate inputs
* Use Blueprints for structure

---

## 13. Common Mistakes

* Forgetting methods=["POST"]
* Using request.args for POST
* No validation
* One giant file
* Hardcoding logic inside routes

---

## 14. Next Topics

* Databases (SQLite, PostgreSQL)
* Authentication
* Logging
* Deployment
