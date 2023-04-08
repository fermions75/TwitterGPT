import sys
import json
import random
# format python script_name.py handle number_of_tweets_to_feth file_path_to_save
# total arguments
from twitter import get_formated_tweets
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])

handle = sys.argv[1]
cnt = sys.argv[2] 
train_path = sys.argv[3]
test_path = sys.argv[4]

print("\nArguments passed:", end = " ")
print("Handle:", handle, "Count:", cnt)
print("Train Path:", train_path)
print("Test Path:", test_path)

data = []
data = get_formated_tweets(handle, int(cnt))

def get_json(line):
  curr = {}
  curr["prompt"] = "Write a tweet that user with handle " + handle + " would write on twitter"
  curr["completion"] = line
  res = json.dumps(curr)
  return res

random.shuffle(data)
train_lim = int(.8 * len(data))

train_set = data[:train_lim]
test_set = data[train_lim:]

with open(train_path, "a") as f:  
  for line in data:
    f.write(str(get_json(line)) + "\n")
    
with open(test_path, "a") as f:  
  for line in data:
    f.write(str(get_json(line)) + "\n")
# f = open("demofile2.txt", "a")
# f.write("Now the file has more content!")
# f.close()