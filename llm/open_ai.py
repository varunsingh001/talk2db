from llm_base import LLM
import os
from prompts import PromptHandler
from ..retrieval_context.FAISS import FAISS
from ..utils.sql_utils import extract_sql
from langchain.chat_models import AzureChatOpenAI

class OpenAIClient(LLM):
    def __init__(self, config=None, prompt=None, context_store=None):
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
            if None is prompt:
                self.prompts = PromptHandler(self.config)
            else:
                self.prompts = prompt
            if None is context_store:
                self.embeddings_store = FAISS(config)
            else:
                self.embeddings_store = context_store
    
    
    def get_llm(self) -> str:
        if self.client is not None:
            return self.client
        else:
            print("OpenAI disabled in config")

