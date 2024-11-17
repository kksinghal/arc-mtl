import json
import search
import os
import sandbox
from helper import compare_grid
from tqdm import tqdm

SPLIT = "training" # or "evaluation"
LOGS = "brute_force"
correct = 0
total = 0
correct_task_names = []
incorrect_task_names = []

files = os.listdir(f"ARC-AGI/data/{SPLIT}")
files = [f.split(".")[0] for f in files]
if not os.path.exists(f"./{LOGS}/solved"):
    os.makedirs(f"./{LOGS}/solved")
if not os.path.exists(f"./{LOGS}/unsolved"):
    os.makedirs(f"./{LOGS}/unsolved")

total_compute = 0
for task_name in tqdm(files):
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

    fs, compute = search.neural_guided_search(train_inputs, train_outputs) # TODO
    total_compute += compute
    solved = True
    if fs:
        for i in range(len(test_inputs)):
            output = test_inputs[i]
            for f in fs:
                syntactical_correctness, output = sandbox.run(f, output)
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
    print(correct/total, correct, total, compute)
    if solved:
        with open(f"./{LOGS}/solved/{task_name}.txt", "w") as file:
            file.write(f"Compute {compute} \n")
            for f in fs:
                file.write(f.__name__ + "\n")

    elif fs and not solved:
        with open(f"./{LOGS}/unsolved/{task_name}.txt", "w") as file:
            file.write(f"Compute {compute} \n")
            for f in fs:
                file.write(f.__name__ + "\n")


print("Accuracy:", correct/total, correct, total, total_compute)