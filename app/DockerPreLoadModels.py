from transformers import BartForConditionalGeneration, BartTokenizer, BartForQuestionAnswering

BartTokenizer.from_pretrained('facebook/bart-large-cnn')
BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
BartForQuestionAnswering.from_pretrained('facebook/bart-large-cnn')