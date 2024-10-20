from ..retrieval_context.ContextStore import ContextStore

class PromptHandler():
    def __init__(self, config = None, 
                 embeddings_store: ContextStore = None
                ):
        if config is None:
            self.config = {}
        self.config = config
        self.static_documentation = ""
        self.dialect = self.config.get("dialect", "SQL")
        self.max_tokens = self.config.get("max_tokens", 14000)
        self.embeddings_store = embeddings_store

    def system_message(self, message: str) -> any:
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> any:
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> any:
        return {"role": "assistant", "content": message}

    def add_ddl_to_prompt(
            self, initial_prompt: str, ddl_list: list[str], max_tokens: int = 14000
        ) -> str:
            if len(ddl_list) > 0:
                initial_prompt += "\n===Tables \n"

                for ddl in ddl_list:
                    if (
                        self.str_to_approx_token_count(initial_prompt)
                        + self.str_to_approx_token_count(ddl)
                        < max_tokens
                    ):
                        initial_prompt += f"{ddl}\n\n"

            return initial_prompt

    def add_documentation_to_prompt(
        self,
        initial_prompt: str,
        documentation_list: list[str],
        max_tokens: int = 14000 
    ) -> str:
        if len(documentation_list) > 0:
            initial_prompt += "\n===Additional Context \n\n"

            for documentation in documentation_list:
                if (self.str_to_approx_token_count(initial_prompt) + self.str_to_approx_token_count(documentation) < max_tokens):
                    initial_prompt += f"{documentation}\n\n"
        return initial_prompt

    def add_sql_to_prompt(
        self, initial_prompt: str, sql_list: list[str], max_tokens: int = 14000
    ) -> str:
        if len(sql_list) > 0:
            initial_prompt += "\n===Question-SQL Pairs\n\n"

            for question in sql_list:
                if (
                    self.str_to_approx_token_count(initial_prompt)
                    + self.str_to_approx_token_count(question["sql"])
                    < max_tokens
                ):
                    initial_prompt += f"{question['question']}\n{question['sql']}\n\n"

        return initial_prompt

    def get_sql_prompt(
        self,
        initial_prompt : str,
        question: str,
        question_sql_list: list,
        ddl_list: list,
        doc_list: list,
        **kwargs,
    ):

        if initial_prompt is None:
            initial_prompt = f"You are a {self.dialect} expert. " + \
            "Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. "

        initial_prompt = self.add_ddl_to_prompt(
            initial_prompt, ddl_list, max_tokens=self.max_tokens
        )

        if self.static_documentation != "":
            doc_list.append(self.static_documentation)

        initial_prompt = self.add_documentation_to_prompt(
            initial_prompt, doc_list, max_tokens=self.max_tokens
        )

        initial_prompt += (
            "===Response Guidelines \n"
            "1. If the provided context is sufficient, please generate a valid SQL query without any explanations for the question. \n"
            "2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql \n"
            "3. If the provided context is insufficient, please explain why it can't be generated. \n"
            "4. Please use the most relevant table(s). \n"
            "5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. \n"
            f"6. Ensure that the output SQL is {self.dialect}-compliant and executable, and free of syntax errors. \n"
        )

        message_log = [self.system_message(initial_prompt)]

        for example in question_sql_list:
            if example is None:
                print("example is None")
            else:
                if example is not None and "question" in example and "sql" in example:
                    message_log.append(self.user_message(example["question"]))
                    message_log.append(self.assistant_message(example["sql"]))

        message_log.append(self.user_message(question))

        return message_log
        
    def str_to_approx_token_count(self, string: str) -> int:
        return len(string) / 4
    

    def get_prompt(self, question: str, **kwargs) -> str:
        if self.config is not None:
            initial_prompt = self.config.get("initial_prompt", None)
        else:
            initial_prompt = None
        question_sql_list = self.embeddings_store.get_similar_question_sql(question, **kwargs)
        ddl_list = self.embeddings_store.get_related_ddl(question, **kwargs)
        doc_list = self.embeddings_store.get_related_documentation(question, **kwargs)
        prompt = self.get_sql_prompt(
            initial_prompt=initial_prompt,
            question=question,
            question_sql_list=question_sql_list,
            ddl_list=ddl_list,
            doc_list=doc_list,
            **kwargs,
        )
        self.log(title="SQL Prompt", message=prompt)
        return prompt