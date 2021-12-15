__version__ = '1.0.0'
from .convert2yamamoto import toYamamotoFile
from flask import (Flask, request, send_file)
import pandas as pd
import datetime


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=("POST", "GET"))
    def index():
        if request.method == "GET":
            return app.send_static_file('index.html')
        else:
            temperature = int(request.form["temperature"])
            eta = float(request.form["eta"])
            test0 = int(request.form["test0"])
            test1 = int(request.form["test1"])
            test2 = int(request.form["test2"])
            test3 = int(request.form["test3"])
            result = int(request.form["result"])
            file_func = {"csv": pd.read_csv, "xlsx": pd.read_excel, "pkl": pd.read_pickle, "pickle": pd.read_pickle, "tsv": pd.read_table}
            jij = file_func[request.files["jij"].filename.split(".")[-1]](request.files["jij"], header=None).to_numpy()
            hi = file_func[request.files["hi"].filename.split(".")[-1]](request.files["hi"], header=None).to_numpy().ravel()
            file = toYamamotoFile(jij, hi, temperature, eta, test0, test1, test2, test3, result)
            return send_file(file, as_attachment=True, attachment_filename=datetime.datetime.now().strftime("%m%d_%H%M%S_") + 'YamaFPGA.zip', mimetype='application/zip')

    return app


if __name__ == "__main":
    app = create_app()
    app.run(port=8000, debug=True)
