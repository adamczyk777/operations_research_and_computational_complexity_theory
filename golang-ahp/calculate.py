import sys
import json
import numpy as np
import copy

def calculate(node, result_size):
    vector = get_vector(node, sys.argv[1])
    if node['children'] is not None and node['children'] != []:
        result_vector = np.array([0] * result_size)
        for idx, child in enumerate(node['children']):
            child_vector = np.array(calculate(child, result_size))
            result_vector = result_vector + vector[idx] * child_vector
        return result_vector
    else:
        return vector

def get_vector(node, method):
    if method == 'norm':
        return norm(node)
    elif method == 'gmm':
        return gmm(node)

def geo_mean(np_array):
    return np_array.prod()**(1.0/len(np_array))

def gmm(node):
    matrix = np.array(node['preferences'])
    out_vector = np.apply_along_axis(geo_mean, 1, matrix)
    return out_vector / out_vector.sum()

def norm(node):
    matrix = np.array(node['preferences'])
    matrix = matrix / matrix.sum(axis=0)
    out_vector = np.mean(matrix, axis=1)
    return out_vector / out_vector.sum()


method = sys.argv[1]

file = open('ahp.json', 'r+')
data = json.loads(file.read())

result_size = len(data['alternatives'])

print(calculate(data['goal'], result_size))
# print(calculate(data['goal']))

