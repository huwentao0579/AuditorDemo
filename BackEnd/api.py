import os
import pickle
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import re
import json
import pandas as pd
app = Flask(__name__)
CORS(app)
api = Api(app)
# Require a parser to parse our POST request.
parser = reqparse.RequestParser()
parser.add_argument("selected_column")
parser.add_argument("input2")
parser.add_argument("Support")
parser.add_argument("Deviation")
parser.add_argument("Violations")
parser.add_argument("Complex")
parser.add_argument("Constraints")
parser.add_argument("ID")
parser.add_argument("Integrity")
parser.add_argument("selected_data")
# Unpickle our model so we can use it!
if os.path.isfile("./our_model.pkl"):
  model = pickle.load(open("./our_model.pkl", "rb"))
else:
  raise FileNotFoundError
class Predict(Resource):
  def post(self):
    df = pd.read_csv("./dataset.csv", index_col = 0)
    df.columns = ['PATIENT_ID', 'VISIT_ID', 'ITEM_NO', 'ITEM_CLASS', 'ITEM_NAME', 'ITEM_CODE', 'ITEM_SPEC', 'AMOUNT',
                  'UNITS', 'ORDER_BY', 'PERFORMED_BY', 'COST', 'CHARGE']
    model.reload_data(df)
    args = parser.parse_args()
    temp_str = args['selected_column']
    selected_column = temp_str.split(",")
    input2 = args['input2']
    Support = float(args['Support'])
    Deviation = int(args['Deviation'])
    print(selected_column, Support,Deviation)
    y = model.predict(selected_column, input2, Support, Deviation)
    print(y)
    return {"output": y.to_json(orient='records')}
class Example(Resource):
  def post(self):
    args = parser.parse_args()
    Violations = args['Violations']
    Complex = args['Complex']
    Constraints = args['Constraints']
    ID = args['ID']
    Integrity = args['Integrity']
    y = model.examine(Integrity, Complex, Constraints, ID, Violations)
    temp = Complex.split('->')
    c1 = temp[0]
    c4 = temp[1]
    op = re.search('[\* + \- / ]', c4).group()
    tp = temp[1].split(op)
    c2 = tp[0]
    c3 = tp[1]
    tableLabel = [{'label': c1, 'align': 'center', 'width': 50, 'prop': c1},{'label': c2, 'align': 'center', 'width': 50,'prop': c2},{'label': c3, 'align': 'center', 'width': '100', 'prop': c3},{'label': c4, 'align': 'center', 'width': '400', 'prop': c4}]
    return {"output": y.to_json(orient='records'), "tableLabel": json.dumps(tableLabel)}

class Mark(Resource):
  def post(self):
    args = parser.parse_args()
    selected_data = args['selected_data']
    selected_data = selected_data.split(',')
    selected_data = [int(i) for i in selected_data]
    Index = model.data_index()
    print(Index)
    print(selected_data)
    for i in selected_data:
      try:
        Index.remove(i)
      except:
        continue
    df = model.df.loc[Index]
    print(df)
    model.data_tocsv(df)
    return None
api.add_resource(Predict,  "/predict")
api.add_resource(Example, '/example')
api.add_resource(Mark, '/Mark')

if __name__ == "__main__":
  app.run(debug=True)