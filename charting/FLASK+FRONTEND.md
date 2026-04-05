# Flask Quant + Frontend Cheatsheet (Practical Build)

## 1. Project Structure

```
project/
│
├── app.py
├── templates/
│   └── index.html
├── routes/
│   ├── chart.py
│   ├── indicator.py
│   ├── signal.py
│   └── backtest.py
├── services/
│   ├── data.py
│   ├── indicators.py
│   ├── strategies.py
│   └── backtester.py
```

---

## 2. Serve Frontend (HTML)

### app.py

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 3. OHLC API (Chart Data)

```python
import yfinance as yf
from flask import jsonify

@app.route("/ohlc/<symbol>")
def ohlc(symbol):
    data = yf.download(symbol, period="5d", interval="5m")

    ohlc = []
    for index, row in data.iterrows():
        ohlc.append({
            "time": str(index),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"]
        })

    return jsonify(ohlc)
```

---

## 4. Indicator API (SMA)

```python
from flask import request, jsonify

@app.route("/indicator/sma", methods=["POST"])
def sma():
    data = request.get_json()

    prices = data["prices"]
    window = data.get("window", 14)

    sma = sum(prices[-window:]) / window

    return jsonify({"sma": sma})
```

---

## 5. Signal API

```python
@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json()

    price = data["price"]
    sma = data["sma"]

    signal = "BUY" if price > sma else "SELL"

    return jsonify({"signal": signal})
```

---

## 6. Backtest API

```python
@app.route("/backtest", methods=["POST"])
def backtest():
    data = request.get_json()

    prices = data["prices"]

    capital = 100000
    position = 0

    avg_price = sum(prices) / len(prices)

    for price in prices:
        if price > avg_price:
            if position == 0:
                position = capital / price
                capital = 0
        else:
            if position > 0:
                capital = position * price
                position = 0

    final_value = capital + position * prices[-1]

    return jsonify({"final_value": final_value})
```

---

## 7. DataFrame → JSON API

```python
import pandas as pd

@app.route("/data")
def data():
    df = pd.DataFrame({
        "price": [100, 101, 102],
        "signal": ["BUY", "SELL", "BUY"]
    })

    return jsonify(df.to_dict(orient="records"))
```

---

## 8. Frontend (index.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Quant App</title>
</head>
<body>

<h2>Quant Dashboard</h2>

<button onclick="loadData()">Load Table</button>
<button onclick="loadChart()">Load Chart</button>

<div id="table"></div>
<div id="chart" style="height:400px"></div>

<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>

<script>

function loadData() {
    fetch('/data')
    .then(res => res.json())
    .then(data => {
        let html = "<table border='1'>";
        data.forEach(row => {
            html += `<tr><td>${row.price}</td><td>${row.signal}</td></tr>`;
        });
        html += "</table>";
        document.getElementById("table").innerHTML = html;
    });
}

function loadChart() {
    const chart = LightweightCharts.createChart(document.getElementById('chart'));

    fetch('/ohlc/NIFTY')
    .then(res => res.json())
    .then(data => {
        const candleSeries = chart.addCandlestickSeries();
        candleSeries.setData(data);
    });
}

</script>

</body>
</html>
```

---

## 9. Frontend → Backend Flow

```
Button click → JS fetch() → Flask API → JSON → Render UI
```

---

## 10. Key Rules (Don’t Ignore)

* Flask = data layer only
* JS = UI + charts
* Never use matplotlib for web charts
* Always return JSON for frontend
* Keep logic in services, not routes

---

## 11. Build Order

1. OHLC API
2. Render chart
3. Add indicator API
4. Add signal API
5. Add backtest API
6. Improve UI

---

## 12. Future Additions

* WebSockets for live data
* Caching (Redis)
* Async jobs (Celery)
* Broker integration
