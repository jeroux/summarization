from gensim.summarization.summarizer import summarize

from core.ml.transformersML import Bert, GPT2, XLM
from ..extract_html import BreakDownBook

DECOUPE_CHAPITRE = 2


class SummarizerML(BreakDownBook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bert_summary = ''
        self.gpt_summary = ''
        self.xlm_summary = ''
        self.bert()
        self.gpt_summary = GPT2(self.text).summary
        self.xlm_summary = XLM(self.text).summary

    def bert(self):

        print("nbrs chapitres:", len(self.chapters))
        for index in range(0, len(self.chapters), DECOUPE_CHAPITRE):
            print(index)

            if index + DECOUPE_CHAPITRE + 1 < len(self.chapters):
                chapter = self.chapters[index:index + DECOUPE_CHAPITRE]
            else:
                chapter = self.chapters[index:]
            chapter = '\nChapitre\n'.join(chapter)

            self.bert_summary += Bert(chapter).summary
