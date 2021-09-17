from transformers import BartTokenizer, BartForQuestionAnswering, BartForSequenceClassification
import torch

# tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')
# model = BartForQuestionAnswering.from_pretrained('facebook/bart-large')
#
# question, text = "Who was Jim Henson?", "Jim Henson was a nice puppet"
# inputs = tokenizer(question, text, return_tensors='pt')
# start_positions = torch.tensor([1])
# end_positions = torch.tensor([3])
#
# outputs = model(**inputs, start_positions=start_positions, end_positions=end_positions)
# loss = outputs.loss
# start_scores = outputs.start_logits
# end_scores = outputs.end_logits

if __name__ == "__main__":
    pass