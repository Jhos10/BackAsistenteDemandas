from huggingface_hub import InferenceClient


client = InferenceClient(
  "cardiffnlp/twitter-roberta-base-sentiment-latest",
  token="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",
)

client.text_classification("Today is a great day")