import json

# Extracting convos where the teacher adapts to the student
def convos_extractor():
    conversation = {}
    i = 0
    for _ in range(1,5):
        with open(f"Education-Dialogue-Dataset-main/conversations_train{_}.json", "r") as file:
            data = json.load(file)
            for j in range(len(data)):
                if data[j]["background_info"]["teacher_reactions"] == "and gets frustrated otherwise":
                    conversation[i] = data[j]["conversation"]
                    i += 1

    print(f"Ended up with {len(conversation)} conversations")
    return conversation

# Making input/output couples


def dataset_maker(n_lines = 3, convos = {}):

    context_size = 2*n_lines                 # number of past lines to take in the context (must be even for it to end at a student's line)
    dataset = []

    for convo in range(len(convos)):
            stop_point = len(convos[convo]) - 1                       # substracted -1 to end in a student's line

            for size in range(2, context_size + 1, 2):                                # even steps to end up at a student line
                for k in range(0, stop_point - size + 1, 2):
                    input = convos[convo][k:k + size]
                    for line in range(len(input)):
                        input[line] = input[line]["text"]
                    output = convos[convo][k + size]["text"]
                    dataset.append({"input": input, "output" : output})
    return dataset

convos = convos_extractor()
dataset = dataset_maker(6, convos)

for i in range(30):
    print(dataset[i])
