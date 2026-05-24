# Closira AI Agent: Patient Coordinator Prototype

## Overview
This is a Python-based AI workflow built to simulate a customer communication platform for an SMB (Bloom Aesthetics Clinic). It handles inbound enquiries, qualifies leads, and intelligently escalates complex issues to human agents using strict SOP boundaries.

## Architecture
The script operates in a continuous loop with four distinct stages:
1. **FAQ Answering:** Governed by a strict "Closed-Book" prompt design.
2. **Lead Qualification:** Collects treatment history and consultation intent.
3. **Escalation Detection:** Monitors for medical questions, frustration, price negotiation, or out-of-scope services, triggering an automatic handoff.
4. **Conversation Summary:** Generates a structured JSON-style summary of intent and recommended actions upon termination.

## Setup Instructions
1. Clone this repository to your local machine.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
3. Activate the virtual environment.
4. Install the required dependencies:
   ```bash
   pip install openai python-dotenv 
5. Create a .env file in the root directory and add your API key:
   SARVAM_API_KEY=your_key_here

## How to Run
Execute the main script from your terminal:

  ```bash
  python agent.py
  ```
Type your queries directly into the terminal. To end the simulation and generate the final summary, type quit.

## Trade-offs & Known Limitations

1. API Routing Workaround: To optimize testing resources and bypass OpenAI's strict tier-based rate limits for new developer accounts, this prototype utilizes the official openai Python SDK but securely routes completion requests to a fully OpenAI-compatible endpoint (Sarvam AI's 105b model). The system architecture, prompt engineering, and logic remain 100% compatible with OpenAI. Swapping back to gpt-4o-mini only requires updating the base_url and model strings in agent.py.

2. No UI: As per the assignment requirements, this is a terminal-based CLI script, not a web application.



