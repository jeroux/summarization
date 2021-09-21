import os

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class Model:
    def __init__(self, cuda=False):
        self.tokenizer = self.model = None
        self.summary = ""
        self.cuda = torch.cuda.is_available() and cuda
        self.max_length = 2048

    def __call__(self, text):
        self.summary = ""
        if self.cuda:
            self.model = self.model.cuda()
        for chapter in text:
            words = chapter.split(" ")
            MIN_LENGTH = max(len(chapter) // 100, 1)
            MAX_LENGTH = max(len(chapter) // 90, 2)
            while words:
                batch_size = min(self.max_length, len(words))
                batch, words = " ".join(words[:batch_size]), words[batch_size:]
                inputs = self.tokenizer(batch, return_tensors="pt", max_length=self.max_length,
                                        truncation=True)

                if self.cuda:
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                ids = inputs["input_ids"]
                outputs = self.model.generate(ids, length_penalty=2.0, num_beams=4, early_stopping=True)
            self.summary += " " + self.tokenizer.decode(outputs[0])
        return self.summary.replace("  ", " ")


class Bert(Model):
    def __init__(self, cuda=False):
        super(Bert, self).__init__(cuda)
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn", fast=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        self.max_length = 1024


class GPT2(Model):
    def __init__(self, cuda=False):
        super(GPT2, self).__init__(cuda)
        self.tokenizer = AutoTokenizer.from_pretrained("google/roberta2roberta_L-24_bbc", fast=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/roberta2roberta_L-24_bbc")
        self.max_length = 512


class XLM(Model):
    def __init__(self, cuda=False):
        super(XLM, self).__init__(cuda)
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-xsum", fast=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-xsum")
        self.max_length = 1024


if __name__ == "__main__":
    ROOTPATH = (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    DATAPATH = os.path.join(ROOTPATH, "data")
    with open(os.path.join(DATAPATH, "103.html"), "rt", encoding="utf-8") as tf:
        text = " ".join([x for x in tf.read().replace("\n", " ").replace("\t", " ").split(" ") if x])
    model1 = Bert()
    print(model1([text]))
    model2 = GPT2()
    print(model2([text]))
    model3 = XLM()
    print(model3([text]))

