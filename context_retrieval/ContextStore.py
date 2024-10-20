from abc import ABC, abstractmethod
class ContextStore(ABC):
    def __init__(self, config={}):
        self.config = config

    # ----------------- Use Any Database to Store and Retrieve Context ----------------- #
    @abstractmethod
    def get_similar_question_sql(self, question: str, **kwargs) -> list:
        pass

    @abstractmethod
    def get_similar_question_sql(self, question: str, **kwargs) -> list:
        pass

    @abstractmethod
    def get_related_ddl(self, question: str, **kwargs) -> list:
        pass

    @abstractmethod
    def get_related_documentation(self, question: str, **kwargs) -> list:
        pass

    @abstractmethod
    def add_question_sql(self, question: str, sql: str, **kwargs) -> str:
        pass

    @abstractmethod
    def add_ddl(self, ddl: str, **kwargs) -> str:
        pass

    @abstractmethod
    def add_documentation(self, documentation: str, **kwargs) -> str:
        pass