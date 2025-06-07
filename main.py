from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from rick_agent import interview_service

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Initialize FastAPI app
app = FastAPI(title="Interview Chatbot API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Connect to MongoDB - Use environment variable for production
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["interview_chatbot"]
candidates_collection = db["candidates"]

# Candidate Registration Model
class CandidateRegister(BaseModel):
    name: str
    email: str
    password: str

# Chat Request Model
class ChatRequest(BaseModel):
    message: str

class Experience(BaseModel):
    years: int
    months: int

class CandidateDetailsUpdate(BaseModel):
    tech_stack: list[str]
    experience: Experience
    interested_roles: list[str]

class LoginRequest(BaseModel):
    name: str
    email: str
    password: str

# Root EndpointS
@app.get("/")
def read_root():
    return {"message": "Welcome to the Rick Sanchez Interview Chatbot!"}

@app.post("/register")
def register_candidate(candidate: CandidateRegister):
    """Registers a new candidate and prompts for tech stack."""
    existing_candidate = candidates_collection.find_one({"email": candidate.email})
    if existing_candidate:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_candidate = {
        "name": candidate.name,
        "email": candidate.email,
        "password": candidate.password,  # 🔴 Hash in real apps!
        "status": "awaiting tech stack",
        "tech_stack": [],
        "chat_history": []  # Initialize empty chat history array
    }
    result = candidates_collection.insert_one(new_candidate)
    return {
    "message": "Registered successfully!",
    "candidate_id": str(result.inserted_id),
    "greeting": "Welcome to the Rick Sanchez interview bot! Please enter your tech stack to begin."
    }

@app.post("/login")
def login_user(credentials: LoginRequest):
    """Logs in a candidate by validating email and password."""
    user = candidates_collection.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user["password"] != credentials.password or user["name"].strip().lower() != credentials.name.strip().lower():
        raise HTTPException(status_code=401, detail="Incorrect password or name.")

    return {
        "candidate_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

@app.post("/start_interview/{candidate_id}")
def start_interview(candidate_id: str):
    """Start a Rick interview session."""
    try:
        obj_id = ObjectId(candidate_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid candidate ID format.")

    candidate = candidates_collection.find_one({"_id": obj_id})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    
    if not candidate.get("tech_stack"):
        raise HTTPException(status_code=400, detail="Tech stack is required to start the interview.")
    
    # Start a new interview session with all candidate details
    greeting = interview_service.start_interview(
        candidate_id=candidate_id,
        candidate_name=candidate["name"],
        tech_stack=candidate["tech_stack"],
        experience=candidate.get("experience", {"years": 0, "months": 0}),
        interested_roles=candidate.get("interested_roles", [])
    )
    
    # Store in chat history - remove any "Rick: " prefix if it exists
    if greeting.startswith("Rick: "):
        greeting = greeting[6:]
    
    # Add to candidate's chat_history array
    from datetime import datetime
    candidates_collection.update_one(
        {"_id": obj_id},
        {"$push": {"chat_history": {
            "user": "START_INTERVIEW",
            "bot": greeting,
            "timestamp": datetime.utcnow()
        }}}
    )
    
    return {"response": greeting}
    
@app.post("/chat/{candidate_id}")
def chat(candidate_id: str, request: ChatRequest):
    """Chat with Rick while linking conversation to a candidate."""
    try:
        obj_id = ObjectId(candidate_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid candidate ID format.")

    candidate = candidates_collection.find_one({"_id": obj_id})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    # Simplified tech stack check - just verify it exists
    if not candidate.get("tech_stack"):
        return {
            "response": "Tech stack is required to begin the interview. Please add your tech stack in your profile."
        }
    
    # Process the message with Rick
    try:
        rick_response = interview_service.process_message(
            candidate_id=candidate_id,
            message=request.message
        )
        
        # Remove "Rick: " prefix if it exists
        if rick_response.startswith("Rick: "):
            rick_response = rick_response[6:]
        
        # Store in candidate's chat history array
        from datetime import datetime
        candidates_collection.update_one(
            {"_id": obj_id},
            {"$push": {"chat_history": {
                "user": request.message,
                "bot": rick_response,
                "timestamp": datetime.utcnow()
            }}}
        )
        
        return {"response": rick_response}
    
    except ValueError as e:
        # Interview not started yet, start it
        if "No active interview" in str(e):
            greeting = interview_service.start_interview(
                candidate_id=candidate_id,
                candidate_name=candidate["name"],
                tech_stack=candidate["tech_stack"],
                experience=candidate.get("experience", {"years": 0, "months": 0}),
                interested_roles=candidate.get("interested_roles", [])
            )
            return {"response": greeting, "interview_started": True}
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/end_interview/{candidate_id}")
def end_interview(candidate_id: str):
    """End the Rick interview session and delete user from database."""
    try:
        # Convert candidate_id to ObjectId
        obj_id = ObjectId(candidate_id)
        
        # End the interview service session
        interview_service.end_interview(candidate_id)
        
        # Delete candidate from candidates collection (chat history is embedded, so this deletes everything)
        candidate_result = candidates_collection.delete_one({"_id": obj_id})
        
        return {
            "message": "Interview ended and user data deleted successfully",
            "deleted_candidate": candidate_result.deleted_count > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_full_details/{candidate_id}")
def update_full_details(candidate_id: str, update: CandidateDetailsUpdate):
    try:
        obj_id = ObjectId(candidate_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid candidate ID format.")

    candidate = candidates_collection.find_one({"_id": obj_id})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    candidates_collection.update_one(
        {"_id": obj_id},
        {"$set": {
            "tech_stack": update.tech_stack,
            "experience": update.experience.model_dump(),
            "interested_roles": update.interested_roles,
            "status": "registered"
        }}
    )
    return {"message": "Candidate details updated successfully!"}

@app.get("/history/{candidate_id}")
def get_chat_history(candidate_id: str):
    """Fetch chat history for a candidate."""
    try:
        obj_id = ObjectId(candidate_id)
        candidate = candidates_collection.find_one({"_id": obj_id}, {"chat_history": 1, "_id": 0})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found.")
        
        # Return chat history array (guaranteed to be in order)
        return {"chat_history": candidate.get("chat_history", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tech_stack/{candidate_id}")
def get_tech_stack(candidate_id: str):
    """Fetch tech stack of a candidate."""
    try:
        obj_id = ObjectId(candidate_id)
        candidate = candidates_collection.find_one({"_id": obj_id})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found.")
        return {"tech_stack": candidate.get("tech_stack", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
