from flask import Flask, render_template, send_file, request
import os
app = Flask(__name__)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

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

@app.route('/upload', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        print("GOT POST")
        file_val = request.files['file']
        file_val.save(os.path.join('tmp', 'z.pickle'))
    return "UPLOADED FILE TODO"

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port: 5000
if __name__ == "__main__":
    app.run()
