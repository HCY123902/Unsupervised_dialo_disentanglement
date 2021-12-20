import json
import random

train_source = open("train.json", "r")
valid_source = open("valid.json", "r")
test_source = open("test.json", "r")

positive_message_sample_size = 1000000
positive_session_sample_size = 500000

negative_message_sample_size = 2000000
negative_session_sample_size = 1000000

def generate_sample(source):
    dialogues = json.load(source)
    positive_message_samples = []
    positive_session_samples = []

    for dialogue in dialogues:
        if len(positive_message_samples) > positive_message_sample_size and len(positive_session_samples) > positive_session_sample_size:
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
                    messages = [[t["speaker"], t["utterance"]] for t in dialogue[:turns[i]["position"]]]
                    sample = {"messages": messages, "current_message": [speaker, turns[i]["utterance"]], "label": 1}
                    positive_session_samples.append(sample)

    negative_message_samples = []
    negative_session_samples = []

    for i, dialogue in enumerate(dialogues[:-1]):
        if len(negative_message_samples) > negative_message_sample_size and len(negative_session_samples) > negative_session_sample_size:
            break
        
        left_position = int(random.random() * len(dialogue))
        dialogue_position = int(random.random() * (len(dialogues) - (i + 1))) + (i + 1)
        right_position = int(random.random() * len(dialogues[dialogue_position]))
        if len(negative_message_samples) <= negative_message_sample_size:
            negative_message_samples.append([dialogue[left_position]["utterance"], dialogue[right_position]["utterance"], 0])

        if len(negative_session_samples) <= negative_session_sample_size:
            messages = [[t["speaker"], t["utterance"]] for t in dialogue[:left_position + 1]]
            current_turn = dialogues[dialogue_position][right_position]
            sample = {"messages": messages, "current_message": [current_turn["speaker"], current_turn["utternace"]], "label": 0}
            negative_session_samples.append(sample)
    
    message_samples = []
    message_samples.extend(positive_message_samples)
    message_samples.extend(negative_message_samples)
    random.shuffle(message_samples)

    session_samples = []
    session_samples.extend(positive_session_samples)
    session_samples.extend(negative_session_samples)
    random.shuffle(session_samples)

    return message_samples, session_samples

train_message_samples, train_session_samples = generate_sample(train_source)
valid_message_samples, valid_session_samples = generate_sample(valid_source)
test_message_samples, test_session_samples = generate_sample(test_source)

train_message = open("train_message.json", "w")
train_session = open("train_session.json", "w")
valid_message = open("train_message.json", "w")
valid_session = open("train_session.json", "w")
test_message = open("train_message.json", "w")
test_session = open("train_session.json", "w")

json.dump(train_message_samples, train_message)
json.dump(train_session_samples, train_session)
json.dump(valid_message_samples, valid_message)
json.dump(valid_session_samples, valid_session)
json.dump(test_message_samples, test_message)
json.dump(test_session_samples, test_session)

