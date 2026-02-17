from models.schema import ConversationHistory, OrchestratorResponse
from openai import OpenAI
class OrchestratorAgent:
    def __init__(self, config):
        self.config = config
        self.openai_api_key = config.OPENAI_API_KEY
        self.openai_model = config.OPENAI_MODEL
        self.system_prompt = """
        You are a technical research assistant.
        You help with programming tasks, code generation, debugging, software engineering, API's and technical problem-solving.
        Always give structured and clear answers.
        Do not guess or make up information. If you don't know the answer, say you don't know.
        Ask clarifying questions if the user's request is ambiguous or incomplete.
        """
        self.conversation_history = ConversationHistory()

    def process_query(self, query):
        self.conversation_history.add_message(role="user", content=query)
        client = OpenAI(api_key=self.openai_api_key)
        response = client.chat.completions.create(
            model=self.openai_model,
            messages=[{"role": "system", "content": self.system_prompt}] + self.conversation_history.to_openai_format(),
            max_tokens=1500,
            temperature=0.3
        )
        self.conversation_history.add_message(role="assistant", content=response.choices[0].message.content)
        return OrchestratorResponse(responose=response.choices[0].message.content,
                                    model_used=self.openai_model,
                                    tokens_used=response.usage.total_tokens,
                                    error="")
    
    def clear_history(self):
        self.conversation_history = ConversationHistory()