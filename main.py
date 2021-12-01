from flask import Flask, render_template, request, jsonify, send_from_directory, Response, url_for, redirect
from flask_cors import CORS, cross_origin
import os
from wsgiref import simple_server

from werkzeug.utils import secure_filename

from logger_class import Logger
import Constants
import DataManipulation as dm
from NltkPro import NltkProcessing

app = Flask(__name__)  # initialising the flask app with the name 'app'
log = Logger("IndexPage")
pred = NltkProcessing()

newFileName = ""


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    log.add_info_log(Constants.URL_HIT)
    return render_template("index.html")


@app.route('/extract_words', methods=["GET", "POST"])
@cross_origin()
def extract_words():
    if request.method == "POST":
        try:
            desc = request.form['description']
            words = list(pred.process(desc))
            return jsonify(words=words)


        except Exception as e:
            log.add_exception_log(Constants.EXCEPTION_HANDLING + " extract_words() " + e)
            return 'something is wrong'


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        os.makedirs(os.path.join(app.instance_path, Constants.UPLOAD_FOLDER), exist_ok=True)
        os.makedirs(os.path.join(app.instance_path, Constants.OUTPUT_FOLDER), exist_ok=True)
        f.save(os.path.join(app.instance_path, Constants.UPLOAD_FOLDER, secure_filename(f.filename)))
        newFileName = f.filename
        datamani = dm.DataManipulation()
        f = datamani.cleanFile(os.path.join(app.instance_path, Constants.UPLOAD_FOLDER, secure_filename(f.filename)))
        datamani.convertDataTocsv(f, app.instance_path, newFileName)

        return download(newFileName)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # return send_from_directory(os.path.join(app.instance_path, Constants.Output_FOLDER), newFileName+ "file.csv",as_attachment=True)
    return send_from_directory(os.path.join(app.instance_path, Constants.OUTPUT_FOLDER), filename, as_attachment=True)


port = int(os.getenv("PORT", 5001))
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # app.run()
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host, port=port, app=app)
    # httpd = simple_server.make_server(host='127.0.0.1', port=5000, app=app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
