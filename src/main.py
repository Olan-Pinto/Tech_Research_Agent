from agents.orchestrator import OrchestratorAgent 
from utils import config
try:
    while(True):
        print("Hi there, we are building a research agent that can help you with your research needs. Please enter your query:")
        print("These are your options:")
        print("clear_chat - Clear the conversation history")
        print("chat_history - Show the conversation history so far")
        print("CTRL+C - Exit the program")
        print("Any other input will be treated as a query to the orchestrator agent")
        user_input = input("Your query: ")
        orchestrator_agent = OrchestratorAgent()
        if(user_input.lower() == "clear_chat"):
            print(*"*" * 20)
            orchestrator_agent.clear_history()
            print("Conversation history cleared.")
            print(*"*" * 20)
        elif(user_input.lower() == "chat_history"):
            print(*"*" * 50)
            print("Conversation History:")
            for msg in orchestrator_agent.conversation_history.messages:
                print(f"{msg.role.capitalize()}: {msg.content}")
            print(*"*" * 50)
        else:
            print("*" * 50)
            print("Assistant:")
            print(orchestrator_agent.process_query(user_input).response)
            print()
            print("Model: ", orchestrator_agent.openai_model, "| Tokens used: ", orchestrator_agent.process_query(user_input).tokens_used)
except KeyboardInterrupt:
    print("\nExiting the program. Goodbye!")