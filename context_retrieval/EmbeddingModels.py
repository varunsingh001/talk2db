from abc import ABC, abstractmethod
from transformers import AutoModel, AutoTokenizer
import torch

class EmbeddingModel(ABC):

    def __init__(self, config):
        self.config = config
        self.model = None
        self.tokenizer = None

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def get_embeddings(self, text):
        pass


class LocalEmbeddingModel(EmbeddingModel):

    def load_model(self):
        local_path = self.config.get('model_path')
        if local_path:
            self.tokenizer = AutoTokenizer.from_pretrained(local_path)
            self.model = AutoModel.from_pretrained(local_path)
            print(f"Model loaded from local path: {local_path}")
        else:
            raise ValueError("Model path not specified in config.")

    def get_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()


class HuggingFaceEmbeddingModel(EmbeddingModel):
    def load_model(self):

        model_name = self.config.get('model_name')
        if model_name:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            print(f"Model loaded from Hugging Face: {model_name}")
        else:
            raise ValueError("Model name not specified in config.")

    def get_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()