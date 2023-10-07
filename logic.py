from my_models import Question
import json
from paraformer.my_retrieval import information_retrieval


def handle(model_ir, model_llm, question: Question):
    with open("data/corpus.json", 'r') as file:
        data_corpus = json.load(file)
    id_copurs = information_retrieval(
        model_ir, question.question, question.question_type, question.options, data_corpus, 20)
