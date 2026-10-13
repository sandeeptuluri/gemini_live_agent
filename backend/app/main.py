import os
from fastapi import FastAPI, WebSocket
from google import genai
from app.agents.interview_agent import InterviewAgent
from app.agents.coach_agent import CoachAgent
from app.services.medical_db import MedicalDB

app = FastAPI()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
db = MedicalDB()

@app.websocket("/ws/kinetic")
async def kinetic_flow(websocket: WebSocket):
    await websocket.accept()
    
    # -- STEP 1: INTERVIEW PHASE --
    interview = InterviewAgent(client)
    # (Logic here would handle the chat loop until 'PLAN_READY' is detected)
    
    # -- STEP 2: PLAN PREPARATION --
    # Mock data from interview summary
    medical_plan = db.get_safe_plan(target="mobility_recovery")
    
    # -- STEP 3 & 4: LIVE COACHING PHASE --
    coach = CoachAgent(client)
    async with await coach.start_session(medical_plan) as session:
        # Step 4: Live video/audio streaming loop
        async for message in websocket.iter_bytes():
            await session.send_realtime_input(message)
            # receive_from_gemini logic handles voice and visual_aid triggers