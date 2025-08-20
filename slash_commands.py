import sys
import os
import io
import contextlib
import asyncio
import subprocess
import json
import random
from typing import Optional

from duckduckgo_mcp_server.server import DuckDuckGoSearcher
from mcp.server.fastmcp import Context

# Mock Context class for our simple client
class MockContext(Context):
    async def info(self, message: str):
        pass

    async def error(self, message: str):
        print(f"ERROR: {message}")

    async def warn(self, message: str):
        print(f"WARN: {message}")

    async def debug(self, message: str):
        pass

class StringIOWithNoName(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = None

async def perform_duckduckgo_search(query: str):
    searcher = DuckDuckGoSearcher()
    mock_ctx = MockContext()
    results = await searcher.search(query, mock_ctx)
    if results:
        return searcher.format_results_for_llm(results)
    else:
        return "No results found or an error occurred."

async def run_duckduckgo(query: str = "Python programming"):
    print(f"Running DuckDuckGo search for: {query}")
    results = await perform_duckduckgo_search(query)
    print("\n--- DuckDuckGo Search Results ---")
    print(results)

def generate_gns3_config(topic):
    if topic.upper() != "OSPF":
        return "GNS3 configuration generation is only supported for OSPF at the moment."

    try:
        with open("gns3_topology.json", "r") as f:
            topology = json.load(f)
    except FileNotFoundError:
        return "gns3_topology.json file not found."
    except json.JSONDecodeError:
        return "Invalid JSON in gns3_topology.json."

    if not os.path.exists("gns3_configs"):
        os.makedirs("gns3_configs")

    for router in topology["routers"]:
        config = f"hostname {router['name']}\n\n"
        for interface in router["interfaces"]:
            config += f"interface {interface['name']}\n"
            config += f" ip address {interface['ip_address']} {interface['subnet_mask']}\n"
            config += f" no shutdown\n\n"
        
        config += "router ospf 1\n"
        config += f" router-id {router['name'].replace('R','')}.{router['name'].replace('R','')}.{router['name'].replace('R','')}.{router['name'].replace('R','')}\n"
        config += " network 10.0.0.0 0.0.0.255 area 0\n"

        with open(f"gns3_configs/{router['name']}_config.txt", "w") as f:
            f.write(config)

    return "GNS3 configuration files have been generated in the 'gns3_configs' directory."

TOPIC_TO_DOMAIN = {
    "OSPF": "infrastructure",
    "BGP": "infrastructure",
    "EIGRP": "infrastructure",
    "STP": "infrastructure",
    "VLANs": "infrastructure",
    "WLAN": "architecture",
    "SD-WAN": "architecture",
    "SD-Access": "architecture",
    "VRF": "virtualization",
    "GRE": "virtualization",
    "NetFlow": "network_assurance",
    "SPAN/RSPAN/ERSPAN": "network_assurance",
    "IPSLA": "network_assurance",
    "SNMP": "network_assurance",
    "Syslog": "network_assurance",
    "Device Access Control": "security",
    "Infrastructure Security": "security",
    "REST API Security": "security",
    "Wireless Security": "security",
    "Python": "automation",
    "JSON": "automation",
    "REST APIs": "automation",
}

def get_question_bank_path(topic):
    domain = TOPIC_TO_DOMAIN.get(topic.upper())
    if not domain:
        return None
    return os.path.join("question_bank", domain, f"{topic.lower()}.json")

QUIZ_STATE_FILE = "quiz_state.json"

def start_quiz(topic: str, num_questions: int = 10):
    question_bank_path = get_question_bank_path(topic)
    if not question_bank_path or not os.path.exists(question_bank_path):
        return f"Topic '{topic}' not found in the question bank. Please add questions to the question bank first. See INSTRUCTIONS.md for more details."

    all_questions = []
    if os.path.exists(question_bank_path):
        try:
            with open(question_bank_path, "r") as f:
                all_questions = json.load(f)
        except json.JSONDecodeError:
            return f"Invalid JSON in {question_bank_path}."

    if len(all_questions) < num_questions:
        return f"Not enough questions for topic '{topic}'. Only {len(all_questions)} available. Please add more questions to the question bank."
    
    questions = random.sample(all_questions, num_questions)

    quiz_state = {
        "topic": topic,
        "questions": questions,
        "score": 0,
        "current_question_index": 0
    }

    with open(QUIZ_STATE_FILE, "w") as f:
        json.dump(quiz_state, f)

    return ask_question()

def ask_question():
    if not os.path.exists(QUIZ_STATE_FILE):
        return "No active quiz. Please start a quiz first with /quizme topic=<topic_name>"

    with open(QUIZ_STATE_FILE, "r") as f:
        quiz_state = json.load(f)

    current_question_index = quiz_state["current_question_index"]
    question = quiz_state["questions"][current_question_index]

    question_text = f"Question {current_question_index + 1}: {question['question']}\n"
    for option, text in question['options'].items():
        question_text += f"  {option}: {text}\n"

    return question_text

def answer_question(user_answer: str):
    if not os.path.exists(QUIZ_STATE_FILE):
        return "No active quiz. Please start a quiz first with /quizme topic=<topic_name>"

    with open(QUIZ_STATE_FILE, "r") as f:
        quiz_state = json.load(f)

    current_question_index = quiz_state["current_question_index"]
    question = quiz_state["questions"][current_question_index]
    correct_answer = question["answer"]

    if user_answer.upper() == correct_answer:
        quiz_state["score"] += 1
        feedback = "Correct!"
    else:
        feedback = f"Wrong! The correct answer is {correct_answer}."

    # Check if this is the last question *before* incrementing
    if current_question_index + 1 >= len(quiz_state["questions"]):
        quiz_state["current_question_index"] += 1 # Increment for final state
        with open(QUIZ_STATE_FILE, "w") as f:
            json.dump(quiz_state, f)
        return f"{feedback}\n\n{get_quiz_results()}"
    else:
        quiz_state["current_question_index"] += 1
        with open(QUIZ_STATE_FILE, "w") as f:
            json.dump(quiz_state, f)
        return f"{feedback}\n\n{ask_question()}"

def get_quiz_results():
    if not os.path.exists(QUIZ_STATE_FILE):
        return "No active quiz. Please start a quiz first with /quizme topic=<topic_name>"

    with open(QUIZ_STATE_FILE, "r") as f:
        quiz_state = json.load(f)

    score = quiz_state["score"]
    num_questions = len(quiz_state["questions"])
    final_score = (score / num_questions) * 100
    result = f"You scored {final_score:.2f}%. You answered {score} out of {num_questions} questions correctly."

    if (num_questions - score) >= 5:
        result += "\n" + generate_gns3_config(quiz_state["topic"])

    return result

async def quiz_me(topic: Optional[str] = None, answer: Optional[str] = None):
    if not os.path.exists(QUIZ_STATE_FILE) and not topic:
        return "Welcome to the CCNP Trainer Quiz!\n\nPlease choose a topic to get started.\n\nAvailable topics:\n" + "\n".join([f"- {t}" for t in TOPIC_TO_DOMAIN.keys()]) + "\n\nTo start a quiz, use the command: /quizme topic=\"<topic_name>\""
    
    if topic and not os.path.exists(QUIZ_STATE_FILE):
        return start_quiz(topic)
    
    if os.path.exists(QUIZ_STATE_FILE) and answer:
        return answer_question(answer)
    
    if os.path.exists(QUIZ_STATE_FILE) and not answer:
        return ask_question()
    
    return "Invalid state. Please start a quiz with /quizme topic=\"<topic_name>\" or provide an answer to the current question."