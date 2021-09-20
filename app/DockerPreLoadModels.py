from transformers import AutoTokenizer, AutoModelForQuestionAnswering

AutoTokenizer.from_pretrained('valhalla/bart-large-finetuned-squadv1')
AutoModelForQuestionAnswering.from_pretrained("valhalla/bart-large-finetuned-squadv1")
