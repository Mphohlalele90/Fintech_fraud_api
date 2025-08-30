FinTech Fraud Detection API
A Django REST Framework API for detecting fraudulent loan applications using machine learning and behavioral analysis.

🚀 API Endpoints
Loan Request Assessment
POST /api/loan/request/

Assesses a loan application for potential fraud risks based on client behavior, location, device information, and transaction patterns.

Request Body
json
{
    "client_id": "string (required)",
    "location": {
        "lat": "float (required)",
        "long": "float (required)"
    },
    "transaction_time": "string (optional, format: YYYY-MM-DD HH:MM:SS)",
    "device_imsi": "string (optional)",
    "device_number": "string (optional)"
}
Example Request
bash
curl -X POST http://127.0.0.1:8000/api/loan/request/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "003",
    "location": {"lat": -26.2485, "long": 27.8540},
    "transaction_time": "2025-08-30 14:30:00",
    "device_imsi": "999999999999999",
    "device_number": "+27123456703"
  }'
Response
json
{
    "client_id": "003",
    "client_name": "Mike Mdlalose",
    "approved": true,
    "flags": [],
    "risk_score": 55,
    "risk_profile": "MED_HIGH",
    "message": "Medium-high risk - Manual review required"
}
📊 Risk Assessment Metrics
Risk Score Ranges
0-20: LOW RISK - Standard approval

21-40: MEDIUM RISK - Additional verification recommended

41-60: MEDIUM-HIGH RISK - Manual review required

61-100: HIGH RISK - Automatic rejection

Fraud Detection Flags
UNUSUAL_TIME: Transaction outside normal activity hours

UNUSUAL_LOCATION: Transaction >30km from usual locations

SIM_CHANGED: Device IMSI different from registered IMSI

NUMBER_CHANGED: Device number different from registered number

RECENT_SIM_SWAP: SIM swap within last 7 days

PHISHING_OR_SPYWARE: Previous phishing/spyware incidents

🏦 Sample Client Data
Client ID	Name	Risk Score	Incident
001	Thabo Radebe	10	None
002	Jenny Van Tonder	8	None
003	Mike Mdlalose	55	Suspicious SIM swap
004	Lerato Mofokeng	60	SIM swap before loan request
005	Robyn Du Ploy	90	Unusual location & time
006	Lauren London	75	Phishing incident
🔧 Installation & Setup
Clone repository

bash
git clone <repository-url>
cd fintech_fraud_detection
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies

bash
pip install -r requirements.txt
Run migrations

bash
python manage.py migrate
Create superuser

bash
python manage.py createsuperuser
Run development server

bash
python manage.py runserver
📋 API Usage Examples
Example 1: Low Risk Application
Request:

json
{
    "client_id": "001",
    "location": {"lat": -25.9992, "long": 28.1286},
    "transaction_time": "2025-08-30 14:30:00"
}
Response:

json
{
    "client_id": "001",
    "client_name": "Thabo Radebe",
    "approved": true,
    "flags": [],
    "risk_score": 10,
    "risk_profile": "LOW",
    "message": "Low risk - Standard approval"
}
Example 2: High Risk Application
Request:

json
{
    "client_id": "005",
    "location": {"lat": -29.5383, "long": 31.2140},
    "transaction_time": "2025-08-30 02:30:00"
}
Response:

json
{
    "client_id": "005",
    "client_name": "Robyn Du Ploy",
    "approved": false,
    "flags": ["UNUSUAL_TIME", "UNUSUAL_LOCATION"],
    "risk_score": 90,
    "risk_profile": "HIGH", 
    "message": "High fraud risk detected"
}
🛠️ Technologies Used
Backend: Django REST Framework

Database: SQLite (development) / PostgreSQL (production)

Geolocation: geopy for distance calculations

Authentication: JWT Tokens

Testing: Django Test Framework

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing-feature)

Open a Pull Request

📞 Support


Note: This is a development version. For production use, ensure proper security measures, database optimization, and additional fraud detection mechanisms are implemented.
