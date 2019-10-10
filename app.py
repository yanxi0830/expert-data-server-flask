from flask import Flask, render_template, send_file, request
import os
import pathlib
import io
import zipfile
import pickle

app = Flask(__name__)


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
        print("GOT POST")
        file_val = request.files['file']
        file_val.save(os.path.join('tmp', 'z.pickle'))

    return "UPLOADED FILE TODO"


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
