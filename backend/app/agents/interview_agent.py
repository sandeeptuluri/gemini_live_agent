from google import genai
from google.genai import types

class InterviewAgent:
    def __init__(self, client):
        self.client = client
        self.model_id = "gemini-2.0-flash" # High reasoning for medical planning

    def get_intake_instructions(self):
        return """
        You are a Medical Intake Specialist for 'Project Kinetic'. 
        Goal: Interview the patient to create a safe workout plan.
        Steps:
        1. Ask about their specific physical condition (e.g., Paralysis level, recovery stage).
        2. Inquire about cognitive needs (e.g., ADHD focus cues).
        3. Once you have enough data, conclude by saying 'PLAN_READY' and summarize their constraints.
        """

    async def run_interview(self, user_input, history=[]):
        """
        Standard chat interaction for the intake phase.
        """
        response = await self.client.aio.models.generate_content(
            model=self.model_id,
            contents=history + [user_input],
            config=types.GenerateContentConfig(
                system_instruction=self.get_intake_instructions()
            )
        )
        return response.text