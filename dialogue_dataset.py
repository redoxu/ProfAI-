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
dataset = dataset_maker(8, convos)


# Your original data (replace this with loading from your file if needed)

converted_data = []

for entry in dataset:
    user_content = "\n".join(entry["input"])
    # Wrap user content inside <think> tags
    user_content_wrapped = f"/no_think{user_content}"
    
    assistant_content = entry["output"]
    # Wrap assistant content with empty <think> and <answer> tags
    assistant_content_wrapped = f"<think>\n\n</think>\n<answer>\n{assistant_content}\n</answer>"
    
    converted_data.append({
        "messages": [
            {"role": "user", "content": user_content_wrapped},
            {"role": "assistant", "content": assistant_content_wrapped}
        ]
    })

with open("dialogues_dataset.json", "w", encoding="utf-8") as f:
    json.dump(converted_data, f, ensure_ascii=False, indent=2)
