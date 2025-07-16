from utils import getPrompt , getModel

if __name__ == "__main__":
    llm = getModel()

    user_query = input("💬 User: ")
    ticket_id = input("🔢 Ticket ID to check: ")

    try:
        ticket_id = int(ticket_id)
        prompt = getPrompt(user_query, ticket_id)
        response = llm(prompt, max_tokens=1000)
        print("🤖 Bot:", response["choices"][0]["text"].strip())
    except Exception as e:
        print(f"❌ LLM failed to generate response: {e}")
