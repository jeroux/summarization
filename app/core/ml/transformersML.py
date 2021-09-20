from summarizer import Summarizer, TransformerSummarizer


class Bert:

    def __init__(self, text):
        MIN_LENGTH = len(text) // 1000
        MAX_LENGTH = len(text) // 900
        model = Summarizer()
        self.summary = ''.join(model(text, min_length=MIN_LENGTH, max_length=MAX_LENGTH))


class GPT2:

    def __init__(self, text):
        MIN_LENGTH = len(text) // 1000
        MAX_LENGTH = len(text) // 900
        model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")
        self.summary = ''.join(model(text, min_length=MIN_LENGTH, max_length=MAX_LENGTH))


class XLM:

    def __init__(self, text):
        MIN_LENGTH = len(text) // 1000
        MAX_LENGTH = len(text) // 900
        model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
        self.summary = ''.join(model(text, min_length=MIN_LENGTH, max_length=MAX_LENGTH))
