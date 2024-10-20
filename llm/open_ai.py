from llm_base import LLM
import os
from prompts import PromptHandler
from langchain.chat_models import AzureChatOpenAI

class OpenAIClient(LLM):
    def __init__(self, config=None):
        LLM.__init__(self, config=config)

        if config is not None and self.config.get("llm") is "openai":
            if "openai_deployment_name" in config or os.environ.get('OPENAI_DEPLOYMENT_NAME'):
                raise Exception(
                "OPENAI_DEPLOYMENT_NAME not set!"
            )

            if "openai_model_name" in config or os.environ.get('OPENAI_MODEL_NAME'):
                raise Exception(
                "OPENAI_MODEL_NAME not set!"
            )
        
            if "openai_api_url" in config or os.environ.get('OPENAI_API_URL'):
                raise Exception(
                "OPENAI_API_URL not set!"
            )

            if "openai_api_key" in config or os.environ.get('OPENAI_API_KEY'):
                raise Exception(
                "OPENAI_API_KEY not set!"
            )

            self.client = AzureChatOpenAI(
                        deployment_name=self.config.get("openai_deployment_name", os.environ.get('OPENAI_DEPLOYMENT_NAME')), 
                        model_name=self.config.get("openai_model_name", os.environ.get('OPENAI_MODEL_NAME')), 
                        temperature=self.config.get("temperature", 0))
    
    
    def get_llm(self) -> str:
        if self.client is not None:
            return self.client
        else:
            print("OpenAI disabled in config")

