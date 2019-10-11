import pickle
import operator
import re
import numpy as np


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
    p = re.compile("([a-z]+)([0-9]+)", re.IGNORECASE)
    # p.match("coco2")
    # p.match("openimages32")

    dataset2partition_file = {
        'coco': '',
        'openimages': ''
    }
    
    # for partition in pickle_dict:



def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()