from fastapi import FastAPI
from model import Question

app = FastAPI()


@app.get("/")
def ping() -> dict:
    return {"msg": "Server is OK"}


@app.post("/")
async def answer(question: Question) -> dict:
    try:
        return {"msg": question}
    except Exception as e:
        return {"Bug": {str(e)}}
