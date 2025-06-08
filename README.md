# 🤖 Rick Sanchez Interview Chatbot

<div align="center">
  <img src="techrickal.png" alt="Rick Sanchez Interview Bot" width="200"/>
  <br/>
  <em>Wubba Lubba Dub Dub! Let's get technical!</em>
</div>

## Documentation Index

- [Project Overview](#-project-overview)
- [Installation Instructions](#-installation-instructions)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Prompt Design](#-prompt-design)
- [Technical Architecture](#-technical-architecture)
- [Challenges & Solutions](#-challenges--solutions)

## Project Overview

The Rick Sanchez Interview Chatbot is an AI-powered technical interview assistant that revolutionizes the initial screening process. Built with a unique Rick and Morty personality twist, it combines advanced AI technology with professional interview techniques to create an engaging and efficient candidate screening experience.

### Core Capabilities

- **Intelligent Screening**: Conducts preliminary technical interviews with human-like interaction
- **Personality-Driven**: Maintains Rick Sanchez's unique personality while staying professional
- **Dynamic Adaptation**: Adjusts questions based on candidate's tech stack and experience level
- **State Management**: Maintains conversation context and progress using LangGraph
- **Data Persistence**: Securely stores interview responses for later review
- **Multi-Platform**: Accessible via web interface with responsive design

### Technical Architecture

- **Frontend**: Streamlit-based responsive web interface
- **Backend**: FastAPI server with WebSocket support
- **AI Engine**: OpenAI GPT-4 Turbo with custom prompt engineering
- **State Management**: LangGraph with MongoDB checkpointing
- **Database**: MongoDB Atlas for persistent storage
- **Deployment**: Docker containerization with Google Cloud Run

### 🌟 Key Features

- **🤖 AI-Powered Interviews**

  - Powered by OpenAI's GPT-4 Turbo for intelligent conversation
  - Custom-trained to maintain Rick Sanchez's personality while conducting professional interviews
  - Context-aware responses and follow-up questions
  - **LangGraph Integration** for sophisticated conversation state management and flow control
  - MongoDB checkpointing for persistent conversation state

- **💻 Modern Tech Stack**

  - Frontend: Streamlit for a sleek, responsive UI
  - Backend: FastAPI for robust API handling
  - Database: MongoDB for secure data storage
  - Containerized with Docker for easy deployment
  - **LangGraph** for advanced conversation orchestration
  - **LangGraph MongoDB Checkpointing** for state persistence

- **🎯 Interview Features**

  - Dynamic candidate onboarding
  - Tech stack-based question generation
  - Experience level adaptation
  - Real-time conversation history
  - Audio feedback (Rick's iconic catchphrases)
  - Comprehensive response storage

- **🔒 Security & Privacy**
  - Secure API key management
  - Environment variable protection
  - MongoDB Atlas integration
  - CORS protection
  - Data encryption

## Installation Instructions

### Prerequisites

- **Required**: Python 3.8+, Git, OpenAI API key
- **Database**: MongoDB Atlas account (free tier available)
- **Optional**: Docker (for containerization)

## 🏠 Local Development Setup

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/PrakharPandey2729/interview-chatbot.git
cd interview-chatbot

# Create and activate virtual environment
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

- Create MongoDB Atlas account at [MongoDB Atlas](https://www.mongodb.com/atlas)
- Set up a free cluster:
  - Choose "Shared" (free tier)
  - Select region (same as your deployment region)
  - Create cluster
- Configure database access:
  - Go to "Database Access"
  - Add new user with username/password
  - Grant "Atlas admin" privileges
- Set up network access:
  - Go to "Network Access"
  - Add IP address: `0.0.0.0/0` (for development)
- Get connection string:
  - Go to "Database" → "Connect" → "Connect your application"
  - Copy the connection string: `mongodb+srv://username:password@cluster.mongodb.net/`

### 3. Configuration

Create a `.env` file with required variables:

```env
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_mongodb_connection_string
BACKEND_URL=http://127.0.0.1:8000
```

## ☁️ Cloud Deployment Setup

### Google Cloud Run Deployment

The application is designed for easy deployment to Google Cloud Run. See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

**Quick Cloud Deployment**:

```bash
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/interview-chatbot
gcloud run deploy interview-chatbot \
  --image gcr.io/YOUR-PROJECT-ID/interview-chatbot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Production Environment Variables**:

```env
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_production_mongodb_connection_string
PORT=8000
```

## 🚀 Quick Start

### Option 1: Local Development (Recommended for Testing)

```bash
# 1. Clone and setup
git clone https://github.com/PrakharPandey2729/interview-chatbot.git
cd interview-chatbot
python -m venv venv && .\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Configure environment (create .env file)
OPENAI_API_KEY=your_key_here
MONGO_URI=your_mongodb_connection_string

# 3. Start both servers (Windows)
start_servers_locally.bat
# Access: http://localhost:8501
```

### Option 2: Cloud Deployment

```bash
# Deploy to Google Cloud Run - follow the detailed cloud deployment guide above
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/interview-chatbot
gcloud run deploy interview-chatbot \
  --image gcr.io/YOUR-PROJECT-ID/interview-chatbot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📖 Usage Guide

### Starting an Interview

1. Access the web interface at `http://localhost:8501`
2. **Login/Register**:

   - Enter your name, email, and password
   - New users will be registered automatically
   - Existing users will be logged in

3. **Tech Stack Setup** (for new users):

   - Enter your technical experience (e.g., "I've worked with Python, React, and AWS")
   - The system will automatically detect and extract technologies
   - Select your years and months of experience
   - Choose your interested roles (e.g., Frontend Developer, Backend Developer, etc.)
   - Review and confirm your details

4. **Interview Session**:
   - Click "Start Interview" to begin
   - Rick will greet you with his characteristic style
   - Answer technical questions based on your tech stack
   - Use the chat interface to respond
   - Access interview controls (logout, end interview) in the settings panel

### Interview Controls

- **End Interview**: Ends the session and logs you out
- **Log Out**: Logs out while preserving your session
- **Returning Users**: Your previous conversation will be loaded automatically

### Key Features

- Dynamic question generation based on your tech stack
- Experience-level appropriate questions
- Context-aware follow-up questions
- Persistent conversation history
- Rick's unique personality and style

## 🏗️ Technical Architecture

### Core Technologies Stack

- **Frontend**: Streamlit 1.44.1 with responsive UI components
- **Backend**: FastAPI 0.115.12 with async request handling
- **AI Engine**: OpenAI GPT-4 Turbo with custom prompt engineering
- **State Management**: LangGraph 0.4.5 with directed graph orchestration
- **Database**: MongoDB Atlas with embedded document structure
- **Persistence**: LangGraph MongoDB checkpointing for conversation state
- **Containerization**: Docker with multi-stage builds
- **Deployment**: Google Cloud Run with auto-scaling

### Project Structure

```
interview-chatbot/
├── app.py                        # Streamlit frontend application
├── main.py                      # FastAPI backend server
├── rick_agent.py               # Rick Sanchez AI agent with LangGraph
├── requirements.txt            # Python dependencies
├── Dockerfile                 # Container configuration
├── start_servers_locally.bat # Windows local development script
└── .env                      # Environment variables (not in repo)
```

### LangGraph Conversation Flow

The interview flow is managed through a sophisticated directed graph:

```mermaid
%%{init: {"theme": "dark", "themeVariables": { "primaryColor": "#ff4c4c", "primaryTextColor": "#ffffff", "primaryBorderColor": "#ff4c4c", "lineColor": "#ffffff", "sectionBkgColor": "#1a1a1a", "altSectionBkgColor": "#2a2a2a", "gridColor": "#333333", "secondaryColor": "#a8c8ec", "tertiaryColor": "#1a1a1a"}}}%%
graph TD
    %% Entry Points
    Start([__start__]) --> EntryRouter{determine_entry_point}

    %% Interview State - Central state management
    InterviewState[(Interview State<br/>• candidate_name<br/>• tech_stack<br/>• experience<br/>• interested_roles<br/>• current_question_index<br/>• questions<br/>• history<br/>• last_response<br/>• greeting_done<br/>• ready_to_start<br/>• current_base_question<br/>• follow_up_count<br/>• current_thread<br/>• fallback_attempts<br/>• last_evaluation<br/>• _routing)]

    %% Greeting Flow
    EntryRouter -->|No Greeting| GreetCandidate[Greet Candidate]
    EntryRouter -->|Has Response| GreetingResponse[Process Greeting]
    EntryRouter -->|Ready to Start| Evaluator[Evaluate Response]

    %% State flows through all nodes
    InterviewState -.-> GreetCandidate
    InterviewState -.-> GreetingResponse
    InterviewState -.-> RickAgent
    InterviewState -.-> Evaluator
    InterviewState -.-> FollowUpCheck
    InterviewState -.-> FallbackAgent

    %% Greeting Response Flow
    GreetingResponse --> GreetRouter{greeting_response_router}
    GreetRouter -->|Not Ready| GreetCandidate
    GreetRouter -->|Ready| RickAgent[Generate Question]

    %% Main Interview Flow
    Evaluator --> EvalRouter{evaluation_decision}
    EvalRouter -->|Relevant| FollowUpCheck[Check Follow-up]
    EvalRouter -->|Irrelevant/Gibberish| FallbackAgent[Generate Fallback]

    %% Follow-up Flow
    FollowUpCheck --> FollowUpRouter{followup_router}
    FollowUpRouter -->|Generated Follow-up| End1([End])
    FollowUpRouter -->|No Follow-up Generated| RickAgent

    %% Fallback Flow
    FallbackAgent --> FallbackRouter{fallback_router}
    FallbackRouter -->|More than 3 Attempts| RickAgent
    FallbackRouter -->|Normal Fallback| End2([End])

    %% Legend
    Legend[Legend:<br/>🔷 Diamonds = Routing Functions<br/>📦 Rectangles = Process Nodes<br/>⭕ Circles = Terminal Nodes<br/>🗄️ Cylinder = Shared State]

    %% Node Styles
    classDef process fill:#ff4c4c,stroke:#ffffff,stroke-width:2px,color:#ffffff
    classDef decision fill:#a8c8ec,stroke:#ffffff,stroke-width:2px,color:#000000
    classDef endpoint fill:#4ade80,stroke:#ffffff,stroke-width:2px,color:#000000
    classDef state fill:#fbbf24,stroke:#ffffff,stroke-width:2px,color:#000000
    classDef legend fill:#333333,stroke:#ffffff,stroke-width:1px,color:#ffffff

    class GreetCandidate,Evaluator,GreetingResponse,FollowUpCheck,FallbackAgent,RickAgent process
    class EntryRouter,GreetRouter,EvalRouter,FollowUpRouter,FallbackRouter decision
    class Start,End1,End2,End3 endpoint
    class InterviewState state
    class Legend legend
```

**Key Components:**

- **Entry Point Router**: Smart routing based on current state
- **Greeting Flow**: Handles initial interaction and readiness check
- **Question Generation**: Creates personalized technical questions
- **Answer Evaluation**: Assesses response quality
- **Follow-up System**: Generates context-aware follow-up questions
- **Fallback System**: Handles poor or irrelevant responses
- **State Persistence**: MongoDB checkpointing for conversation state

### Interview State Structure

The complete Interview State that flows through all LangGraph nodes:

```python
class InterviewState(TypedDict):
    # Candidate Information
    candidate_name: str                    # Candidate's full name
    tech_stack: List[str]                 # Technologies they work with
    experience: dict                      # Years and months of experience
    interested_roles: List[str]           # Roles they're interested in

    # Interview Progress
    current_question_index: int           # Index of current question
    questions: List[str]                  # List of generated questions
    history: List[dict]                   # Full conversation history
    last_response: str                    # Last user/bot response

    # Flow Control
    greeting_done: bool                   # Whether greeting is complete
    ready_to_start: bool                 # Whether candidate is ready
    current_base_question: str           # Current main question
    follow_up_count: int                 # Number of follow-ups asked
    current_thread: List[dict]           # Current question thread
    fallback_attempts: int               # Number of fallback attempts
    last_evaluation: str                 # Last answer evaluation result
    _routing: str                        # Internal routing information
```

This state structure enables:

- **Conversation Continuity**: Maintains context across all interactions
- **Dynamic Question Generation**: Adapts questions based on candidate profile
- **Thread Management**: Tracks follow-up questions and conversation threads
- **Error Recovery**: Handles fallback scenarios and routing decisions

### Core System Components

1. **LangGraph Integration**

   - Sophisticated conversation state management
   - Directed acyclic graph (DAG) for interview flow control
   - State persistence using MongoDB checkpointing
   - Custom node definitions for interview stages
   - Error handling and recovery mechanisms

2. **Interview Flow Management**

   - Multi-stage interview process
   - Dynamic question generation based on tech stack
   - Experience level adaptation
   - Context preservation across sessions
   - Graceful conversation termination

3. **API Design**

   - RESTful endpoints for interview management
   - Rate limiting and request validation
   - Error handling middleware
   - CORS configuration
   - FastAPI automatic documentation

4. **Database Architecture**

   ```json
   {
     "candidates": {
       "_id": "ObjectId",
       "name": "string",
       "email": "string",
       "password": "string",
       "tech_stack": ["string"],
       "experience": {
         "years": "number",
         "months": "number"
       },
       "interested_roles": ["string"],
       "chat_history": [
         {
           "user": "string",
           "bot": "string",
           "timestamp": "datetime"
         }
       ]
     }
   }
   ```

   **Schema Features:**

   - Single collection design with embedded chat history
   - Unique email constraint for registration
   - Timestamped conversation tracking
   - Tech stack and experience modeling
   - Role preferences storage
   - LangGraph state stored separately via `langgraph-checkpoint-mongodb`

5. **Security & Performance Features**
   - Environment variable protection
   - API key management
   - MongoDB Atlas integration
   - CORS protection
   - Rate limiting
   - Input validation and sanitization
   - Token usage optimization
   - Response caching for common queries

### Development Tools

- **Local Development**: Windows batch scripts for server management
- **Containerization**: Docker with optimized multi-stage builds
- **Cloud Deployment**: Google Cloud Run with auto-scaling
- **API Documentation**: FastAPI automatic OpenAPI documentation
- **Environment Management**: `.env` file configuration
- **Monitoring**: Built-in logging and error tracking

### API Documentation

The backend API provides comprehensive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: Auto-generated with request/response models

## 🎨 Prompt Design

### Core Principles

1. **Personality Consistency**

   - Maintain Rick's unique voice while staying professional
   - Use appropriate catchphrases and references
   - Balance technical accuracy with character
   - Context-aware personality adaptation

2. **Interview Structure**

   ```python
   INTERVIEW_STAGES = {
       "greeting": "Initial welcome and overview",
       "candidate_info": "Collect basic information",
       "tech_stack": "Gather technical background",
       "technical_qa": "Dynamic question generation",
       "follow_up": "Context-aware follow-ups",
       "conclusion": "Summary and next steps"
   }
   ```

3. **Question Generation Strategy**

   - Tech stack-based question selection
   - Experience level adaptation
   - Progressive difficulty scaling
   - Context preservation
   - Dynamic follow-up generation
   - Quality validation checks

4. **Response Handling**
   - Input validation and sanitization
   - Error recovery mechanisms
   - Context maintenance
   - State persistence
   - Progress tracking
   - Graceful fallbacks

## 🎯 Challenges & Solutions

### 1. Conversation State Management

**Challenge**: Maintaining context across long conversations while preserving personality
**Solution**:

- Implemented LangGraph for sophisticated state management
- MongoDB checkpointing for persistent state storage
- Custom node definitions for each interview stage
- Error recovery and state restoration
- Concurrent user handling

### 2. Personality Consistency

**Challenge**: Balancing Rick's unique personality with professional interview conduct
**Solution**:

- Carefully crafted prompt templates with personality markers
- Context-aware personality adaptation
- Professional fallback mechanisms
- Response validation for tone consistency
- Dynamic personality intensity based on context

### 3. Technical Question Generation

**Challenge**: Generating relevant, difficulty-appropriate technical questions
**Solution**:

- Comprehensive tech stack to question category mapping
- Experience-based difficulty adjustment
- Dynamic follow-up question generation
- Question quality validation
- Response analysis for follow-ups

### 4. Performance Optimization

**Challenge**: Managing API costs and response times while maintaining quality
**Solution**:

- Efficient prompt engineering to reduce token usage
- Response caching for common queries
- Rate limiting implementation
- Token usage optimization
- Batch processing where applicable

### 5. Deployment Complexity

**Challenge**: Managing multiple services and dependencies across environments
**Solution**:

- Docker containerization for consistent environments
- Environment variable management
- Automated deployment scripts
- Cloud platform optimization
- Health check implementations

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔧 Troubleshooting

### Common Issues

1. **API Connection Errors**

   - Verify your OpenAI API key
   - Check MongoDB connection string
   - Ensure backend server is running

2. **Deployment Issues**

   - Check Google Cloud Run logs
   - Verify environment variables
   - Ensure Docker build succeeds

3. **Local Development**
   - Clear browser cache if UI issues occur
   - Check port availability (8000, 8501)
   - Verify virtual environment activation

## 📈 Performance & Scaling

- **Resource Requirements**

  - Memory: 2GB minimum (increased for LangGraph operations)
  - CPU: 1 vCPU minimum
  - Storage: 512MB minimum
  - MongoDB Atlas: Free tier sufficient for development

- **Scaling Considerations**
  - Horizontal scaling supported via Cloud Run
  - MongoDB Atlas handles database scaling
  - Rate limiting implemented for API protection
  - LangGraph state management optimized for concurrent users
  - Efficient token usage in conversation management

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">
  <em>Made with 💚 and a touch of Rick's genius</em>
  <br/>
  <sub>Remember: "To be fair, you have to have a very high IQ to understand this chatbot..."</sub>
</div>
