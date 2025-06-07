@echo off
REM Batch script to start both FastAPI and Streamlit servers
REM Navigate to the interview-chatbot directory and start both servers in separate CMD windows

echo Starting both servers...

REM Start FastAPI server (uvicorn) in a new CMD window
start "FastAPI Server" cmd /k "uvicorn main:app --reload"

REM Start Streamlit app in another new CMD window
start "Streamlit App" cmd /k "streamlit run app.py"

echo Started both servers:
echo - FastAPI server (uvicorn) running on http://localhost:8000
echo - Streamlit app running on http://localhost:8501
echo Both terminals will remain open. Close them manually when done.
pause 