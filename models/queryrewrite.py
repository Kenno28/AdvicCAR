from pydantic import BaseModel

class QueryRewrite(BaseModel):
    query: str