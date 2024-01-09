from transformers import BertModel, BertTokenizer
import torch

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Input text
text = "Example sentence to embed."

# Tokenize and convert to tensor
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

# Extract embeddings (CLS token embeddings for the entire sequence)
embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

print(embeddings)
