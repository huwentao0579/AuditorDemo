from itertools import combinations
import pandas as pd
import pickle
from mm import Model
class CIC:
  cicCount = -1

  def __init__(self,category,num,c_v, n_v, support, deviation, min_df, max_df, first_co):
    self.category = str(category) + '->' + str(num)
    self.num = num
    self.c_v = c_v
    self.n_v = n_v
    self.support = support
    self.deviation = deviation
    self.min_df = min_df
    self.max_df = max_df
    self.first_co = first_co
    CIC.cicCount += 1
    self.violations = sum(self.min_df) + sum(self.max_df)




#Getting data
df = pd.read_csv("./dataset.csv", index_col=0)
df.columns = ['PATIENT_ID', 'VISIT_ID', 'ITEM_NO', 'ITEM_CLASS', 'ITEM_NAME', 'ITEM_CODE', 'ITEM_SPEC', 'AMOUNT', 'UNITS', 'ORDER_BY', 'PERFORMED_BY', 'COST', 'CHARGE']
present_df = pd.DataFrame(columns=['Complex', 'Integrity', 'Constraints (CICs)', 'Support', 'Deviation', '#Violations'])

selected_column=['ITEM_CODE', 'PATIENT_ID', 'ORDER_BY', 'AMOUNT', 'CHARGE', 'COST']
input2 = ''
Support = 0.1
Deviation = 4
# t= [selected_column, input2, Support, Deviation]


clf = Model(selected_column, input2, Support, Deviation, df)
temp_df = clf.predict(selected_column,input2,Support,Deviation)
print(temp_df)
# tp_df = clf.examine("'300403'", "ORDER_BY->CHARGE+AMOUNT",  "[-2.87, 12.37]", '27', '3')
# print(tp_df)
# print(tp_df.to_json(orient='records'))
# print(temp_df.to_json(orient='records'))
# print(clf.data_index())
pickle.dump(clf, open("./our_model.pkl", "wb"))