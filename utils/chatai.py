from langchain.schema import HumanMessage
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()


class LangChainModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LangChainModel, cls).__new__(cls)
            # Initialize the instance
            cls._instance._init_model()
        return cls._instance

    def _init_model(self):
        try:
            model = "gemma2-9b-it"
            provider = "groq"

            self._chat_model = init_chat_model(
                model,
                model_provider=provider,
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.7,
            )

        except Exception as e:
            raise Exception(f"Error creating LangChain model\n{e}")

    def get_response(self, user_prompt: str) -> str:
        try:
            message = [HumanMessage(content=user_prompt)]
            response = self._chat_model.invoke(message)
            return response.content

        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")
