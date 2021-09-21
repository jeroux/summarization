from transformers import AutoTokenizer, AutoModelForQuestionAnswering, AutoModelForPreTraining

AutoTokenizer.from_pretrained('valhalla/bart-large-finetuned-squadv1')
AutoModelForQuestionAnswering.from_pretrained("valhalla/bart-large-finetuned-squadv1")

AutoTokenizer.from_pretrained('gpt2-medium')
AutoModelForPreTraining.from_pretrained('gpt2-medium')

AutoTokenizer.from_pretrained("bert-large-uncased")
AutoModelForPreTraining.from_pretrained("bert-large-uncased")

AutoTokenizer.from_pretrained('xlnet-base-cased')
AutoModelForPreTraining.from_pretrained('xlnet-base-cased')
