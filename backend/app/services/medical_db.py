import requests
import os

class MedicalDB:
    def __init__(self):
        self.api_url = "https://exercisedb.p.rapidapi.com/exercises"
        self.headers = {
            "X-RapidAPI-Key": os.getenv("EXERCISE_DB_KEY"),
            "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
        }

    def get_exercises_by_target(self, target_muscle):
        # Fetching exercises specifically safe for medical recovery
        response = requests.get(f"{self.api_url}/target/{target_muscle}", headers=self.headers)
        return response.json()

    def get_safe_plan(self, constraints):
        # Logic to filter exercises based on ADHD/Paralysis needs
        # For now, we fetch basic bodyweight movements
        response = requests.get(f"{self.api_url}/equipment/body%20weight", headers=self.headers)
        return response.json()[:3] # Returns top 3 safe exercises