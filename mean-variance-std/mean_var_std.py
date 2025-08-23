import numpy as np

def calculate(lst):
    if len(lst) != 9:
        raise ValueError("List must contain nine numbers.")
    
    matrix = np.array(lst).reshape(3, 3)

    calculations = {
        'mean': [matrix.mean(axis=0).tolist(), matrix.mean(axis=1).tolist(), float(matrix.mean())],
        'variance': [matrix.var(axis=0).tolist(), matrix.var(axis=1).tolist(), float(matrix.var())],
        'standard deviation': [matrix.std(axis=0).tolist(), matrix.std(axis=1).tolist(), float(matrix.std())],
        'max': [matrix.max(axis=0).tolist(), matrix.max(axis=1).tolist(), float(matrix.max())],
        'min': [matrix.min(axis=0).tolist(), matrix.min(axis=1).tolist(), float(matrix.min())],
        'sum': [matrix.sum(axis=0).tolist(), matrix.sum(axis=1).tolist(), float(matrix.sum())]
    }

    return calculations
