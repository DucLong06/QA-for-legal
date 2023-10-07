from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    question_type: str
    question: str
    options: List[str] = [""]
