import os

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

from core.ml.summarizerML import SummarizerML


class QABookSummerizerML(SummarizerML):
    def __init__(self, html_filepath, chapters_summary_limit=-1, cuda=False):
        super(QABookSummerizerML, self).__init__(html_filepath=html_filepath,
                                                 chapters_summary_limit=chapters_summary_limit)
        self.tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
        self.model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
        self.output = "No Data has been processed"
        self.questions = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data",
                                     "faq.csv"))
        self.cuda = torch.cuda.is_available() and cuda
        if self.cuda:
            self.model = self.model.cuda()

    def __call__(self, question):
        return self.qa(question)

    def qa(self, question):
        answer_text = self.bert_summary + " " + self.gpt_summary + " " + self.xlm_summary
        inputs = self.tokenizer.encode_plus(question.lower(), answer_text, add_special_tokens=True, return_tensors="pt",
                                            max_length=512)
        input_ids = inputs["input_ids"].tolist()[0]

        outputs = self.model(**inputs)
        answer_start_scores = outputs.start_logits.cpu()
        answer_end_scores = outputs.end_logits.cpu()

        answer_start = torch.argmax(
            answer_start_scores
        )  # Get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(
            answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score

        answer = self.tokenizer.convert_tokens_to_string(
            # self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
            self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        # Combine the tokens in the answer and print it out.""
        answer = answer.replace("#", "")

        return answer

    def faq(self):
        q_a = pd.DataFrame([], columns=("Question", "Answer"), dtype=str)
        q_a.iloc[:, :] = [["What is the book title?", self.title.upper()],
                          ["Who is the author of the book?", self.prettify_text(self.author)],
                          ["How long is the book?", f"The book is composed of {self.n_chapters} chapters"]]
        for i, question in self.questions.iterrows():
            question = question[0]
        q_a.append({"Question": self.clean_text(question), "Answer": self.prettify_text(self.qa(question))})
        return q_a

    @staticmethod
    def prettify_text(text, full_cap=True):
        if full_cap:
            return " ".join([x.capitalize() for x in text.split(" ") if x])
        else:
            return " ".join([x for x in text.split(" ") if x]).capitalize()


if __name__ == "__main__":
    ROOTPATH = (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    DATAPATH = os.path.join(ROOTPATH, "data")
    qab = QABookSummerizerML(os.path.join(DATAPATH, "103.html"), 200, cuda=True)

    print("Question: Who is the main character?", "\nAnswer: " + qab("Who is the main character?"))
    print("Question: What is the main challenge?", "\nAnswer: " + qab("What is the main challenge?"))
    print(qab("What is the main challenge?"))
    print("Question: Who follows Phileas Fogg?", "\nAnswer: " + qab("Who follows Phileas Fogg??"))
    print("Question: What is the hero's task?", "\nAnswer: " + qab("What is the hero's task?"))
