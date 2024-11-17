import importlib
import sandbox
from helper import compare_grid, hamming_distance, neural_distance
import numpy as np

MAX_DEPTH = 4

module = importlib.import_module("dsl")
# program = getattr(module, new_uuid)
library = []
for f in dir(module):
    if f[0].islower():
        library.append(getattr(module, f))

print("Length of library:", len(library))

def brute_force(train_inputs, train_outputs, f_list=[], depth=1, compute=0):
    if depth > MAX_DEPTH: return None, compute

    for f in library:
        compute=compute+1
        f_train_outputs = []
        f_works = True
        for i in range(len(train_inputs)):
            syntactical_correctness, out = sandbox.run(f, train_inputs[i])
            if not syntactical_correctness:
                f_works = False
                break
            
            f_train_outputs.append(out)

        if not f_works: continue
        
        if f_works:
            #check for task success
            success = True
            for i in range(len(train_inputs)):
                if not compare_grid(f_train_outputs[i], train_outputs[i]):
                    success = False
                    break
            if success: return f_list + [f], compute

            # else continue with brute force search
            fs, compute = brute_force(f_train_outputs, train_outputs, f_list=f_list+[f], depth=depth+1, compute=compute)
            if fs is not None:
                return fs, compute
    
    return None, compute


def hamming_guided_search(train_inputs, train_outputs, f_list=[], depth=1, compute=0):
    if depth > MAX_DEPTH: return None, compute

    priority_sorted_functions = []
    scores = []
    for f in library:
        score = hamming_distance(f, train_inputs, train_outputs)
        scores.append(score)

    sorted_indices = np.argsort(scores)
    priority_sorted_functions = [library[i] for i in sorted_indices]

    for f in priority_sorted_functions:
        compute=compute+1
        f_train_outputs = []
        f_works = True
        for i in range(len(train_inputs)):
            syntactical_correctness, out = sandbox.run(f, train_inputs[i])
            if not syntactical_correctness:
                f_works = False
                break
            
            f_train_outputs.append(out)

        if not f_works: continue
        
        if f_works:
            #check for task success
            success = True
            for i in range(len(train_inputs)):
                if not compare_grid(f_train_outputs[i], train_outputs[i]):
                    success = False
                    break
            if success: return f_list + [f], compute

            # else continue with brute force search
            fs, compute = hamming_guided_search(f_train_outputs, train_outputs, f_list=f_list+[f], depth=depth+1, compute=compute)
            if fs is not None:
                return fs, compute
    
    return None, compute


def neural_guided_search(train_inputs, train_outputs, f_list=[], depth=1, compute=0):
    if depth > MAX_DEPTH: return None, compute

    priority_sorted_functions = []
    scores = []
    for f in library:
        score = neural_distance(f, train_inputs, train_outputs)
        scores.append(score)

    sorted_indices = np.argsort(scores)
    priority_sorted_functions = [library[i] for i in sorted_indices]

    for f in priority_sorted_functions:
        compute=compute+1
        f_train_outputs = []
        f_works = True
        for i in range(len(train_inputs)):
            syntactical_correctness, out = sandbox.run(f, train_inputs[i])
            if not syntactical_correctness:
                f_works = False
                break
            
            f_train_outputs.append(out)

        if not f_works: continue
        
        if f_works:
            #check for task success
            success = True
            for i in range(len(train_inputs)):
                if not compare_grid(f_train_outputs[i], train_outputs[i]):
                    success = False
                    break
            if success: return f_list + [f], compute

            # else continue with brute force search
            fs, compute = neural_guided_search(f_train_outputs, train_outputs, f_list=f_list+[f], depth=depth+1, compute=compute)
            if fs is not None:
                return fs, compute
    
    return None, compute