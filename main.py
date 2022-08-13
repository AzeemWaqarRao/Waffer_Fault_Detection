import sys

import pandas as pd
from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_jsonpify import jsonpify
from flask_cors import CORS, cross_origin
from Training_Validation.training_validation import Training_Validation
from Model.preprocessing import Preprocessor
from Clustering.clustering import Clustering
from Model.model_finder import Model_Finder
import flask_monitoringdashboard as dashboard
from Prediction_Validation.prediction_validation import Prediction_Validation
from Data_Validation.validate_data import Data_Validation
from Predict_Result.predict_result import Predict_Result

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


def deleteDB(path):

    try:
        os.remove(path)
    except Exception as e:
        print(e)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('temp.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        deleteDB(os.path.join("DataBase","Training_Data.db"))
        path = request.form['path']
        print(path)
        tv = Training_Validation(path)
        tv.validate_data()

        pr = Preprocessor("Training_Data.csv")
        pr.preprocess_train()

        cl = Clustering()
        X, list_of_clusters = cl.clustering()

        X['label'] = pd.read_csv("y.csv").iloc[:, 1:]

        model_finder = Model_Finder(X, list_of_clusters)
        model_finder.get_model()

    except ValueError:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return Response("Error Occurred! %s" % e)

    return Response("Training successfull!!")


@app.route("/predict", methods=['POST'])
@cross_origin()

def predictRouteClient():
    try:
        deleteDB(os.path.join("DataBase", "Prediction_Data.db"))
        # Prediction
        print(0)
        path = request.form['path']
        print(1)
        pv = Prediction_Validation(path)
        pv.validate_data()
        print(2)
        pr = Preprocessor("Prediction_Data.csv")
        pr.preprocess_predict()
        print(3)
        predict = Predict_Result()
        predict.predict()
        print(4)
        df = pd.read_csv("Predict_Result/prediction.csv")

        df_list = df.values.tolist()
        df = jsonpify(df_list)
        return df

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
