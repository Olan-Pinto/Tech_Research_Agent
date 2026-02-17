from models.schema import ConversationHistory, OrchestratorResponse
from openai import OpenAI
from utils.config import settings
from utils.cost_calculator import calculate_cost
from utils.logger import get_logger
from agents.prompts import ORCHESTRATOR_SYSTEM_PROMPT 

logger = get_logger(__name__)

class OrchestratorAgent:
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.openai_model = settings.OPENAI_MODEL
        self.system_prompt = ORCHESTRATOR_SYSTEM_PROMPT
        self.conversation_history = ConversationHistory()

    def process_query(self, query):
        self.conversation_history.add_message(role="user", content=query)
        client = OpenAI(api_key=self.openai_api_key)
        logger.info("Processing user query through OpenAI API", query_length=len(query), conversation_turns=len(self.conversation_history.messages))
        try:
            response = client.chat.completions.create(
                model=self.openai_model,
                messages=[{"role": "system", "content": self.system_prompt}] + self.conversation_history.to_openai_format(),
                max_tokens=1500,
                temperature=0.3
            )
            self.conversation_history.add_message(role="assistant", content=response.choices[0].message.content)
            cost = calculate_cost(self.openai_model, response.usage.prompt_tokens, response.usage.completion_tokens)
            logger.info("Query processed", model=self.openai_model, input_tokens=response.usage.prompt_tokens,
                        output_tokens=response.usage.completion_tokens, 
                        total_tokens=response.usage.total_tokens, cost_usd=f"${cost:.6f}")
            return OrchestratorResponse(response=response.choices[0].message.content,
                                        model_used=self.openai_model,
                                        tokens_used=response.usage.total_tokens,
                                        error="",cost_usd=cost)
        except Exception as e:
            logger.error("Error processing query", error=str(e.code), model=self.openai_model)
            return OrchestratorResponse(response="", model_used=self.openai_model, tokens_used=0, error=str(e.code), cost_usd=0.0)
    
    def clear_history(self):
        self.conversation_history = ConversationHistory()