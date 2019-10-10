import pickle

temp_nodes = {
    "nodes": [
        {"id": "CENTER", "group": 1},
        {"id": "COCO[0]", "group": 2},
        {"id": "COCO[1]", "group": 3},
        {"id": "COCO[2]", "group": 4},
        {"id": "COCO[3]", "group": 5},
        {"id": "COCO[4]", "group": 6},
        {"id": "COCO[5]", "group": 7}
    ],
    "links": [
        {"source": "CENTER", "target": "COCO[0]", "value": 46.2891},
        {"source": "CENTER", "target": "COCO[1]", "value": 57.7973},
        {"source": "CENTER", "target": "COCO[2]", "value": 55.1241},
        {"source": "CENTER", "target": "COCO[3]", "value": 42.7405},
        {"source": "CENTER", "target": "COCO[4]", "value": 57},
        {"source": "CENTER", "target": "COCO[5]", "value": 40}
    ]
}

def transfer_pickle2json(pickle_dict):
    # {'old_coco_k6_expert4': 53.6566, 'old_coco_k6_expert3': 46.9727, 'old_coco_k6_expert0': 47.3202, 'old_coco_k6_expert2': 53.2849, 'old_coco_k6_expert5': 62.9665, 'old_coco_k6_expert1': 67.9512}
    res = {
        "nodes": [{"id": "CLIENT DATASET", "group": 0}],
        "links": []
    }
    for i, expert_name in enumerate(pickle_dict):
        node = {"id": expert_name, "group": i}
        res["nodes"].append(node)
        link = {"source": "CLIENT DATASET", "target": expert_name, "value": pickle_dict[expert_name]}
        res["links"].append(link)
    
    return res