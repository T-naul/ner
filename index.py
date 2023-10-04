from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

import os 

def setup_cache_directory(cache_dir):
    """
    Creates the cache directory if it does not exist.

    Args:
        cache_dir (str): The path to the cache directory.
    """
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir
def setup_model(model_id, cache_dir):
    """
    Sets up the tokenizer and model.

    Args:
        model_id (str): The model identifier.
        cache_dir (str): The path to the cache directory.

    Returns:
        tokenizer: The tokenizer object.
        model: The model object.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=cache_dir)
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model = AutoModelForTokenClassification.from_pretrained(model_id, cache_dir=cache_dir)
    return tokenizer, model

def setup_ner(model_id="xlm-roberta-large-finetuned-conll03-english", cache_dir=None):
    """
    Sets up the ner model.

    Args:
        model_id (str): The model identifier.
        cache_dir (str): The path to the cache directory.

    Returns:
        model: The pipeline model object.
    """
    cache_dir = setup_cache_directory(cache_dir)
    tokenizer, model = setup_model(model_id, cache_dir)
    classifier = pipeline("ner", model=model, tokenizer=tokenizer)

    return classifier
