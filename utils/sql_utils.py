import re

def extract_sql(self, llm_response: str) -> str:
    sqls = re.findall(r"\bWITH\b .*?;", llm_response, re.DOTALL)
    if sqls:
        sql = sqls[-1]
        self.log(title="Extracted SQL", message=f"{sql}")
        return sql
    sqls = re.findall(r"SELECT.*?;", llm_response, re.DOTALL)
    if sqls:
        sql = sqls[-1]
        self.log(title="Extracted SQL", message=f"{sql}")
        return sql
    sqls = re.findall(r"```sql\n(.*)```", llm_response, re.DOTALL)
    if sqls:
        sql = sqls[-1]
        self.log(title="Extracted SQL", message=f"{sql}")
        return sql

    sqls = re.findall(r"```(.*)```", llm_response, re.DOTALL)
    if sqls:
        sql = sqls[-1]
        self.log(title="Extracted SQL", message=f"{sql}")
        return sql
    return llm_response

    def is_sql_valid(self, sql: str) -> bool:
        parsed = sqlparse.parse(sql)

        for statement in parsed:
            if statement.get_type() == 'SELECT':
                return True
        return False

    def should_generate_chart(self, df: pd.DataFrame) -> bool:
        if len(df) > 1 and df.select_dtypes(include=['number']).shape[1] > 0:
            return True
        return False
    