from transformers import BartForConditionalGeneration, AutoTokenizer, BartTokenizer, AutoModelForQuestionAnswering

BartTokenizer.from_pretrained('facebook/bart-large-cnn')
BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
AutoTokenizer.from_pretrained('valhalla/bart-large-finetuned-squadv1')
AutoModelForQuestionAnswering.from_pretrained("valhalla/bart-large-finetuned-squadv1")
