import jsonlines
import random

data = []

with jsonlines.open("elonmusk_prepared.jsonl") as f:
    for obj in f:
        data.append(obj)

random.shuffle(data)

reader = jsonlines.Reader(data)
print(reader)

for obj in reader:
  print(obj)

# with jsonlines.Writer("elonmusk_prepared_shuffled.jsonl") as writer:
#     writer.write_all(data)
