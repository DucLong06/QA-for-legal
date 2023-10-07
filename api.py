from fastapi import FastAPI, Request
from logic import handle
from my_models import Question
# import llm.my_llm as my_llm
import my_env
from paraformer import my_retrieval


app = FastAPI()

# model_llm, tokenizer = my_llm.load_model(my_env.MODEL_NAME, my_env.PATH_TO_CACHE)
model_ir = my_retrieval.load_model("")
model_llm = ""


@app.get("/")
def ping() -> dict:
    return {"msg": "Server is OK"}


@app.post("/")
async def answer(request: Question) -> dict:
    try:
        response_data = handle(model_ir, model_llm, request)
        return response_data
    except Exception as e:
        return {"Bug": {str(e)}}
