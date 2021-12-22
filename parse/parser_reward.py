import json
import random

train_source_json = open("entangled_train.json", "r")
valid_source_json = open("entangled_dev.json", "r")
test_source_json = open("entangled_test.json", "r")

# 1 for IRC and 0.1 for Movie
percentage = 0.1

t = json.load(train_source_json)
train_source = t[:int(percentage * len(t))]

v = json.load(valid_source_json)
valid_source = v[:int(percentage * len(v))]

e = json.load(test_source_json)
test_source = e[:int(percentage * len(v))]

# positive_message_sample_size = 1000000 * percentage
# positive_session_sample_size = 500000 * percentage

# negative_message_sample_size = 2000000 * percentage
# negative_session_sample_size = 1000000 * percentage

# t = json.load(train_source_json)
# train_source = t[:int(percentage * len(t))]

# v = json.load(valid_source_json)
# valid_source = v[:int(percentage * len(v))]

# e = json.load(test_source_json)
# test_source = e[:int(percentage * len(v))]

# sampled_train_json = open("entangled_train_{}_percent.json".format(int(percentage * 100)), "w")
# sampled_valid_json = open("entangled_valid_{}_percent.json".format(int(percentage * 100)), "w")
# sampled_test_json = open("entangled_test_{}_percent.json".format(int(percentage * 100)), "w")

# json.dump(train_source, sampled_train_json)
# json.dump(valid_source, sampled_valid_json)
# json.dump(test_source, sampled_test_json)

def generate_sample(source):
    dialogues = source
    samples = []
    # positive_session_samples = []

    for number, dialogue in enumerate(dialogues):
        # if len(positive_message_samples) >= positive_message_sample_size and len(positive_session_samples) >= positive_session_sample_size:
        #     break
    
        # speakers = {}
        # for position, turn in enumerate(dialogue):
        #     (speakers.setdefault(turn["speaker"], [])).append({"position": position, "utterance": turn["utterance"], "label": turn["label"]})
        # for speaker, turns in speakers.items():
        #     for i in range(0, len(turns) - 1):
        #         for j in range(i + 1, len(turns)):
        #             # The sessions need to be the same
        #             if len(positive_message_samples) <= positive_message_sample_size and turns[i]["label"] == turns[j]["label"]:
        #                 positive_message_samples.append([turns[i]["utterance"], turns[j]["utterance"], 1])
        for i in range(1, len(dialogue)):

            # Exclude the pair with 2 identical turns
            for j in range(i):
                sample = {"text1": dialogue[i]["utterance"], "text2": dialogue[j]["utterance"], "pos1": i, "pos2": j, "label1": dialogue[i]["label"], "label2": dialogue[j]["label"], "data_id": number}
                samples.append(sample)

    random.shuffle(samples)
    # message_samples = []
    # message_samples.extend(positive_message_samples)
    # message_samples.extend(negative_message_samples)
    # random.shuffle(message_samples)

    print("{} samples captured".format(len(samples)))
    # print("{} positive and {} negative message samples captured".format(len(positive_message_samples), len(negative_message_samples)))
    # print("{} positive and {} negative session samples captured".format(len(positive_session_samples), len(negative_session_samples)))

    return samples

train_samples = generate_sample(train_source)
valid_samples = generate_sample(valid_source)
test_samples = generate_sample(test_source)

# train_message_samples, train_session_samples = generate_sample(train_source)
# valid_message_samples, valid_session_samples = generate_sample(valid_source)
# test_message_samples, test_session_samples = generate_sample(test_source)

train_message = open("train_reward_{}_percent.json".format(int(percentage * 100)), "w")
# train_session = open("train_session_{}_percent.json".format(int(percentage * 100)), "w")
valid_message = open("valid_reward_{}_percent.json".format(int(percentage * 100)), "w")
# valid_session = open("valid_session_{}_percent.json".format(int(percentage * 100)), "w")
test_message = open("test_reward_{}_percent.json".format(int(percentage * 100)), "w")
# test_session = open("test_session_{}_percent.json".format(int(percentage * 100)), "w")

json.dump(train_message_samples, train_message)
# json.dump(train_session_samples, train_session)
json.dump(valid_message_samples, valid_message)
# json.dump(valid_session_samples, valid_session)
json.dump(test_message_samples, test_message)
# json.dump(test_session_samples, test_session)
