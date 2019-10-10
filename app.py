from flask import Flask, render_template, send_file, request, jsonify
import os
import pathlib
import io
import zipfile
import pickle
from utils import transfer_pickle2json

app = Flask(__name__)
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

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/download_coco_experts.sh")
def download_coco_experts():
    script_path = 'scripts/download_coco_experts.sh'
    return send_file(script_path, attachment_filename='download_coco_experts.sh')


@app.route("/fast_adapt.sh")
def fast_adapt():
    script_path = 'scripts/fast_adapt.sh'
    return send_file(script_path, attachment_filename='fast_adapt.sh')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        save_path = os.path.join('tmp', 'z.pickle')
        file_val = request.files['file']
        file_val.save(save_path)
        z = pickle.load(open(save_path, 'rb'))
        json_graph = transfer_pickle2json(z)
        return jsonify(json_graph)
    return "/upload ENDPOINT"


@app.route('/download-zip', methods=['GET'])
def request_zip():
    print("PLACEHOLDER FOR DOWNLOADING ZIP")
    partition_dict_path = '/h/yanxi/git/expert-data-server/partition/res152--h-yanxi-Disk-datasets-coco-val2017--partition.pickle'
    with open(partition_dict_path, 'rb') as f:
        partition_dict = pickle.load(f)

    cluster_filepaths = partition_dict[0]

    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in cluster_filepaths:
            z.write(f_name, os.path.basename(f_name))
    data.seek(0)
    return send_file(data, mimetype='application/zip', as_attachment=True, attachment_filename='data.zip')


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port: 5000
if __name__ == "__main__":
    app.run()
