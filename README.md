Crypto Scan Dashboard v2

A modern, responsive cryptocurrency trading dashboard that displays real-time market data, trading signals, and volatility analysis.

Features

· Real-time Data: Fetches cryptocurrency data from a Flask backend server
· Trading Signals: Displays BUY/SELL/HOLD signals with color-coded indicators
· Volatility Analysis: Provides volatility notes based on score metrics
· Interactive Charts: Visualizes price, volume, and momentum data using Chart.js
· Advanced Filtering: Filter by coin, signal type, and volatility level
· Responsive Design: Works seamlessly on desktop and mobile devices
· Dark/Light Mode: Toggle between color themes for comfortable viewing
· Data Export: Export filtered data to CSV format
· Auto-refresh: Automatically updates data every 60 seconds

Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd crypto-scan-dashboard
```

1. Set up the Flask backend server (ensure Python is installed):

```bash
# Install required packages
pip install flask flask-cors

# Run the server
python app.py
```

1. Open the index.html file in a web browser or serve it through a local web server.

Usage

1. Viewing Data: The dashboard automatically loads data from the Flask server
2. Filtering: Use the search box and dropdown filters to find specific coins or signals
3. Sorting: Click on column headers to sort data by that column
4. Charts: View visual representations of the top 10 coins by score
5. Export: Click the "Export CSV" button to download current data
6. Theme Toggle: Use the moon/sun icon to switch between dark and light modes

API Endpoints

The dashboard expects a Flask server with the following endpoint:

· GET /api/data - Returns cryptocurrency data in JSON format

Example response format:

```json
[
  {
    "coin": "BTC",
    "signal": "BUY",
    "price": 85000,
    "volume": 2500000000,
    "momentum": 5.2,
    "next_price": 89500,
    "score": 92,
    "timestamp": "20250909_145719"
  }
]
```

Project Structure

```
crypto-scan-dashboard/
├── index.html          # Main dashboard interface
├── app.py             # Flask server (to be created)
├── README.md          # Project documentation
└── assets/            # Optional folder for images/styles
```

Technologies Used

· HTML5, CSS3, JavaScript (ES6)
· Chart.js for data visualization
· Flask for backend API
· Responsive CSS Grid and Flexbox layouts

Browser Support

This dashboard supports all modern browsers including:

· Chrome (recommended)
· Firefox
· Safari
· Edge

License

This project is open source and available under the MIT License.
