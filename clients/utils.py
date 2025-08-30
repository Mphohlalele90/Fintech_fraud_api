from datetime import datetime, time
from geopy.distance import geodesic

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

class FraudDetector:
    @staticmethod
    def detect_unusual_time(client, transaction_time):
        try:
            trans_time = datetime.strptime(transaction_time, '%Y-%m-%d %H:%M:%S').time()
            start, end = client.normal_activity_start, client.normal_activity_end
            return not (time(start) <= trans_time <= time(end))
        except Exception:
            return False

    @staticmethod
    def detect_unusual_location(client, location):
        current_loc = (location['lat'], location['long'])
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
                sim_swap_date = client.sim_swap_date
                txn_date = datetime.strptime(transaction_time, "%Y-%m-%d %H:%M:%S").date()
                if (txn_date - sim_swap_date).days <= 7:
                    issues.append("RECENT_SIM_SWAP")
            except Exception:
                pass

        return issues

    @staticmethod
    def determine_risk_profile(risk_score):
        if risk_score <= RISK_PROFILE_THRESHOLDS["LOW"]:
            return "LOW"
        elif risk_score <= RISK_PROFILE_THRESHOLDS["MEDIUM"]:
            return "MEDIUM"
        elif risk_score <= RISK_PROFILE_THRESHOLDS["MED_HIGH"]:
            return "MED_HIGH"
        else:
            return "HIGH"
        
    @staticmethod
    def detect_phishing_or_spyware(client):
        incident = client.incident.lower() if client.incident else ""
        if "phishing" in incident or "spyware" in incident:
            return True
        return False

    @staticmethod
    def assess_fraud_risk(client, location, transaction_time=None, current_imsi=None, current_number=None):
        """
        Main method to assess fraud risk for a client
        Returns: risk_score, flags, risk_profile, message
        """
        risk_score = client.risk_score or 0
        flags = []
        
        detector = FraudDetector()
        
        # Phishing or spyware
        if detector.detect_phishing_or_spyware(client):
            flags.append("PHISHING_OR_SPYWARE")
            risk_score += RISK_SCORE_INCREMENT["PHISHING_OR_SPYWARE"]

        # Unusual time
        if transaction_time and detector.detect_unusual_time(client, transaction_time):
            flags.append("UNUSUAL_TIME")
            risk_score += RISK_SCORE_INCREMENT["UNUSUAL_TIME"]

        # Unusual location
        if detector.detect_unusual_location(client, location):
            flags.append("UNUSUAL_LOCATION")
            risk_score += RISK_SCORE_INCREMENT["UNUSUAL_LOCATION"]

        # SIM swap and number change
        if current_imsi and current_number and transaction_time:
            sim_issues = detector.detect_sim_swap(client, current_imsi, current_number, transaction_time)
            for issue in sim_issues:
                if issue in RISK_SCORE_INCREMENT:
                    flags.append(issue)
                    risk_score += RISK_SCORE_INCREMENT[issue]

        # Final risk assessment
        risk_profile = detector.determine_risk_profile(risk_score)
        
        if risk_score >= RISK_THRESHOLD:
            approved = False
            message = "High fraud risk detected"
        else:
            approved = True
            message = RISK_PROFILE_MESSAGES[risk_profile]

        return {
            "approved": approved,
            "risk_score": risk_score,
            "flags": flags,
            "risk_profile": risk_profile,
            "message": message
        }