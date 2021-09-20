import json
import os

from transformers import BartForConditionalGeneration, BartTokenizer

from core.extract_html import BreakDownBook


class Bart(BreakDownBook):
    def __init__(self, html_filepath):
        super(Bart, self).__init__(html_filepath)
        self.file_id = html_filepath.replace("\\", "/").split("/")[-1].split(".")[0]
        self.data_path = os.path.dirname(html_filepath)

        self.cached = {int(x.replace("\\", "/").split("/")[-1].split(".")[0]): os.path.join(self.data_path, x)
                       for x in os.listdir(self.data_path) if x.endswith(".json")}
        if self.file_id not in self.cached:
            tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
            model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
            self.by_chapter_summary = list()
            for chapter in self.chapters:
                self.by_chapter_summary += [self.summarize(chapter, tokenizer, model)]
            self.by_chapter_summary = tuple(self.by_chapter_summary)

            self.summary = "\n".join(self.by_chapter_summary)
            self.short_summary = self.summarize("\n".join(self.by_chapter_summary), tokenizer, model)
            self.save_cache()
        else:
            with open(self.cached[self.file_id], "rt") as cache_json:
                cache = json.load(cache_json)
            self.title = cache["title"]
            self.author = cache["author"]
            self.chapters = cache["chapters"]
            self.chapter_names = cache["chapter_names"]

    def summarize(self, text, tokenizer, model):
        inputs = tokenizer.batch_encode_plus([text],
                                             return_tensors='pt',
                                             max_length=1024,
                                             truncation=True)
        summary_ids = model.generate(inputs['input_ids'], early_stopping=True)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def save_cache(self):
        self.cached[self.file_id] = os.path.join(self.data_path, str(self.file_id) + ".json")
        with open(self.cached[self.file_id], "w+") as cache_json:
            cache = dict()
            cache["title"] = self.title
            cache["author"] = self.author
            cache["chapters"] = self.chapters
            cache["chapter_names"] = self.chapter_names
            json.dump(cache, cache_json)


class GPT2():
    pass


class XLM():
    pass
