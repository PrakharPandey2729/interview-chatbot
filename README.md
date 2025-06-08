# 🤖 Rick Sanchez Interview Chatbot

<div align="center">
  <img src="techrickal.png" alt="Rick Sanchez Interview Bot" width="200"/>
  <br/>
  <em>Wubba Lubba Dub Dub! Let's get technical!</em>
</div>

## Documentation Index

- [Project Overview](#-project-overview)
- [Installation Instructions](#-installation-instructions)
- [Usage Guide](#-usage-guide)
- [Technical Details](#-technical-details)
- [Prompt Design](#-prompt-design)
- [Challenges & Solutions](#-challenges--solutions)
- [Development & Deployment](#-development--deployment)

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

## 🛠️ Technical Details

### Core Technologies

- **Frontend**: Streamlit 1.44.1
- **Backend**: FastAPI 0.115.12
- **AI Model**: OpenAI GPT-4 Turbo
- **State Management**: LangGraph 0.4.5
- **Database**: MongoDB Atlas
- **Containerization**: Docker

### Architecture Decisions

1. **LangGraph Implementation**

   The interview flow is managed through a directed graph with the following structure:

   ```mermaid
   %%{init: {"theme": "dark", "themeVariables": { "primaryColor": "#ff4c4c", "primaryTextColor": "#ffffff", "primaryBorderColor": "#ff4c4c", "lineColor": "#ffffff", "sectionBkgColor": "#1a1a1a", "altSectionBkgColor": "#2a2a2a", "gridColor": "#333333", "secondaryColor": "#a8c8ec", "tertiaryColor": "#1a1a1a"}}}%%
   graph TD
       %% Entry Points
       Start([__start__]) --> EntryRouter{determine_entry_point}

       %% Greeting Flow
       EntryRouter -->|No Greeting| GreetCandidate[Greet Candidate]
       EntryRouter -->|Has Response| GreetingResponse[Process Greeting]
       EntryRouter -->|Ready to Start| Evaluator[Evaluate Response]

       %% Greeting Response Flow
       GreetingResponse --> GreetRouter{greeting_response_router}
       GreetRouter -->|Not Ready| GreetCandidate
       GreetRouter -->|Ready| RickAgent[Generate Question]

       %% Main Interview Flow
       RickAgent --> End3([End - Show Question])
       Evaluator --> EvalRouter{evaluation_decision}
       EvalRouter -->|Relevant| FollowUpCheck[Check Follow-up]
       EvalRouter -->|Irrelevant/Gibberish| FallbackAgent[Generate Fallback]

       %% Follow-up Flow
       FollowUpCheck --> FollowUpRouter{followup_router}
       FollowUpRouter -->|Generated Follow-up| End1([End - Show Follow-up Question])
       FollowUpRouter -->|No Follow-up Generated| RickAgent

       %% Fallback Flow
       FallbackAgent --> FallbackRouter{fallback_router}
       FallbackRouter -->|More than 3 Attempts| RickAgent
       FallbackRouter -->|Normal Fallback| End2([End - Show Fallback Response])

       %% Legend
       Legend[Legend:<br/>🔷 Diamonds = Routing Functions<br/>📦 Rectangles = Process Nodes<br/>⭕ Circles = Terminal Nodes]

       %% Node Styles
       classDef process fill:#ff4c4c,stroke:#ffffff,stroke-width:2px,color:#ffffff
       classDef decision fill:#a8c8ec,stroke:#ffffff,stroke-width:2px,color:#000000
       classDef endpoint fill:#4ade80,stroke:#ffffff,stroke-width:2px,color:#000000
       classDef legend fill:#333333,stroke:#ffffff,stroke-width:1px,color:#ffffff

       class GreetCandidate,Evaluator,GreetingResponse,FollowUpCheck,FallbackAgent process
       class EntryRouter,GreetRouter,EvalRouter,FollowUpRouter,FallbackRouter decision
       class Start,End1,End2,End3,RickAgent endpoint
       class Legend legend
   ```

   Key Components:

   - **Entry Point Router**: Smart routing based on current state
   - **Greeting Flow**: Handles initial interaction and readiness check
   - **Question Generation**: Creates personalized technical questions
   - **Answer Evaluation**: Assesses response quality
   - **Follow-up System**: Generates context-aware follow-up questions
   - **Fallback System**: Handles poor or irrelevant responses
   - **State Persistence**: MongoDB checkpointing for conversation state

   The graph ensures:

   - Natural conversation flow
   - Context-aware question generation
   - Graceful error handling
   - State persistence across sessions
   - Concurrent user support

2. **API Design**

   - RESTful endpoints for interview management
   - WebSocket for real-time updates
   - Rate limiting and request validation
   - Error handling middleware
   - CORS configuration

3. **Database Schema**

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

   The schema uses a single collection `candidates` with embedded chat history. Key features:

   - Unique email constraint for registration
   - Embedded chat history with timestamps
   - Tech stack and experience tracking
   - Role preferences storage
   - MongoDB ObjectId as primary key

   Note: The LangGraph state is stored separately in MongoDB using the `langgraph-checkpoint-mongodb` package.

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

## 📊 Architecture

```
interview-chatbot/
├── app.py              # Streamlit frontend application
├── main.py            # FastAPI backend server
├── rick_agent.py      # Rick Sanchez AI agent implementation with LangGraph
├── requirements.txt   # Python dependencies
├── Dockerfile        # Container configuration
├── start_servers_locally.bat  # Windows local development script
├── build-and-deploy.bat      # Windows deployment script
└── .env             # Environment variables (not in repo)
```

## 🛠️ Development

### Project Structure

- `app.py`: Streamlit frontend with UI components and user interaction
- `main.py`: FastAPI backend handling API requests and business logic
- `rick_agent.py`: Core AI agent implementation with Rick's personality and LangGraph integration
- `requirements.txt`: Project dependencies including LangGraph and MongoDB checkpointing
- `Dockerfile`: Container configuration
- `start_servers_locally.bat`: Windows script for local development
- `build-and-deploy.bat`: Windows script for deployment

### Key Technical Components

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

3. **State Management**

   - MongoDB checkpointing for conversation state
   - Session persistence across server restarts
   - Candidate data storage and retrieval
   - Interview progress tracking
   - Error recovery mechanisms

4. **Security Features**

   - Environment variable protection
   - API key management
   - MongoDB Atlas integration
   - CORS protection
   - Rate limiting
   - Input validation and sanitization

5. **Development Tools**
   - Windows batch scripts for local development
   - Docker containerization
   - Cloud deployment automation
   - Environment configuration management
   - Logging and monitoring

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Submit a pull request

## 📝 API Documentation

The backend API is documented using FastAPI's automatic documentation. After starting the server, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

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
