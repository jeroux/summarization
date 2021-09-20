from transformers import BartForConditionalGeneration, BartTokenizer

from core.extract_html import BreakDownBook


class Bart(BreakDownBook):
    def __init__(self, html_filepath):
        super(Bart, self).__init__(html_filepath)
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        self.by_chapter_summary = list()
        for chapter in self.chapters:
            self.by_chapter_summary += [self.summarize(chapter, tokenizer, model)]
        self.by_chapter_summary = tuple(self.by_chapter_summary)



        self.summary = self.summarize("\n".join(self.by_chapter_summary), tokenizer, model)



    def summarize(self, text, tokenizer, model):
        inputs = tokenizer.batch_encode_plus([text],
                                             return_tensors='pt',
                                             max_length=1024,
                                             truncation=True)
        summary_ids = model.generate(inputs['input_ids'], early_stopping=True)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


class GPT2():
    pass


class XLM():
    pass
