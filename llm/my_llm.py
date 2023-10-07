import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

_logger = logging.getLogger(__name__)


def _generate_text(input_text, model, tokenizer):
    inputs = tokenizer(input_text, return_tensors="pt",
                       max_length=2048).input_ids.to("cuda")

    with torch.no_grad():
        outputs = model.generate(inputs, max_new_tokens=100,
                                 return_dict_in_generate=True, output_scores=True, temperature=1)

    return tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)


def _determine_answer(prediction):
    prediction = prediction.lower()
    return prediction


def load_model(model_name: str, path_to_cache: str):
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, cache_dir=path_to_cache)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name, cache_dir=path_to_cache, device_map="auto")
        _logger.info("Load model LLM successful")
        return model, tokenizer
    except Exception as e:
        _logger.exception("Unable to load model: %s", str(e))
        return None, None


def anwser_question(model, tokenizer, question, question_type, options):
    text_prompt = ""
    model_answer = _generate_text(text_prompt, model, tokenizer)
    model_answer = _determine_answer(model_answer)
    