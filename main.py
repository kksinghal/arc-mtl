import json
import search
import os
import sandbox
from helper import compare_grid
from tqdm import tqdm

SPLIT = "training" # or "evaluation"

correct = 0
total = 0
correct_task_names = []
incorrect_task_names = []

files = os.listdir(f"ARC-AGI/data/{SPLIT}/")
files = [f.split(".")[0] for f in files]

for task_name in tqdm(files):
    if task_name in os.listdir("./logs"): continue

    with open(f"ARC-AGI/data/training/{task_name}.json", "r") as f:
        task = json.load(f)
    
    train_inputs = []
    train_outputs = []
    test_inputs = []
    test_outputs = []
    for ex in task["train"]:
            train_inputs.append(tuple(map(tuple, ex["input"])))
            train_outputs.append(tuple(map(tuple, ex["output"])))

    for ex in task["test"]:
        test_inputs.append(tuple(map(tuple, ex["input"])))
        test_outputs.append(tuple(map(tuple, ex["output"])))

    fs = search.brute_force(train_inputs, train_outputs)
    solved = True
    if fs:
        for i in range(len(test_inputs)):
            output = test_inputs[i]
            for f in fs:
                syntactical_correctness, output = sandbox.run(f, test_inputs[i])
                if not syntactical_correctness: 
                    solved = False
                    break
            if not compare_grid(output, test_outputs[i]):
                solved = False
    else: solved = False
    
    if solved:
        correct+=1
        correct_task_names.append(task_name)
    else:
        incorrect_task_names.append(task_name)

    total += 1
    print(correct/total, correct, total)
    if solved:
        with open(f"./logs/{task_name}.txt", "w") as file:
            print(fs)
            for f in fs:
                file.write(f.__name__ + "\n")