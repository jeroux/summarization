from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig


class Bart:
    def __init__(self, text):
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        inputs = tokenizer.batch_encode_plus([text], return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(inputs['input_ids'], min_length=50, num_beams=7, early_stopping=False)
        self.summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)


class GPT2():
    pass

class XLM():
    pass