import pickle
import operator
import re
import numpy as np
import os

def transfer_pickle2json(pickle_dict):
    # Given {'coco4': 53.6566, 'coco3': 46.9727, 'coco0': 47.3202, 'coco2': 53.2849, 'coco5': 62.9665, 'coco6': 67.9512}
    res = {
        "nodes": [{"id": "CLIENT DATASET", "group": 0, "value": 1.5}],
        "links": []
    }

    max_perf = max(pickle_dict.values())
    min_perf = min(pickle_dict.values())
    delta = max_perf - min_perf
    for i, expert_name in enumerate(pickle_dict):
        normalized_value = (pickle_dict[expert_name] - min_perf) / delta
        node = {"id": "{}".format(expert_name),
                "group": i, 
                "value": normalized_value}
        res["nodes"].append(node)
        link = {"source": "CLIENT DATASET", "target": expert_name, "value": pickle_dict[expert_name]}
        res["links"].append(link)
    
    return res

def sample_from_partition(pickle_dict):
    """
    Given pickle_dict={'coco4': 53.6566, 'coco3': 46.9727, 'coco0': 47.3202, 'coco2': 53.2849, 'coco5': 62.9665, 'coco6': 67.9512}
    Use it to sample from static pre-defined partition={0: [list of filepaths]}
    """
    p = re.compile("([^0-9]+)([0-9]+)", re.IGNORECASE)

    dataset2partition_file = {
        'coco': os.path.join('partitions', 'coco-partition.pickle'),
        'openimages': os.path.join('partitions', 'openimages-partition.pickle')
    }
    
    dataset2partition = {
        k: pickle.load(open(dataset2partition_file[k], 'rb')) for k in dataset2partition_file
    }

    # map pickle_dict transfer performance to softmax probability
    expert_names = []
    expert_perfs = []
    for e in pickle_dict:
        expert_names.append(e)
        expert_perfs.append(pickle_dict[e])
    
    expert_perfs = np.array(expert_perfs)
    expert_perfs = (expert_perfs - np.min(expert_perfs)) / (np.max(expert_perfs) - np.min(expert_perfs))
    expert_perfs = expert_perfs * 100

    expert_probs = softmax(expert_perfs)
    print(expert_probs)
    print(expert_names)

    # make list of file names
    # make list of probs mapping filename to 1/len(cluster)*probability
    filenames = []
    filenames_probs = []
    for i, e in enumerate(expert_names):
        dataset, cluster_idx = p.match(e).groups()
        cluster_idx = int(cluster_idx)
        partition = dataset2partition[dataset]
        cluster_filepaths = partition['clusters'][cluster_idx]
        filenames.extend(cluster_filepaths)
        filenames_probs.extend([1.0/len(cluster_filepaths) * expert_probs[i]] * len(cluster_filepaths))

    filenames_probs = np.array(filenames_probs)
    # sampling filenames
    filenames_probs /= filenames_probs.sum()
    sample_size = 117266    # TODO: size according to client request
    sample_size = 500
    sampled_indices = np.random.choice(len(filenames_probs), sample_size, replace=False, p=filenames_probs)
    
    sampled_filenames = [filenames[i] for i in sampled_indices]
    # print(sampled_filenames)

    return sampled_filenames   

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()