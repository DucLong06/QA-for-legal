import torch
import logging
import numpy as np
from collections import Counter, defaultdict
from rank_bm25 import BM25Okapi
from paraformer.my_paraformer import Model_Paraformer
from paraformer.processing_data import word_segment

_logger = logging.getLogger(__name__)


def load_model(path_to_model: str):
    try:
        model = Model_Paraformer(
            "khanhpd2/sbert_phobert_large_cosine_sim").to('cuda')
        checkpoint = torch.load(path_to_model, map_location='cuda')
        model.load_state_dict(checkpoint)
        _logger.info("Load model PARAFORMER successful")
        return model
    except Exception as e:
        _logger.exception("Unable to load model: %s", str(e))
        return None


def _get_top_n_articles(query: str, data_corpus, top_n: int):
    corpus = list(data_corpus.values())
    tokenized_corpus = [word_segment(doc) for doc in corpus]
    tokenized_corpus = [doc.split(" ") for doc in tokenized_corpus]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = word_segment(query)
    tokenized_query = tokenized_query.split(" ")
    bm25_scores = bm25.get_scores(tokenized_query)

    top_n_articles = sorted(list(zip(data_corpus.keys(), data_corpus.values(), bm25_scores)),
                            key=lambda x: x[2], reverse=True)[:top_n]
    return top_n_articles


def information_retrieval(model: Model_Paraformer, question, question_type, options, data_corpus, top_n):
    model.eval()
    list_question = []
    total_choice = []
    if question_type != "options":
        list_question.append(question)
    else:
        pass
    for query in list_question:
        final_scores = []
        top_n_articles = _get_top_n_articles(
            query, data_corpus, top_n=top_n)
        list_keys, list_articles, bm25_scores = zip(*top_n_articles)

        for i, article in enumerate(list_articles):
            article = [sentence.strip() for sentence in article.split(
                "\n") if sentence.strip() != ""]
            deep_score = model.get_score(query, article)
            final_scores.append(0.7*deep_score+(1-0.7)*bm25_scores[i])
        total_choice.append(
            (np.max(final_scores), list_keys[np.argmax(final_scores)]))

    id_corpus = [id for _, id in total_choice]
    counter = Counter(id_corpus)
    most_common = counter.most_common()
    if len(most_common) in [2, 4]:
        _, id_corpus = max(total_choice, key=lambda x: x[0])
    else:
        id_corpus = most_common[0][0]
    return id_corpus
