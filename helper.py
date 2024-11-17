import sandbox
import numpy as np
from transformation_to_vec import TransformationToVec

def compare_grid(grid1, grid2):
    if len(grid1) != len(grid2):
        return False
    
    for row1, row2 in zip(grid1, grid2):
        if len(row1) != len(row2) or any(elem1 != elem2 for elem1, elem2 in zip(row1, row2)):
            return False
    
    return True


"""
Parameters:
    inp: List[2d list], input
    true_output: List[2d list]
    realised_output: List[2d list]

Returns: float in range[0,1], similarity between the transformation from input to true output and realised output
"""
def hamming_distance(f, inputs, outputs):
    assert len(inputs) == len(outputs)
    num_samples = len(inputs)
    total_score = 0

    realised_outputs = []
    for i in range(num_samples):
        syntactical_correctness, realised_output = sandbox.run(f, inputs[i])
        if not syntactical_correctness: return np.inf
        realised_outputs.append(realised_output)

    for o1, o2 in zip(outputs, realised_outputs):
        d = 0
        for i in range(min(len(o1), len(o2))):
            for j in range(min(len(o1[i]), len(o2[i]))):
                if o1[i][j] != o2[i][j]: d+=1
        
        total_score += max(len(o1),len(o2)) * max(len(o1[0]),len(o2[0])) - min(len(o1),len(o2)) * min(len(o1[0]),len(o2[0])) + d
    return total_score/len(inputs)


def pixelwise_comparison_score(f, inputs, outputs):
    assert len(inputs) == len(outputs)
    num_samples = len(inputs)
    total_score = 0
    for i in range(num_samples):
        _, realised_output = sandbox.run(f, inputs[i])
        total_score += compare_grid(outputs[i], realised_output)

    return total_score/num_samples


transformation_to_vec = TransformationToVec(model_dir="./concept-classifiers")
def neural_distance(f, inputs, outputs):
    assert len(inputs) == len(outputs)
    num_samples = len(inputs)
    total_score = 0
    
    realised_outputs = []
    for i in range(num_samples):
        syntactical_correctness, realised_output = sandbox.run(f, inputs[i])
        if not syntactical_correctness: return np.inf
        realised_outputs.append(realised_output)
        
    true_transformation_embedding = transformation_to_vec.get(inputs, outputs)
    pred_transformation_embedding = transformation_to_vec.get(inputs, realised_outputs)

    return np.sqrt(np.square(np.array(true_transformation_embedding) - np.array(pred_transformation_embedding)).sum())