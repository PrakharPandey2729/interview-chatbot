# Interview Chatbot

## Project Overview
The Interview Chatbot is an AI-powered assistant designed to conduct preliminary technical interviews. It collects candidate details, asks tailored technical questions based on their tech stack, and stores responses for later review.

## Features
- **User Interface**: Built using Streamlit for an intuitive chat experience.
- **Chatbot Capabilities**:
  - Greets candidates and provides an overview.
  - Collects candidate details such as name, email, phone number, experience, and tech stack.
  - Generates technical questions based on declared tech stack.
  - Maintains conversation context and provides meaningful responses.
  - Gracefully ends the conversation with next-step details.
- **LLM Integration**: Uses OpenAI's GPT-4 Turbo API for conversation handling.
- **Data Storage**: Stores candidate responses for later review (MongoDB/local storage).
- **Deployment**: Initially runs locally; later deployed on AWS/GCP.

## Installation Instructions
### Prerequisites
- Python 3.8+
- Git
- OpenAI API key
- Streamlit

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/PrakharPandey2729/interview-chatbot.git
   cd interview-chatbot
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up OpenAI API key:
   ```sh
   export OPENAI_API_KEY=your_api_key_here  # Windows: set OPENAI_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```sh
   streamlit run app.py
   ```

## Usage Guide
- Open the Streamlit interface in the browser.
- Follow chatbot prompts to provide details and answer technical questions.
- Responses are stored for later review.

## Technical Details
- **Libraries**: Python, Streamlit, OpenAI API, MongoDB (optional for data storage)
- **Architecture**: Frontend in Streamlit, backend using OpenAI API, data handling with MongoDB/local files.
- **Prompt Design**: Carefully structured prompts for engaging and relevant interview questions.

## Challenges & Solutions
- **Handling unexpected responses**: Implemented fallback mechanisms to guide candidates.
- **Ensuring relevant technical questions**: Uses a mapping of tech stacks to question categories.
- **Efficient API usage**: Optimized prompt engineering to reduce token usage.

## Future Enhancements
- Deploy on AWS/GCP and provide a live demo link.
- Implement role-based access for interviewers to review responses.
- Add support for voice interactions.

## Contributing
Feel free to fork the repo, make changes, and submit pull requests!

## License
MIT License

