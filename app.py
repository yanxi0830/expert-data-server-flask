from flask import Flask, render_template, send_file, request, jsonify, Response
import os
import pathlib
import io
import zipfile
import pickle
import json
import argparse

from utils import transfer_pickle2json, sample_from_partition

app = Flask(__name__)

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route("/nds/")
def home():
    return render_template('index.html')

@app.route("/nds/index.html")
def index():
    return render_template('index.html')

@app.route("/nds/paper.html")
def paper():
    return render_template('paper.html')

@app.route("/nds/terms.html")
def terms():
    return render_template('terms.html')

@app.route("/nds/privacy.html")
def privacy():
    return render_template('privacy.html')

@app.route("/nds/demo.html")
def demo():
    return render_template('demo.html')

@app.route("/nds/contribute.html")
def contribute():
    return render_template('contribute.html')

@app.route("/nds/NeuralDataServer_ClientFastAdapt.ipynb")
def download_coco_experts():
    script_path = 'scripts/NeuralDataServer_ClientFastAdapt.ipynb'
    return send_file(script_path, attachment_filename='NeuralDataServer_ClientFastAdapt.ipynb')


@app.route('/nds/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        save_path = os.path.join('tmp', 'z.pickle')
        file_val = request.files['file']
        file_val.save(save_path)
        z = pickle.load(open(save_path, 'rb'))
        json_graph = transfer_pickle2json(z)
        return jsonify(json_graph)
    return "UPLOAD-ENDPOINT"


@app.route('/nds/download-data', methods=['GET'])
def request_zip():
    budget = int(request.args.get('budget'))
    save_path = os.path.join('tmp', 'z.pickle')
    z = pickle.load(open(save_path, 'rb'))
    sampled_filenames = sample_from_partition(z, budget)

    json_file = json.dumps({"imageids": sampled_filenames})    # TODO: more detailed JSON? 

    return Response(json_file,
                    mimetype='application/json',
                    headers={'Content-Disposition':'attachment;filename=data.json'})

    # print("PLACEHOLDER FOR DOWNLOADING ZIP")
    # partition_dict_path = '/h/yanxi/git/expert-data-server/partition/res152--h-yanxi-Disk-datasets-coco-val2017--partition.pickle'
    # with open(partition_dict_path, 'rb') as f:
    #     partition_dict = pickle.load(f)

    # cluster_filepaths = partition_dict[0]

    # data = io.BytesIO()
    # with zipfile.ZipFile(data, mode='w') as z:
    #     for f_name in cluster_filepaths:
    #         z.write(f_name, os.path.basename(f_name))
    # data.seek(0)
    # return send_file(data, mimetype='application/zip', as_attachment=True, attachment_filename='data.zip')


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8002)

    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    app.run(port=args.port, threaded=True)
