from datetime import datetime, time
from geopy.distance import geodesic

class FraudDetector:
    RISK_SCORE_INCREMENT = {
        "UNUSUAL_TIME": 15,
        "UNUSUAL_LOCATION": 20,
        "SIM_CHANGED": 25,
        "NUMBER_CHANGED": 25,
        "RECENT_SIM_SWAP": 10,
        "PHISHING_OR_SPYWARE": 15
    }

    RISK_THRESHOLD = 70

    RISK_PROFILE_THRESHOLDS = {
        "LOW": 20,
        "MEDIUM": 40,
        "MED_HIGH": 60,
        "HIGH": 100
    }

    RISK_PROFILE_MESSAGES = {
        "LOW": "Low risk - Standard approval",
        "MEDIUM": "Medium risk - Additional verification recommended",
        "MED_HIGH": "Medium-high risk - Manual review required",
        "HIGH": "High risk - Automatic rejection"
    }

    @staticmethod
    def detect_unusual_time(client, transaction_time):
        try:
            trans_time = transaction_time.time()
            start = client.normal_activity_start
            end = client.normal_activity_end
            return not (start <= trans_time <= end)
        except Exception:
            return False

    @staticmethod
    def detect_unusual_location(client, location_lat, location_long):
        current_loc = (location_lat, location_long)
        usual_locations = [(client.latitude, client.longitude)]
        return all(geodesic(current_loc, loc).km > 30 for loc in usual_locations)

    @staticmethod
    def detect_sim_swap(client, current_imsi, current_number, transaction_time):
        issues = []

        if current_imsi and current_imsi != client.imsi:
            issues.append("SIM_CHANGED")
        if current_number and current_number != client.phone_number:
            issues.append("NUMBER_CHANGED")

        if client.sim_swap and client.sim_swap_date:
            try:
                if (transaction_time.date() - client.sim_swap_date).days <= 7:
                    issues.append("RECENT_SIM_SWAP")
            except Exception:
                pass

        return issues

    @staticmethod
    def determine_risk_profile(risk_score):
        if risk_score <= FraudDetector.RISK_PROFILE_THRESHOLDS["LOW"]:
            return "LOW"
        elif risk_score <= FraudDetector.RISK_PROFILE_THRESHOLDS["MEDIUM"]:
            return "MEDIUM"
        elif risk_score <= FraudDetector.RISK_PROFILE_THRESHOLDS["MED_HIGH"]:
            return "MED_HIGH"
        else:
            return "HIGH"
        
    @staticmethod
    def detect_phishing_or_spyware(client):
        incident = client.incident.lower()
        if "phishing" in incident or "spyware" in incident:
            return True
        return False

    @classmethod
    def analyze_transaction(cls, client, transaction_data):
        risk_score = client.risk_score
        flags = []
        
        # Phishing or spyware
        if cls.detect_phishing_or_spyware(client):
            flags.append("PHISHING_OR_SPYWARE")
            risk_score += cls.RISK_SCORE_INCREMENT.get("PHISHING_OR_SPYWARE", 15)

        # Unusual time
        if cls.detect_unusual_time(client, transaction_data['transaction_time']):
            flags.append("UNUSUAL_TIME")
            risk_score += cls.RISK_SCORE_INCREMENT["UNUSUAL_TIME"]

        # Unusual location
        if cls.detect_unusual_location(client, transaction_data['location_lat'], transaction_data['location_long']):
            flags.append("UNUSUAL_LOCATION")
            risk_score += cls.RISK_SCORE_INCREMENT["UNUSUAL_LOCATION"]

        # SIM swap and number change
        issues = cls.detect_sim_swap(
            client, 
            transaction_data['device_imsi'], 
            transaction_data['device_number'], 
            transaction_data['transaction_time']
        )
        for issue in issues:
            if issue in cls.RISK_SCORE_INCREMENT:
                flags.append(issue)
                risk_score += cls.RISK_SCORE_INCREMENT[issue]

        # Final risk assessment
        risk_profile = cls.determine_risk_profile(risk_score)
        approved = risk_score < cls.RISK_THRESHOLD
        
        return {
            "risk_score": risk_score,
            "risk_profile": risk_profile,
            "flags": flags,
            "approved": approved,
            "message": cls.RISK_PROFILE_MESSAGES[risk_profile] if approved else "High fraud risk detected"
        }