import importlib
import sandbox
from helper import compare_grid

module = importlib.import_module("dsl")
# program = getattr(module, new_uuid)
library = []
for f in dir(module):
    if f[0].islower():
        library.append(getattr(module, f))

print("Length of library:", len(library))

def brute_force(train_inputs, train_outputs, f_list=[], depth=1):
    if depth > 5: return None

    for f in library:
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
            if success: return f_list + [f]

            # else continue with brute force search
            brute_force(f_train_outputs, train_outputs, f_list=f_list+[f], depth=depth+1)
