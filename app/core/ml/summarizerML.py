import json
import os

from gensim.summarization.summarizer import summarize

from core.ml.transformersML import Bert, GPT2, XLM
from ..extract_html import BreakDownBook

DECOUPE_CHAPITRE = 2


class SummarizerML(BreakDownBook):
    def __init__(self, html_filepath):
        super(SummarizerML, self).__init__(html_filepath)
        self.bert_summary = ''
        self.gpt_summary = ''
        self.xlm_summary = ''
        self.file_id = html_filepath.replace("\\", "/").split("/")[-1].split(".")[0]
        self.data_path = os.path.dirname(html_filepath)

        self.cached = {int(x.replace("\\", "/").split("/")[-1].split(".")[0]): os.path.join(self.data_path, x)
                       for x in os.listdir(self.data_path) if x.endswith(".json")}

        if self.file_id not in self.cached:
            # self.by_chapter_summary = list()
            # for chapter in self.chapters:
            #     self.by_chapter_summary += [self.summarize(chapter, self.gen_tokenizer, self.gen_model)]
            # self.by_chapter_summary = tuple(self.by_chapter_summary)

            self.bert()
            self.gpt_summary = GPT2(self.text).summary
            self.xlm_summary = XLM(self.text).summary

            self.save_cache()
        else:
            with open(self.cached[self.file_id], "rt") as cache_json:
                cache = json.load(cache_json)
            self.title = cache["title"]
            self.author = cache["author"]
            self.chapters = cache["chapters"]
            self.chapter_names = cache["chapter_names"]
            self.bart_summary = cache["bart_summary"]
            self.bart_short_summary = cache["bart_short_summary"]
            self.bert_summary = cache["bert_summary"]
            self.gpt_summary = cache["gpt_summary"]
            self.xlm_summary = cache["xlm_summary"]

    def bert(self):

        print("nbrs chapitres:", self.n_chapters)
        for index in range(0, len(self.chapters), DECOUPE_CHAPITRE):
            print(index)

            if index + DECOUPE_CHAPITRE + 1 < len(self.chapters):
                chapter = self.chapters[index:index + DECOUPE_CHAPITRE]
            else:
                chapter = self.chapters[index:]
            chapter = '\nChapitre\n'.join(chapter)

            self.bert_summary += Bert(chapter).summary

    def save_cache(self):
        self.cached[self.file_id] = os.path.join(self.data_path, str(self.file_id) + ".json")
        with open(self.cached[self.file_id], "w+") as cache_json:
            cache = dict()
            cache["title"] = self.title
            cache["author"] = self.author
            cache["chapters"] = self.chapters
            cache["chapter_names"] = self.chapter_names
            cache["bert_summary"] = self.bert_summary
            cache["gpt_summary"] = self.gpt_summary
            cache["xlm_summary"] = self.xlm_summary
            json.dump(cache, cache_json)
