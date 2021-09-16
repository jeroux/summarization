from gensim.summarization.summarizer import summarize
from core.ml.transformersML import Bart

from ..extract_html import BreakDownBook

class Summarizer(BreakDownBook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bart_summary = ''

        summaries = list()
        size_summary = 1024//5
        for index in range(0, len(self.chapters), 5):
            chapters_summaries = ''
            if index+6 < len(self.chapters):
                chapters = self.chapters[index:index+5]
            else:
                chapters = self.chapters[index:]
            for chapter in chapters:
                chapters_summaries += self.summarize(text=chapter, length=size_summary)
            summaries.append(chapters_summaries)
        for chapter in summaries:
            self.bart_summary += Bart('\n'.join(chapter)).summary

    def summarize(self, text=None, length=1024):
        text = text if text else self.text
        return summarize(text, word_count=length)

