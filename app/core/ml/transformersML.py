from summarizer import Summarizer, TransformerSummarizer


class Bert:
    def __init__(self, text):
        model = Summarizer()
        self.summary = ''.join(model(text, min_length=20, max_length=30))


class GPT2:
    def __init__(self, text):
        model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")
        self.summary = ''.join(model(text, min_length=20, max_length=30))


class XLM:
    def __init__(self, text):
        model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
        self.summary = ''.join(model(text, min_length=20, max_length=30))
