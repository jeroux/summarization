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
        if int(self.file_id) not in self.cached or chapters_summary_limit != 200:
            # self.by_chapter_summary = list()
            # for chapter in self.chapters:
            #     self.by_chapter_summary += [self.summarize(chapter, self.gen_tokenizer, self.gen_model)]
            # self.by_chapter_summary = tuple(self.by_chapter_summary)
            # bert = Bert( cuda=self.cuda)
            # gpt2 = GPT2( cuda=self.cuda)
            xlm = XLM( cuda=self.cuda)
            if chapters_summary_limit < self.n_chapters:
                text = self.chapters[:chapters_summary_limit]
            else:
                text = self.chapters
            # bert(text)
            # gpt2(text)
            xlm(text)
            # self.bert_summary = bert.summary
            # print(self.bert_summary)
            # self.gpt_summary = gpt2.summary
            # print(self.gpt_summary)
            self.xlm_summary = xlm.summary
            print(self.xlm_summary)

            self.save_cache()
        else:
            with open(self.cached[int(self.file_id)], "rt", encoding="utf-8") as cache_json:
                cache = json.load(cache_json)
            self.title = cache["title"]
            self.author = cache["author"]
            self.chapters = cache["chapters"]
            self.chapter_names = cache["chapter_names"]
            self.bert_summary = cache["bert_summary"]
            self.gpt_summary = cache["gpt_summary"]
            self.xlm_summary = cache["xlm_summary"]
            # self.bert_summary += str(text)

    def save_cache(self):
        self.cached[self.file_id] = os.path.join(self.data_path, str(self.file_id) + ".json")
        with open(self.cached[self.file_id], "w+", encoding="utf-8") as cache_json:
            cache = dict()
            cache["title"] = self.title
            cache["author"] = self.author
            cache["chapters"] = self.chapters
            cache["chapter_names"] = self.chapter_names
            cache["bert_summary"] = self.bert_summary
            cache["gpt_summary"] = self.gpt_summary
            cache["xlm_summary"] = self.xlm_summary
            json.dump(cache, cache_json,sort_keys=True, indent=4)
