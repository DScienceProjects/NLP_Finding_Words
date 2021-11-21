from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
import os
from wsgiref import simple_server
from logger_class import Logger
import Constants

from NltkPro import NltkProcessing

app = Flask(__name__)  # initialising the flask app with the name 'app'
log = Logger("IndexPage")
pred = NltkProcessing()


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    log.add_info_log(Constants.URL_HIT)
    return "Flask app is running"

@app.route('/extract_words',methods=["GET","POST"])
@cross_origin()
def extract_words():
    if request.method == "POST":
        try:
            desc = request.form['description']
            words = list(pred.process(desc))
            return jsonify(words=words)


        except Exception as e:
            log.add_exception_log(Constants.EXCEPTION_HANDLING + " extract_words() "+e)
            return 'something is wrong'




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

port = int(os.getenv("PORT", 5001))
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #app.run()
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host, port=port, app=app)
    # httpd = simple_server.make_server(host='127.0.0.1', port=5000, app=app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
