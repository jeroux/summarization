import json
import os

from transformers import BartForConditionalGeneration, BartTokenizer

from core.extract_html import BreakDownBook


class Bert:
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    def summarize(self, text):
        inputs = self.tokenizer.batch_encode_plus([text],
                                             return_tensors='pt',
                                             max_length=1024,
                                             truncation=True)
        summary_ids = self.model.generate(inputs['input_ids'], early_stopping=True)
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)


class GPT2():
    pass


class XLM():
    pass
