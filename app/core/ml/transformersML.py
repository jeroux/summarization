import torch
from transformers import AutoTokenizer, \
    AutoModelForSeq2SeqLM


class Model:
    def __init__(self, cuda=True):
        self.tokenizer = self.model = None
        self.summary = ""
        self.cuda = torch.cuda.is_available() and cuda

    def __call__(self, text):
        MIN_LENGTH = max(len(text) // 100, 1)
        MAX_LENGTH = max(len(text) // 90, 1200)
        inputs = self.tokenizer("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

        ids = inputs["input_ids"]
        if self.cuda:
            raise NotImplementedError
            self.model = self.model.cuda()
            ids = ids.cuda()
        outputs = self.model.generate(ids, max_length=MAX_LENGTH, min_length=MIN_LENGTH, length_penalty=2.0,
                                      num_beams=4, early_stopping=True)
        self.summary = self.tokenizer.decode(outputs[0])
        return self.summary


class Bert(Model):
    def __init__(self, cuda=False):
        super(Bert, self).__init__(cuda)
        self.tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-xsum")
        self.summary = ""


class GPT2(Model):
    def __init__(self, cuda=True):
        super(GPT2, self).__init__(cuda)
        self.tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")


class XLM(Model):
    def __init__(self, cuda=True):
        super(XLM, self).__init__(cuda)
        self.tokenizer = AutoTokenizer.from_pretrained("google/roberta2roberta_L-24_bbc")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/roberta2roberta_L-24_bbc")


if __name__ == "__main__":
    model = GPT2()
    print(model('the circumstances under which this telegraphic dispatch about phileas fogg was sent were as follows: '
                'the steamer “mongolia,” belonging to the peninsular and oriental company, built of iron, of two '
                'thousand eight hundred tons burden, and five hundred ' +
                "is the consulate?” “there, on the corner of the square,” said fix, pointing to a house two hundred "
                "steps off. “i’ll go and fetch my master, who won’t be much pleased, however, to be disturbed.” "
                "the passenger bowed to fix, and returned to the steamer."))
    model = XLM()
    print(model('the circumstances under which this telegraphic dispatch about phileas fogg was sent were as follows: '
                'the steamer “mongolia,” belonging to the peninsular and oriental company, built of iron, of two '
                'thousand eight hundred tons burden, and five hundred ' +
                "is the consulate?” “there, on the corner of the square,” said fix, pointing to a house two hundred "
                "steps off. “i’ll go and fetch my master, who won’t be much pleased, however, to be disturbed.” "
                "the passenger bowed to fix, and returned to the steamer."))
    model = Bert()
    print(model('the circumstances under which this telegraphic dispatch about phileas fogg was sent were as follows: '
                'the steamer “mongolia,” belonging to the peninsular and oriental company, built of iron, of two '
                'thousand eight hundred tons burden, and five hundred ' +
                "is the consulate?” “there, on the corner of the square,” said fix, pointing to a house two hundred "
                "steps off. “i’ll go and fetch my master, who won’t be much pleased, however, to be disturbed.” "
                "the passenger bowed to fix, and returned to the steamer."))
