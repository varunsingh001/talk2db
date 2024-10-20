from abc import ABC, abstractmethod

class LLM():
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config

    @abstractmethod
    def get_llm(self) -> str:
       pass

