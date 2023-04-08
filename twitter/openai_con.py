import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# openai.File.create(
#   file=open("elonmusk_test_prepared.jsonl", "rb"),
#   purpose='fine-tune'
# )
train_file = "file-FMIBb1rhojB5CVK7AtsdbvK9"
test_file = "file-izio2y8HqgmacRqcMXAGxv5O"
# print(openai.File.list())

# res = openai.FineTune.create(training_file=train_file,model="davinci",
                      #  validation_file=test_file, suffix="twitter_test_elon")
model_id = "ft-ZIkoYMoiKLfkiiZ0DY2NZha1"
# res = openai.FineTune(id=model_id)
fine_tuned_model = "davinci:ft-personal:twitter-test-elon-2023-04-08-08-09-36"
new_prompt = "Write a tweet that Elon Musk would send out."

res = openai.Completion.create(
  model=prompt=fine_tuned_model,
  new_prompt
)

print(res)