import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

from core.ml.summarizerML import SummarizerML


class QABookSummerizerML(SummarizerML):
    def __init__(self, html_filepath):
        super(QABookSummerizerML, self).__init__(html_filepath=html_filepath)
        self.tokenizer = AutoTokenizer.from_pretrained("valhalla/bart-large-finetuned-squadv1")
        self.model = AutoModelForQuestionAnswering.from_pretrained("valhalla/bart-large-finetuned-squadv1")
        self.output = "No Data has been processed"
        self.questions = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"),
                                     "faq.csv")

    def __call__(self, question):
        return self.qa(question)

    def qa(self, question):
        answer_text = self.summary
        inputs = self.tokenizer.encode_plus(question.lower(), answer_text, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]

        outputs = self.model(**inputs)
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits

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
                          ["Who is the author of the book?", " ".join([x.capitalize() for x in self.author.split(" ")])]]
        return self.questions


if __name__ == "__main__":
    import os

    ROOTPATH = (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    DATAPATH = os.path.join(ROOTPATH, "data")
    qab = QABookSummerizerML(os.path.join(DATAPATH, "103.html"))

    print("Question: Who is the main character?", "\nAnswer: " + qab("Who is the main character?"))
    print("Question: What is the main challenge?", "\nAnswer: " + qab("What is the main challenge?"))
    print(qab("What is the main challenge?"))
    print("Question: Who follows Phileas Fogg?", "\nAnswer: " + qab("Who follows Phileas Fogg??"))
    print("Question: What is the hero's task?", "\nAnswer: " + qab("What is the hero's task?"))
