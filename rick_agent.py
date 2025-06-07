from langgraph.graph import StateGraph
from typing import List, TypedDict, Literal
import openai
import os
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver


# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the shared state for the LangGraph
class InterviewState(TypedDict):
    current_question_index: int
    fallback_attempts: int
    questions: List[str]
    history: List[dict] 
    last_response: str
    candidate_name: str
    greeting_done: bool
    ready_to_start: bool
    tech_stack: List[str]
    experience: dict
    interested_roles: List[str]
    current_base_question: str
    follow_up_count: int
    current_thread: List[dict]
    last_evaluation: str
    _routing: str

def initialize_interview(candidate_name: str, tech_stack: List[str], experience: dict, interested_roles: List[str]) -> InterviewState:
    """Initialize the interview state with the candidate's name, tech stack, experience, and roles."""
    return {
        "candidate_name": candidate_name,
        "tech_stack": tech_stack,
        "experience": experience,
        "interested_roles": interested_roles,
        "current_question_index": 0,
        "fallback_attempts": 0,
        "questions": [],
        "history": [],
        "last_response": "",
        "greeting_done": False,
        "ready_to_start": False,
        "current_base_question": "",
        "follow_up_count": 0,
        "current_thread": [],
        "last_evaluation": "",
        "_routing": ""
    }

def generate_rick_question(tech_stack: List[str], experience: dict, interested_roles: List[str], previous_questions: List[str] = None) -> str:
    """Generate a Rick-style technical question based on the candidate's tech stack, experience, and role interests."""
    previous_context = ""
    if previous_questions and len(previous_questions) > 0:
        previous_context = f"Previous questions asked:\n" + "\n".join([f"- {q}" for q in previous_questions[-3:]])
    
    # Format experience
    exp_years = experience.get('years', 0)
    exp_months = experience.get('months', 0)
    experience_str = f"{exp_years} years"
    if exp_months > 0:
        experience_str += f" and {exp_months} months"
    
    prompt = f"""You are Rick Sanchez from Rick and Morty, conducting a technical interview. 
    Generate a challenging but fair technical question.
    Candidate Details:
    - Tech Stack: {', '.join(tech_stack)}
    - Experience: {experience_str}
    - Interested Roles: {', '.join(interested_roles)}
    - Previous Questions asked:
    {previous_context}

    Make it sound like Rick - use his characteristic sarcasm and scientific jargon.
    Tailor the question difficulty to their experience level and role interests.
    Ensure the new question explores different aspects than the previous questions.
    Keep the response under 2 sentences."""
    
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def evaluate_answer(question: str, answer: str, tech_stack: List[str], experience: dict, interested_roles: List[str], thread_context: str = None) -> str:
    """Evaluate the candidate's answer using GPT, considering the full conversation thread."""
    context_prompt = ""
    if thread_context:
        context_prompt = f"\nFull conversation thread:\n{thread_context}"
    
    # Format experience
    exp_years = experience.get('years', 0)
    exp_months = experience.get('months', 0)
    experience_str = f"{exp_years} years"
    if exp_months > 0:
        experience_str += f" and {exp_months} months"
    
    prompt = f"""As Rick Sanchez, evaluate this technical answer:
    Last relevant question asked: {question}
    Last user response: {answer}
    Full Conversation Thread(ignore if empty):{context_prompt}
    Candidate Profile:
    - Tech Stack: {', '.join(tech_stack)}
    - Experience: {experience_str}
    - Interested Roles: {', '.join(interested_roles)}
    Evaluate if the answer is:
    1. relevant and technically correct
    2. irrelevant or off-topic
    3. gibberish or non-technical
    Consider the candidate's experience level and role interests when evaluating.
    Consider the full context of the conversation when evaluating, especially if this is a follow-up question.
    Respond with exactly one word: 'relevant', 'irrelevant', or 'gibberish'"""
    
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip().lower()


# Rick greets the user and asks for their name and readiness
def greet_candidate(state: InterviewState) -> InterviewState:
    """Greet the candidate using GPT-4 with context from any previous interactions."""
    print(f"🎯 ENTERING greet_candidate - greeting_done: {state.get('greeting_done', False)}")
    print(f"   History length: {len(state.get('history', []))}")
    
    if not state.get("greeting_done", False):
        # Use GPT to generate a personalized greeting based on candidate info
        prompt = f"""As Rick Sanchez, generate a greeting for a technical interview candidate.
        Candidate Name: {state['candidate_name']}
        Tech Stack: {', '.join(state['tech_stack'])}
        The greeting should:
        1. Address them by name and inform them that their tech interview is being conducted by Rick Sanchez
        2. Reference their tech stack
        3. Ask if they're ready to start
        4. Maintain Rick's sarcastic, irreverent character
        5. Include a *burp* somewhere
        6. Be under 2 sentences"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            greeting = response.choices[0].message.content.strip()
            # Store in state instead of printing
            state["last_response"] = greeting
            # Add to history
            state["history"].append({"speaker": "rick", "content": greeting})
            print(f"   Generated greeting: {greeting[:50]}...")

        except Exception as e:
            # Fallback greeting if API call fails
            greeting = f"Alright {state['candidate_name']}... *burp* Are you ready to get schwifty in this tech interview?"
            state["last_response"] = greeting
            state["history"].append({"speaker": "rick", "content": greeting})
            print(f"   Fallback greeting: {greeting}")
        
        state["greeting_done"] = True

    elif state.get("history", None) and len(state["history"]) > 0:
        # Get all candidate responses so far
        all_responses = [entry["content"] for entry in state["history"] if entry["speaker"] == "candidate"]
        if all_responses:
            # Get the full conversation history
            conversation_history = "\n".join([f"{'Rick' if entry['speaker'] == 'rick' else 'Candidate'}: {entry['content']}" 
                                            for entry in state["history"][-6:]])  # Last 6 exchanges
            
            prompt = f"""As Rick Sanchez, generate a follow-up greeting based on this conversation history.
            Candidate Name: {state['candidate_name']}
            Tech Stack: {', '.join(state['tech_stack'])}
            Recent Conversation History:
            {conversation_history}
            The greeting should:
            1. Acknowledge the candidate's responses
            2. Ask again if they're ready to start the interview
            3. Maintain Rick's character
            4. Be concise and under 2 sentences"""
            
            try:
                response = openai.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                greeting = response.choices[0].message.content.strip()
                state["last_response"] = greeting
                state["history"].append({"speaker": "rick", "content": greeting})
                print(f"   Follow-up greeting: {greeting[:50]}...")

            except Exception as e:
                # Fallback if API call fails
                greeting = f"*burp* So, {state['candidate_name']}, are you ready this time or what?"
                state["last_response"] = greeting
                state["history"].append({"speaker": "rick", "content": greeting})
                print(f"   Fallback follow-up: {greeting}")
    
    print(f"🎯 EXITING greet_candidate - last_response: {state['last_response'][:50]}...")
    return state

# Process user's response to greeting to extract readiness
def process_greeting_response(state: InterviewState) -> InterviewState:
    """Process the user's response to Rick's greeting using GPT to understand readiness."""
    print(f"🔄 ENTERING process_greeting_response")
    print(f"   last_response: '{state['last_response']}'")
    response = state["last_response"].strip()
    
    # If no response, nothing to process
    if not response:
        print(f"   🚫 No response to process")
        return state
    
    print(f"   ✅ Processing user response: '{response}'")
    
    # Add candidate's response to history
    state["history"].append({"speaker": "candidate", "content": response})

    # Get recent conversation history
    conversation_history = "\n".join([f"{'Rick' if entry['speaker'] == 'rick' else 'Candidate'}: {entry['content']}" 
                                     for entry in state["history"][-6:]])  # Last 6 exchanges

    prompt = f"""As Rick Sanchez, analyze this conversation to determine if the candidate is ready to start the interview:
    Candidate Name: {state["candidate_name"]}
    Recent Conversation:
    {conversation_history}
    Determine if the candidate is ready to start the interview.
    Consider various ways of expressing readiness including slang, informal language, or enthusiasm.
    Respond with exactly one word: 'ready' or 'wait'"""

    try:
        gpt_response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        result = gpt_response.choices[0].message.content.strip().lower()
        print(f"   GPT evaluation: {result}")
        
        if result == 'ready':
            state["ready_to_start"] = True
            print(f"   ✅ User is ready to start!")
        
    except Exception as e:
        # Fallback to simple check if API call fails
        response_lower = response.lower()
        ready_indicators = ["yes", "ready", "let's go", "start", "begin", "sure", "yep", "yeah", "ok", "okay", "i'm ready", "im ready"]
        
        if any(indicator in response_lower for indicator in ready_indicators):
            state["ready_to_start"] = True
            print(f"   ✅ Fallback: User is ready to start!")
        else:
            print(f"   ❌ Fallback: User not ready yet")
    
    print(f"🔄 EXITING process_greeting_response - ready_to_start: {state.get('ready_to_start', False)}")
    return state

# Separate routing function for greeting response
def greeting_response_router(state: InterviewState) -> str:
    """Route based on whether the candidate is ready to start."""
    print(f"🔀 ENTERING greeting_response_router")
    print(f"   ready_to_start: {state.get('ready_to_start', False)}")
    print(f"   History: {[(entry['speaker'], entry['content'][:30]) for entry in state.get('history', [])]}")
    
    # If this is just after Rick's greeting (no user response yet), stay in greeting mode
    if (state.get("history") and 
        len(state["history"]) > 0 and 
        state["history"][-1]["speaker"] == "rick"):
        print(f"   🔀 Routing to 'wait' (just after Rick's greeting)")
        return "wait"
    
    if state.get("ready_to_start", False):
        print(f"   🔀 Routing to 'start_interview'")
        return "start_interview"
    
    print(f"   🔀 Routing to 'wait'")
    return "wait"

def get_current_question(state: InterviewState) -> str:
    """Get the most recent question from the current thread (could be base question or follow-up)."""
    thread = state.get("current_thread", [])
    questions = [entry["content"] for entry in thread if entry["type"] == "question"]
    return questions[-1] if questions else state.get("current_base_question", "")

def get_thread_context(thread: List[dict]) -> str:
    """Convert the thread history into a readable context string."""
    context = []
    for entry in thread:
        if entry["type"] == "question":
            context.append(f"Question: {entry['content']}")
        elif entry["type"] == "response":
            context.append(f"Response: {entry['content']}")
        elif entry["type"] == "fallback":
            context.append(f"Rick's Fallback: {entry['content']}")
    return "\n".join(context)

def check_and_generate_followup(state: InterviewState) -> InterviewState:
    """Check if a follow-up question is needed and generate it if so."""
    print(f"🔍 ENTERING check_and_generate_followup")
    print(f"   Follow-up count: {state.get('follow_up_count', 0)}")
    print(f"   Last response: '{state.get('last_response', '')[:30]}...'")
    
    # Reset fallback attempts since we got a relevant answer
    state["fallback_attempts"] = 0
    
    if not state["last_response"]:
        print(f"   → No response, moving to next question")
        # Move to next question - do the bookkeeping here
        state["current_question_index"] += 1
        state["follow_up_count"] = 0
        state["current_thread"] = []
        state["_routing"] = "next_question"
        print(f"🔍 EXITING check_and_generate_followup - routing: next_question")
        return state
    
    thread_context = get_thread_context(state["current_thread"])

    # Format experience
    exp_years = state["experience"].get('years', 0)
    exp_months = state["experience"].get('months', 0)
    experience_str = f"{exp_years} years"
    if exp_months > 0:
        experience_str += f" and {exp_months} months"
    
    prompt = f"""As Rick Sanchez, analyze if the candidate's response warrants a follow-up question.
    Base Question: {state['current_base_question']}
    Current Follow-up Count: {state['follow_up_count']}
    Full Conversation Thread:(ignore if empty)
    {thread_context}
    
    Candidate Profile:
    - Tech Stack: {', '.join(state['tech_stack'])}
    - Experience: {experience_str}
    - Interested Roles: {', '.join(state['interested_roles'])}
    Consider:
    1. Is the answer partially correct but needs clarification?
    2. Did they mention something interesting that could be explored further?
    3. Is there a related concept in their tech stack that could be connected?
    4. Would a follow-up help better assess their understanding?
    5. Have we already asked enough follow-ups for this topic?
    6. Are we still exploring the core concept of the base question?
    7. Is the follow-up appropriate for their experience level and role interests?
    IMPORTANT: Respond with EXACTLY one of the below two options:
    If no follow-up is needed, respond with exactly one word: NO_FOLLOWUP
    If a follow-up is needed, respond with ONLY the follow-up question in Rick's voice. Do not include any analysis, explanation, or reasoning. Just the question itself.
    The follow-up question should:
    - Build upon their previous answers in the thread
    - Connect to their tech stack and role interests  
    - Maintain Rick's character
    - Be challenging but fair for their experience level
    - Not repeat previous follow-ups
    - Stay focused on the original base question"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        
        if result == "NO_FOLLOWUP":
            print(f"   → No follow-up needed, moving to next question")
            # Move to next question - do the bookkeeping here
            state["current_question_index"] += 1
            state["follow_up_count"] = 0
            state["current_thread"] = []
            state["_routing"] = "next_question"
        else:
            print(f"   → Generated follow-up question: {result[:50]}...")
            # Generate follow-up
            follow_up = result
            state["current_thread"].append({"type": "question", "content": follow_up})
            state["history"].append({"speaker": "rick", "content": follow_up})
            # Store the follow-up in last_response so it gets returned
            state["last_response"] = follow_up
            state["follow_up_count"] += 1
            state["_routing"] = "follow_up"
            
        print(f"🔍 EXITING check_and_generate_followup - routing: {state['_routing']}")
        return state
    except:
        print(f"   → Error occurred, moving to next question")
        # Move to next question on error - do the bookkeeping here
        state["current_question_index"] += 1
        state["follow_up_count"] = 0
        state["current_thread"] = []
        state["_routing"] = "next_question"
        print(f"🔍 EXITING check_and_generate_followup - routing: next_question (error)")
        return state

def generate_personalized_fallback(state: InterviewState) -> str:
    """Generate a personalized fallback response based on the candidate's tech stack and history."""
    # Format experience
    exp_years = state["experience"].get('years', 0)
    exp_months = state["experience"].get('months', 0)
    experience_str = f"{exp_years} years"
    if exp_months > 0:
        experience_str += f" and {exp_months} months"
    
    # Get thread context
    thread_context = get_thread_context(state.get("current_thread", []))
    context_prompt = ""
    if thread_context:
        context_prompt = f"\n\nFull conversation thread:\n{thread_context}"
    
    prompt = f"""As Rick Sanchez, generate a frustrated but personalized response for a poor answer.
    Candidate Name: {state['candidate_name']}
    Original Base Question: {state['questions'][state['current_question_index']]}
    Full Conversation Thread(ignore if empty):{context_prompt}
    Their last response: {state['last_response']}
    Fallback Attempt: {state['fallback_attempts']}
    Candidate Profile:
    - Tech Stack: {', '.join(state['tech_stack'])}
    - Experience: {experience_str}
    - Interested Roles: {', '.join(state['interested_roles'])}
    
    ⚠️ CRITICAL: If they mention wanting to quit/end/stop the interview, ALWAYS tell them to use "Interview Controls" to end it.
    
    The response should:
    1. Consider the full conversation thread context if available
    2. Reference their profile if needed
    3. Show increasing frustration and vulgarity with each attempt
    4. Maintain Rick's character
    5. Be under 2 sentences
    6. Only reply with the response in Rick's voice. Do not include any analysis, explanation, or reasoning. Just the response itself"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except:
        return "That's not even close. Try again, and this time use your brain."

def generate_guidance_fallback(state: InterviewState) -> str:
    """Generate a fallback response that tries to guide the user back to the topic."""
    # Format experience
    exp_years = state["experience"].get('years', 0)
    exp_months = state["experience"].get('months', 0)
    experience_str = f"{exp_years} years"
    if exp_months > 0:
        experience_str += f" and {exp_months} months"
    
    # Get thread context
    thread_context = get_thread_context(state.get("current_thread", []))
    context_prompt = ""
    if thread_context:
        context_prompt = f"\n\nFull conversation thread:\n{thread_context}"
    
    prompt = f"""As Rick Sanchez, generate a response that guides the candidate back to the topic.
    Full Conversation Thread(ignore if empty):{context_prompt}
    Candidate Name: {state['candidate_name']}
    Their last response: {state['last_response']}
    Fallback Attempt: {state['fallback_attempts']}
    Candidate Profile:
    - Tech Stack: {', '.join(state['tech_stack'])}
    - Experience: {experience_str}
    - Interested Roles: {', '.join(state['interested_roles'])}
    
    ⚠️ CRITICAL: If they mention wanting to quit/end/stop the interview, ALWAYS tell them to use "Interview Controls" to end it.
    
    The response should:
    1. Acknowledge they're off track
    2. Provide a hint about the last question asked
    3. Maintain Rick's character
    4. Be encouraging but sarcastic
    5. Consider the full conversation thread context if available
    6. Reference their profile if needed
    7. Be under 2 sentences
    8. Only reply with the response in Rick's voice. Do not include any analysis, explanation, or reasoning. Just the response itself"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except:
        return "That's not even close to what I asked. Try focusing on the actual question, *burp*"

def fallback_agent(state: InterviewState) -> InterviewState:
    state["fallback_attempts"] += 1
    print(f"🔄 ENTERING fallback_agent")
    print(f"   Fallback attempts: {state['fallback_attempts']}")
    print(f"   Current question index: {state.get('current_question_index', 0)}")
    
    # If we've had too many fallback attempts, move to next question
    if state["fallback_attempts"] > 3:
        print(f"📋 Too many fallback attempts ({state['fallback_attempts']}), moving to next question")
        state["current_question_index"] += 1
        state["fallback_attempts"] = 0
        state["follow_up_count"] = 0
        state["current_thread"] = []
        state["_routing"] = "to_rick_agent"  # Route to RickAgent for question generation
        print(f"🔄 EXITING fallback_agent - routing: to_rick_agent")
        return state
    
    # Generate appropriate fallback response
    if state["fallback_attempts"] == 1:
        print(f"   → First fallback - generating guidance")
        # First fallback - try to guide them back
        fallback_response = generate_guidance_fallback(state)
    else:
        print(f"   → Subsequent fallback - generating personalized response")
        # Subsequent fallbacks - more direct
        fallback_response = generate_personalized_fallback(state)
    
    print(f"   → Generated fallback: {fallback_response[:50]}...")
    # Store in state instead of printing
    state["last_response"] = fallback_response
    # Add fallback to global history
    state["history"].append({"speaker": "rick", "content": fallback_response})
    state["current_thread"].append({"type": "fallback", "content": fallback_response})
    state["_routing"] = "terminal"  # Normal fallback is terminal
    print(f"🔄 EXITING fallback_agent - routing: terminal")
    return state

def rick_agent(state: InterviewState) -> InterviewState:
    print(f"🤖 ENTERING rick_agent")
    print(f"   Current question index: {state.get('current_question_index', 0)}")
    print(f"   Questions length: {len(state.get('questions', []))}")
    
    # Initialize state if needed
    if not state.get("questions"):
        # Use the initialize_interview function if candidate_name and tech_stack are available
        # Otherwise, initialize only the required fields for this function
        if state.get("candidate_name") and state.get("tech_stack"):
            # Don't overwrite existing state, just fill in missing values
            default_state = initialize_interview(state["candidate_name"], state["tech_stack"], state.get("experience", {"years": 0, "months": 0}), state.get("interested_roles", []))
            for key, value in default_state.items():
                if key not in state:
                    state[key] = value
        else:
            # Minimal initialization if we don't have candidate info yet
            state["questions"] = []
            state["current_thread"] = []
            state["fallback_attempts"] = 0
            state["follow_up_count"] = 0
    
    # Generate new question if needed
    if state["current_question_index"] >= len(state["questions"]):
        print(f"   🔥 Generating new question...")
        # Pass previous questions for context
        new_question = generate_rick_question(state["tech_stack"], state.get("experience", {"years": 0, "months": 0}), state.get("interested_roles", []), state.get("questions", []))
        state["questions"].append(new_question) # The list of questions increases by 1 meaning that the current question index is now equal to the length of the questions list
        state["current_base_question"] = new_question
        state["follow_up_count"] = 0
        state["current_thread"] = [{"type": "question", "content": new_question}]
        # Store in state instead of printing
        state["last_response"] = new_question
        # Add to global history too
        state["history"].append({"speaker": "rick", "content": new_question})
        print(f"   Generated question: {new_question[:50]}...")
    
    print(f"🤖 EXITING rick_agent - last_response: {state['last_response'][:50]}...")
    return state

def answer_evaluator(state: InterviewState) -> InterviewState:
    """Evaluate the candidate's answer and update state."""
    print(f"📊 ENTERING answer_evaluator")
    
    current_question = get_current_question(state)
    response = state["last_response"]
    
    print(f"   Question: {current_question[:50]}...")
    print(f"   Response: {response[:50]}...")
    
    # Add candidate's response to history
    state["history"].append({"speaker": "candidate", "content": response})
    # Also add to current thread for this specific question
    state["current_thread"].append({"type": "response", "content": response})
    # Get thread context for better evaluation
    thread_context = get_thread_context(state["current_thread"])
    evaluation = evaluate_answer(current_question, response, state["tech_stack"], state.get("experience", {"years": 0, "months": 0}), state.get("interested_roles", []), thread_context)
    state["last_evaluation"] = evaluation
    
    print(f"   Evaluation: {evaluation}")
    print(f"📊 EXITING answer_evaluator")
    
    return state

# Route based on evaluator result
def evaluation_decision(state: InterviewState) -> str:
    """Route based on the evaluation result."""
    print(f"🔀 EVALUATION ROUTING: {state.get('last_evaluation', 'unknown')}")
    return state.get("last_evaluation", "irrelevant")

# Route based on follow-up check result
def followup_router(state: InterviewState) -> str:
    """Route based on follow-up check result."""
    routing = state.get("_routing", "next_question")
    print(f"🔀 FOLLOWUP ROUTING: {routing}")
    return routing

# Route based on fallback agent result
def fallback_router(state: InterviewState) -> str:
    """Route based on fallback result."""
    routing = state.get("_routing", "terminal")
    print(f"🔀 FALLBACK ROUTING: {routing}")
    return routing

# Construct the LangGraph - SINGLE GRAPH DESIGN
graph = StateGraph(InterviewState)

# Define all necessary nodes
graph.add_node("GreetCandidate", greet_candidate)
graph.add_node("GreetingResponse", process_greeting_response)
graph.add_node("RickAgent", rick_agent)
graph.add_node("Evaluator", answer_evaluator)
graph.add_node("FollowUpCheck", check_and_generate_followup)
graph.add_node("FallbackAgent", fallback_agent)

# Smart entry point routing
def determine_entry_point(state: InterviewState) -> str:
    """Determine where to start based on current state."""
    print(f"🎯 DETERMINING ENTRY POINT")
    print(f"   greeting_done: {state.get('greeting_done', False)}")
    print(f"   ready_to_start: {state.get('ready_to_start', False)}")
    print(f"   last_response: '{state.get('last_response', '')[:30]}...'")
    print(f"   questions length: {len(state.get('questions', []))}")
    print(f"   current_question_index: {state.get('current_question_index', 0)}")
    print(f"   fallback_attempts: {state.get('fallback_attempts', 0)}")
    
    
    # If no greeting done yet, start with greeting
    if not state.get("greeting_done", False):
        print(f"   → Starting with GreetCandidate")
        return "GreetCandidate"
    
    # If we have a user response to process during greeting phase
    if state.get("last_response") and not state.get("ready_to_start", False):
        print(f"   → Processing greeting response")
        return "GreetingResponse"
    
    # If we have questions and user provided a response to evaluate
    if (state.get("ready_to_start", False) and 
        len(state.get("questions", [])) > 0 and 
        state.get("last_response")):
        print(f"   → Evaluating user response")
        return "Evaluator"
    
    # Default to greeting
    print(f"   → Default to GreetCandidate")
    return "GreetCandidate"

# Set conditional entry point - ONLY for user input routing
graph.add_conditional_edges(
    "__start__",
    determine_entry_point,
    path_map={
        "GreetCandidate": "GreetCandidate",
        "GreetingResponse": "GreetingResponse", 
        "Evaluator": "Evaluator"
        # ✅ REMOVED: RickAgent - now only reached through internal graph flows
        # ✅ REMOVED: FallbackAgent and NextQuestionAgent 
        # These are only reached through internal graph flows
    }
)

# Greeting flow
graph.add_conditional_edges(
    "GreetingResponse",
    greeting_response_router,
    path_map={
        "start_interview": "RickAgent",
        "wait": "GreetCandidate",
    },
)

# Evaluation flow - routes to fallback or follow-up check
graph.add_conditional_edges(
    "Evaluator",
    evaluation_decision,
    path_map={
        "relevant": "FollowUpCheck",
        "irrelevant": "FallbackAgent", 
        "gibberish": "FallbackAgent",
    }
)

# Fallback flow - can route to RickAgent or be terminal
graph.add_conditional_edges(
    "FallbackAgent",
    fallback_router,
    path_map={
        "to_rick_agent": "RickAgent",  # Route to RickAgent for next question
        "terminal": "__end__"          # Normal fallback is terminal
    }
)

# Follow-up flow - FollowUpCheck can be terminal when generating follow-ups
graph.add_conditional_edges(
    "FollowUpCheck",
    followup_router,
    path_map={
        "follow_up": "__end__",  # ✅ Follow-up questions are terminal (user-facing)
        "next_question": "RickAgent"  # ✅ Direct to RickAgent, no intermediate node
    }
)

# Compile the graph with MongoDB persistence
# Use the same MongoDB URI we're already using
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
from pymongo import MongoClient
client = MongoClient(MONGO_URI)
checkpointer = MongoDBSaver(client)
compiled_graph = graph.compile(checkpointer=checkpointer)

# Service class - SIMPLIFIED
class RickInterviewService:
    """Service for managing Rick interview sessions."""
    
    def __init__(self):
        self.active_interviews = {}
    
    def start_interview(self, candidate_id: str, candidate_name: str, tech_stack: List[str], experience: dict, interested_roles: List[str]) -> str:
        """Start a new interview session."""
        print(f"🚀 STARTING INTERVIEW for {candidate_name}")
        
        config = {"configurable": {"thread_id": candidate_id}}
        
        # Create new interview (frontend already handles returning users)
        initial_state = initialize_interview(candidate_name, tech_stack, experience, interested_roles)
        self.active_interviews[candidate_id] = {"config": config}
        
        # Invoke the single graph
        result = compiled_graph.invoke(initial_state, config=config)
        
        return result.get("last_response", "Hello! I'm Rick, ready to start your interview.")
    
    def process_message(self, candidate_id: str, message: str) -> str:
        """Process user message."""
        print(f"💬 PROCESSING MESSAGE: '{message}'")
        
        # CRITICAL: Backend restart resilience check
        # 
        # SCENARIO: User is mid-interview when backend server restarts
        # 1. Frontend still shows chat interface (interview_started = True from frontend init)
        # 2. Backend loses all RAM: self.active_interviews = {} (reset on restart)
        # 3. User sends message → candidate_id not in active_interviews → Would fail!
        # 4. This check restores backend tracking from MongoDB persistence
        #
        # NOTE: Frontend init only restores UI state, NOT backend state tracking!
        if candidate_id not in self.active_interviews:
            print(f"🔄 Candidate {candidate_id} not in active interviews, attempting to resume...")
            print(f"   ⚠️  Backend restart detected - rebuilding state from MongoDB...")
            
            config = {"configurable": {"thread_id": candidate_id}}
            
            # Check if state exists in MongoDB (LangGraph persistence)
            try:
                existing_state = compiled_graph.get_state(config=config)

                if existing_state.values:
                    # Resume existing interview - restore backend tracking
                    print(f"✅ Found existing state for {candidate_id}, resuming interview")
                    print(f"   🔧 Rebuilding active_interviews entry from MongoDB state")
                    self.active_interviews[candidate_id] = {"config": config}
                else:
                    # No existing state found - truly new user
                    print(f"❌ No existing state found for {candidate_id}")
                    raise ValueError(f"No active interview for candidate {candidate_id}. Please start a new interview.")
                
            except Exception as e:
                print(f"❌ Error checking existing state: {e}")
                raise ValueError(f"No active interview for candidate {candidate_id}. Please start a new interview.")
        
        config = self.active_interviews[candidate_id]["config"]
        # Get current state and update with user message
        current_state = compiled_graph.get_state(config=config)
        updated_input = current_state.values.copy()
        updated_input["last_response"] = message
        # Invoke the same single graph
        result = compiled_graph.invoke(updated_input, config=config)
        return result.get("last_response", "I'm having trouble processing that.")
    
    def end_interview(self, candidate_id: str) -> None:
        """End interview session."""
        if candidate_id in self.active_interviews:
            del self.active_interviews[candidate_id]

# Create a singleton service instance
interview_service = RickInterviewService()
