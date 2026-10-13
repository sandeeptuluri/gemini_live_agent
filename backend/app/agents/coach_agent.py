import os
from google import genai
from google.genai import types

class CoachAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-live-2.5-flash-native-audio"
        
    def get_system_instructions(self, user_profile):
        """
        Tailors the coach's behavior based on medical needs (ADHD, Paralysis, etc.)
        """
        return f"""
        YOU ARE: A world-class Physical Therapist and Fitness Coach specializing in {user_profile}.
        
        YOUR GOAL: Watch the user's video feed and guide them through a safe, effective workout.
        
        RULES:
        1. SPATIAL AWARENESS: Before starting, ensure the user is fully visible in the frame.
        2. REAL-TIME CORRECTION: If you see form errors (e.g., knees caving, back arching), interrupt immediately via voice.
        3. ENCOURAGEMENT: Be supportive but strict about safety. 
        4. COUNTING: Count reps out loud only when a full range of motion is achieved.
        5. ADHD ADAPTATION: Keep instructions short, punchy, and use visual aid triggers frequently to maintain focus.
        
        TOOLS:
        - If the user is struggling to understand a movement, call 'show_visual_aid(exercise_name, error_type)'.
        """

    async def start_workout_session(self, user_profile):
        # Configure the Live Session
        config = types.LiveGenerationConfig(
            system_instruction=self.get_system_instructions(user_profile),
            response_modalities=["AUDIO"], # Gemini speaks back
            tools=[{
                "function_declarations": [
                    {
                        "name": "show_visual_aid",
                        "description": "Triggers a visual reference for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "exercise_name": {"type": "string"},
                                "error_type": {"type": "string"}
                            }
                        }
                    }
                ]
            }]
        )

        # Connect to the Multimodal Live API
        async with self.client.aio.live.connect(model=self.model_id, config=config) as session:
            print("Coach is online and watching...")
            # This session will now handle incoming video/audio from your React frontend
            # and send back real-time voice guidance.