import json

class Archivist:
    def __init__(self):
        self.session_logs = []

    def log_event(self, timestamp, event_type, data):
        self.session_logs.append({
            "time": timestamp,
            "type": event_type,
            "details": data
        })

    def generate_report(self):
        # In a real app, this would save to a database like MongoDB or PostgreSQL
        with open("patient_report.json", "w") as f:
            json.dump(self.session_logs, f)
        return "Report generated successfully."