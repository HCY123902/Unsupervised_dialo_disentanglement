import json
import random

train_source_json = open("entangled_train.json", "r")
valid_source_json = open("entangled_dev.json", "r")
test_source_json = open("entangled_test.json", "r")

percentage = 1

positive_message_sample_size = 1000000 * percentage
positive_session_sample_size = 500000 * percentage

negative_message_sample_size = 2000000 * percentage
# negative_session_sample_size = 1000000 * percentage
negative_session_sample_size = 60000

t = json.load(train_source_json)
train_source = t[:int(percentage * len(t))]

v = json.load(valid_source_json)
valid_source = v[:int(percentage * len(v))]

e = json.load(test_source_json)
test_source = e[:int(percentage * len(v))]

sampled_train_json = open("entangled_train_{}_percent.json".format(int(percentage * 100)), "w")
sampled_valid_json = open("entangled_valid_{}_percent.json".format(int(percentage * 100)), "w")
sampled_test_json = open("entangled_test_{}_percent.json".format(int(percentage * 100)), "w")

json.dump(train_source, sampled_train_json)
json.dump(valid_source, sampled_valid_json)
json.dump(test_source, sampled_test_json)

def generate_sample(source):
    dialogues = source
    positive_message_samples = []
    positive_session_samples = []

    for dialogue in dialogues:
        if len(positive_message_samples) >= positive_message_sample_size and len(positive_session_samples) >= positive_session_sample_size:
            break
    
        speakers = {}
        for position, turn in enumerate(dialogue):
            (speakers.setdefault(turn["speaker"], [])).append({"position": position, "utterance": turn["utterance"], "label": turn["label"]})
        for speaker, turns in speakers.items():
            for i in range(0, len(turns) - 1):
                for j in range(i + 1, len(turns)):
                    # The sessions need to be the same
                    if len(positive_message_samples) <= positive_message_sample_size and turns[i]["label"] == turns[j]["label"]:
                        positive_message_samples.append([turns[i]["utterance"], turns[j]["utterance"], 1])

                if len(positive_session_samples) <= positive_session_sample_size and  i >= 1:
                    if len(turns[i]["utterance"].strip()) < 1:
                        print("Detected message {} with length {}".format(turns[i]["utterance"], len(turns[i]["utterance"])))
                        continue
                    
                    messages = [[t["speaker"], t["utterance"], t["label"]] for t in dialogue[:turns[i]["position"]] if len(t["utterance"].strip()) >= 1]
                    if len(messages) <= 0:
                        print("Detected context with length {}".format(len(messages)))
                        continue
                    
                        
                    sample = {"messages": messages, "current_message": [speaker, turns[i]["utterance"], turns[i]["label"]], "label": 1}
                    positive_session_samples.append(sample)

    negative_message_samples = []
    negative_session_samples = []

    for i, dialogue in enumerate(dialogues[:-1]):
        if len(negative_message_samples) >= negative_message_sample_size and len(negative_session_samples) >= negative_session_sample_size:
            break
        
        # left_position = int(random.random() * len(dialogue))
        for j, turn in enumerate(dialogue):
            for k in range(5):
                dialogue_position = int(random.random() * (len(dialogues) - (i + 1))) + (i + 1)
                right_position = int(random.random() * len(dialogues[dialogue_position]))
                if len(negative_message_samples) <= negative_message_sample_size:
                    negative_message_samples.append([turn["utterance"], dialogues[dialogue_position][right_position]["utterance"], 0])

                if len(negative_session_samples) <= negative_session_sample_size:
                    current_turn = dialogues[dialogue_position][right_position]
                    if len(current_turn["utterance"].strip()) < 1:
                        print("Detected message {} with length {}".format(current_turn["utterance"], len(current_turn["utterance"])))
                        continue
                    
                    messages = [[t["speaker"], t["utterance"], t["label"]] for t in dialogue[:j + 1] if len(t["utterance"].strip()) >= 1]
                    if len(messages) <= 0:
                        print("Detected context with length {}".format(len(messages)))
                        continue
                    
                    sample = {"messages": messages, "current_message": [current_turn["speaker"], current_turn["utterance"], current_turn["label"]], "label": 0}
                    negative_session_samples.append(sample)
    
    message_samples = []
    message_samples.extend(positive_message_samples)
    message_samples.extend(negative_message_samples)
    random.shuffle(message_samples)

    session_samples = []
    session_samples.extend(positive_session_samples)
    session_samples.extend(negative_session_samples)
    random.shuffle(session_samples)

    print("{} positive and {} negative message samples captured".format(len(positive_message_samples), len(negative_message_samples)))
    print("{} positive and {} negative session samples captured".format(len(positive_session_samples), len(negative_session_samples)))

    return message_samples, session_samples

train_message_samples, train_session_samples = generate_sample(train_source)
valid_message_samples, valid_session_samples = generate_sample(valid_source)
test_message_samples, test_session_samples = generate_sample(test_source)

train_message = open("train_message_{}_percent.json".format(int(percentage * 100)), "w")
train_session = open("train_session_{}_percent.json".format(int(percentage * 100)), "w")
valid_message = open("valid_message_{}_percent.json".format(int(percentage * 100)), "w")
valid_session = open("valid_session_{}_percent.json".format(int(percentage * 100)), "w")
test_message = open("test_message_{}_percent.json".format(int(percentage * 100)), "w")
test_session = open("test_session_{}_percent.json".format(int(percentage * 100)), "w")

json.dump(train_message_samples, train_message)
json.dump(train_session_samples, train_session)
json.dump(valid_message_samples, valid_message)
json.dump(valid_session_samples, valid_session)
json.dump(test_message_samples, test_message)
json.dump(test_session_samples, test_session)
