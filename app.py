from retrieval_context import FAISS
from retrieval_context.EmbeddingModels import LocalEmbeddingModel, HuggingFaceEmbeddingModel
from llm.open_ai import OpenAIClient
from llm.prompts import PromptHandler
from utils.sql_utils import is_sql_valid
from langchain.chains import LLMChain



config = {}
embedding_model = None
context_store = None
llm = None


if "LOCAL" in config.get('embedding_model_type', 'LOCAL'):
    embedding_model = LocalEmbeddingModel(config).load_model()
else:
    embedding_model = HuggingFaceEmbeddingModel(config).load_model() 

if "faiss" in config.get('embedding_store', 'faiss'):
    context_store = FAISS(config)

if "openai" in config.get('llm', 'openai'):
    llm = OpenAIClient(config)

prompt = PromptHandler(config=config, embeddings_store=context_store)
chain = LLMChain(llm=llm)
# Generate SQL using the chain
sql_query = chain.run(prompt=prompt.get_prompt(question=""))
print("Is valid SQL : " + is_sql_valid(sql_query))  
print(sql_query)