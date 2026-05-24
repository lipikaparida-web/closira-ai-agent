import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key
load_dotenv()
# The technical loophole: Use the OpenAI library, but point it to Sarvam's URL!
client = OpenAI(
    api_key=os.getenv("SARVAM_API_KEY"),
    base_url="https://api.sarvam.ai/v1"
)

# 1. The Brain: Paste the core rules from your prompt_design.md here
SYSTEM_PROMPT = """
You are the premium patient coordinator for Bloom Aesthetics Clinic. 
Your goal is to warmly assist patients, answer basic enquiries, and smoothly qualify them for our treatments.

YOUR KNOWLEDGE BASE:
- Hours: Monday to Saturday, 9:00 AM to 7:00 PM. Closed Sundays.
- Services & Starting Prices: Botox (from £200), Dermal Fillers (from £250), Initial Consultations (Free).
- Booking & Policies: WhatsApp or website. Strict 24-hour notice for cancellations.

OPERATING RULES:
1. The "Closed-Book" Rule: ONLY provide facts listed above. For unlisted services, politely explain you need a specialist to confirm and escalate.
2. Lead Qualification: If interested, ask: "Is this your first time visiting us for this treatment?" and "Would you like me to help arrange a free consultation?"
3. Mandatory Escalation: If the patient asks for medical advice, complains, negotiates pricing, or asks out-of-scope questions, state that a human team member will take over shortly.
"""

def generate_summary(chat_history):
    """Stage 4: Generates a summary when the chat ends."""
    summary_prompt = "Review the following chat log. Provide a brief, structured summary including: Customer Intent, Key Details Collected, and Recommended Next Action."
    
    # We create a new temporary message array just for the summary
    messages = [{"role": "system", "content": summary_prompt}]
    messages.extend(chat_history[1:]) # Skip the original system prompt
    
    response = client.chat.completions.create(
                model="sarvam-105b", 
                messages=messages,
                temperature=0.2 
    )
    return response.choices[0].message.content

def main():
    print("Welcome to Bloom Aesthetics Clinic (AI Prototype).")
    print("Type 'quit' to end the simulation.\n" + "-"*50)
    
    # Initialize conversational memory
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        # Get customer input
        user_input = input("\nCustomer: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        # Append user message to memory
        messages.append({"role": "user", "content": user_input})
        
        # Call the OpenAI API (Stages 1 & 2: FAQ and Lead Qual)
        try:
            response = client.chat.completions.create(
                model="sarvam-105b",
                messages=messages,
                temperature=0.2 # Low temperature keeps it factual
            )
            
            ai_message = response.choices[0].message.content
            print(f"\nClosira AI: {ai_message}")
            
            # Append AI message to memory
            messages.append({"role": "assistant", "content": ai_message})
            
            # Stage 3: Escalation Detection
            # If the AI uses its hand-off phrases, we break the loop
            escalation_keywords = ["human team member", "specialist", "take over shortly"]
            if any(keyword in ai_message.lower() for keyword in escalation_keywords):
                print("\n[SYSTEM LOG: Escalation Trigger Detected. Handoff initiated.]")
                break
                
        except Exception as e:
            print(f"\n[Error communicating with OpenAI: {e}]")
            break

    # Stage 4: Conversation Summary
    print("\n" + "="*50)
    print("SESSION ENDED. GENERATING SUMMARY...\n")
    print(generate_summary(messages))

if __name__ == "__main__":
    main()