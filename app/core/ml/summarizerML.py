import json
import os

from core.ml.transformersML import Bert, GPT2, XLM
from core.extract_html import BreakDownBook

DECOUPE_CHAPITRE = 3


class SummarizerML(BreakDownBook):
    def __init__(self, html_filepath, chapters_summary_limit=-1, cuda=False):
        super(SummarizerML, self).__init__(html_filepath)
        self.bert_summary = ''
        self.gpt_summary = ''
        self.xlm_summary = ''
        self.chapters_summary_limit = chapters_summary_limit
        self.file_id = html_filepath.replace("\\", "/").split("/")[-1].split(".")[0]
        self.data_path = os.path.dirname(html_filepath)

        self.cached = {int(x.replace("\\", "/").split("/")[-1].split(".")[0]): os.path.join(self.data_path, x)
                       for x in os.listdir(self.data_path) if x.endswith(".json")}

        self.cuda=cuda
        if self.file_id not in self.cached or chapters_summary_limit != 200:
            # self.by_chapter_summary = list()
            # for chapter in self.chapters:
            #     self.by_chapter_summary += [self.summarize(chapter, self.gen_tokenizer, self.gen_model)]
            # self.by_chapter_summary = tuple(self.by_chapter_summary)
            bert = Bert()
            gpt2 = GPT2()
            xlm = XLM()
            bert.cuda = gpt2.cuda = xlm.cuda = self.cuda
            text = self.get_text_until_n_chapter(chapters_summary_limit)
            print("text: ", text)
            bert(text)
            gpt2(text)
            xlm(text)
            self.bert_summary = bert.summary
            print(self.bert_summary)
            self.gpt_summary = gpt2.summary
            print(self.gpt_summary)
            self.xlm_summary = xlm.summary
            print(self.xlm_summary)

            self.save_cache()
        else:
            with open(self.cached[self.file_id], "rt") as cache_json:
                cache = json.load(cache_json)
            self.title = cache["title"]
            self.author = cache["author"]
            self.chapters = cache["chapters"]
            self.chapter_names = cache["chapter_names"]
            self.bert_summary = cache["bert_summary"]
            self.gpt_summary = cache["gpt_summary"]
            self.xlm_summary = cache["xlm_summary"]

    def bert(self):
        bert = Bert()
        chapters_summary_limit = self.n_chapters if self.chapters_summary_limit < 1 else self.chapters_summary_limit
        for index in range(0, min(self.n_chapters, chapters_summary_limit), DECOUPE_CHAPITRE):

            if index + DECOUPE_CHAPITRE + 1 < len(self.chapters):
                chapter = self.chapters[index:index + DECOUPE_CHAPITRE]
            else:
                chapter = self.chapters[index:]
            chapter = '\n'.join(chapter)
            text = bert(chapter)
            print(text, type(text))
            # self.bert_summary += str(text)

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
