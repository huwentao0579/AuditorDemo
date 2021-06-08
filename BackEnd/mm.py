from itertools import combinations
import pandas as pd

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




class Model:

  def __init__(self,selected_column, input2, Support, Deviation,df):
    self.selected_column = selected_column
    self.input2 = input2
    self.Support = Support
    self.Deviation = Deviation
    self.df = df

  def data_index(self):
    Index = [i for i in self.df.index]
    return Index

  def reload_data(self, df):
    self.df = df

  def data_tocsv(self, df):
    df.to_csv('./dataset.csv')

  def data_select(self, df, selected_column):
    number_co = []
    str_co = []
    for i in selected_column:
      if df.dtypes[i] == object:
        str_co.append(i)
      else:
        number_co.append(i)
    number_conbination = list(combinations(number_co, 2))
    return str_co, number_conbination

  def cache_algorithm(self, Deviation, can_co, df, present_df):
    for temp_co in can_co:
      d = pd.DataFrame(columns=[''])
      for i in range(4):
        if i == 0:
          temp_df = df[temp_co[0]] + df[temp_co[1]]
          d[temp_co[0] + '+' + temp_co[1]] = temp_df
        elif i == 1:
          temp_df = df[temp_co[0]] - df[temp_co[1]]
          d[temp_co[0] + '-' + temp_co[1]] = temp_df
        elif i == 2:
          temp_df = df[temp_co[0]] * df[temp_co[1]]
          d[temp_co[0] + '*' + temp_co[1]] = temp_df
        elif i == 3:
          if sum(df[temp_co[1]]) > 0:
            continue
          temp_df = df[temp_co[0]] / df[temp_co[1]]
          d[temp_co[0] + '/' + temp_co[1]] = temp_df
        try:
          min_range = round(temp_df.mean() - Deviation * temp_df.std(), 2)
          max_range = round(temp_df.mean() + Deviation * temp_df.std(), 2)
        except:
          continue
        n_range = '[' + str(min_range) + ', ' + str(max_range) + ']'
        # min_df = temp_df[temp_df < min_range]
        # max_df = temp_df[temp_df > max_range]
        min_df = temp_df < min_range
        max_df = temp_df > max_range
        globals()['CIC' + str(CIC.cicCount)] = CIC('_', d.columns[-1], '_', n_range, 1, Deviation, min_df, max_df,
                                                   temp_co[0])
        tp = globals()['CIC' + str(CIC.cicCount)]
        CICs = tp.category
        CICs2 = tp.c_v
        CICs3 = tp.n_v
        new = pd.DataFrame(
          {'Complex': CICs, 'Integrity': CICs2, 'Constraints (CICs)': CICs3, 'Support': 1, 'Deviation': Deviation,
           '#Violations': int(tp.violations)}, index=[0])
        present_df = present_df.append(new, ignore_index=True)

    return present_df

  def algebra_algorithm(self, Support, Deviation, str_co, can_co, df, present_df):
    for temp in str_co:
      list_value = df[temp].unique()
      for temp_v in list_value:
        value = temp_v
        if sum(df[temp] == temp_v) > Support * len(df):
          support = round(sum(df[temp] == temp_v) / len(df), 3)
          for temp_co in can_co:
            tp_df = df[df[temp] == temp_v]
            d = pd.DataFrame(columns=[''])
            for i in range(4):
              if i == 0:
                temp_df = tp_df[temp_co[0]] + tp_df[temp_co[1]]
                d[temp_co[0] + '+' + temp_co[1]] = temp_df
              elif i == 1:
                temp_df = tp_df[temp_co[0]] - tp_df[temp_co[1]]
                d[temp_co[0] + '-' + temp_co[1]] = temp_df
              elif i == 2:
                temp_df = tp_df[temp_co[0]] * tp_df[temp_co[1]]
                d[temp_co[0] + '*' + temp_co[1]] = temp_df
              elif i == 3:
                if sum(df[temp_co[1]]) > 0:
                  continue
                temp_df = tp_df[temp_co[0]] / tp_df[temp_co[1]]
                d[temp_co[0] + '/' + temp_co[1]] = temp_df
              try:
                min_range = round(temp_df.mean() - Deviation * temp_df.std(), 2)
                max_range = round(temp_df.mean() + Deviation * temp_df.std(), 2)
              except:
                continue
              n_range = '[' + str(min_range) + ', ' + str(max_range) + ']'
              min_df = temp_df < min_range
              max_df = temp_df > max_range
              globals()['CIC' + str(CIC.cicCount)] = CIC(temp, d.columns[-1], value, n_range, 1, Deviation, min_df,
                                                         max_df,
                                                         temp_co[0])
              tp = globals()['CIC' + str(CIC.cicCount)]
              CICs = tp.category
              CICs2 = tp.c_v
              CICs3 = tp.n_v
              new = pd.DataFrame(
                {'Complex': CICs, 'Integrity': CICs2, 'Constraints (CICs)': CICs3, 'Support': support,
                 'Deviation': Deviation,
                 '#Violations': int(tp.violations)}, index=[0])
              present_df = present_df.append(new, ignore_index=True)
    return present_df


  def predict(self,selected_column, input2, Support,Deviation):
    str_co, can_co = self.data_select(self.df, selected_column)
    present_df = pd.DataFrame(columns=['Complex', 'Integrity', 'Constraints (CICs)', 'Support', 'Deviation', '#Violations'])
    temp_df = self.cache_algorithm(Deviation, can_co, self.df, present_df)
    temp_df = temp_df.append(self.algebra_algorithm(Support, Deviation, str_co, can_co, self.df, temp_df))
    temp_df.index = range(len(temp_df))
    temp_df['ID'] = temp_df.index
    return temp_df

  def examine(self, Integrity, Complex, Constraints, ID,Violations):
    if Integrity == '_':
      tp = Complex.split('->')
      if tp[1].find('+') != -1:
        first_co = tp[1][:tp[1].find('+')]
        second_co =tp[1][tp[1].find('+')+1:]
        temp_column = [first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        temp_df = self.df[first_co] + self.df[second_co]
        min_v = temp_df < normal_value[0]
        max_v = temp_df > normal_value[1]
        tp_df = self.df[temp_column][min_v + max_v]
        new_co = tp_df.iloc[:, 0] + tp_df.iloc[:, -1]
      elif tp[1].find('-') != -1:
        first_co = tp[1][:tp[1].find('-')]
        second_co = tp[1][tp[1].find('-') + 1:]
        temp_column = [first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        temp_df = self.df[first_co] - self.df[second_co]
        min_v = temp_df < normal_value[0]
        max_v = temp_df > normal_value[1]
        tp_df = self.df[temp_column][min_v + max_v]
        new_co = tp_df.iloc[:, 0] - tp_df.iloc[:, -1]
      elif tp[1].find('*') != -1:
        first_co = tp[1][:tp[1].find('*')]
        second_co = tp[1][tp[1].find('*') + 1:]
        temp_column = [first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        temp_df = self.df[first_co] * self.df[second_co]
        min_v = temp_df < normal_value[0]
        max_v = temp_df > normal_value[1]
        tp_df = self.df[temp_column][min_v + max_v]
        new_co = tp_df.iloc[:, 0] * tp_df.iloc[:, -1]
      elif tp[1].find('/') != -1:
        first_co = tp[1][:tp[1].find('/')]
        second_co = tp[1][tp[1].find('/') + 1:]
        temp_column = [first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        temp_df = self.df[first_co] * self.df[second_co]
        min_v = temp_df < normal_value[0]
        max_v = temp_df > normal_value[1]
        tp_df = self.df[temp_column][min_v + max_v]
        new_co = tp_df.iloc[:, 0] / tp_df.iloc[:, -1]

      tp_str = ' not in ' + str(normal_value)
      ttt = [str(i) + tp_str for i in new_co]
      tp_df[tp[1]] = ttt
      tp_df['order'] = [i for i in tp_df.index]
      tp_df['_'] = ['_' for i in range(int(Violations))]
      value_support = 1- (int(Violations) / len(min_v))
      value_support = round(value_support, 4)
      value_support = [value_support for i in range(int(Violations))]
      Id = [ID for i in range(int(Violations))]
      tp_df['Support'] = value_support
      tp_df['ID'] = Id
      return tp_df
    else:
      tp = Complex.split('->')
      t_df = self.df[tp[0]] == Integrity
      df = self.df[t_df]
      if tp[1].find('+') != -1:
        first_co = tp[1][:tp[1].find('+')]
        second_co =tp[1][tp[1].find('+')+1:]
        temp_column = [tp[0], first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        tt_df = df[first_co] + df[second_co]
        min_v = tt_df < normal_value[0]
        max_v = tt_df > normal_value[1]
        tp_df = df[temp_column][min_v + max_v]
        new_co = tp_df.iloc[:, 1] + tp_df.iloc[:, -1]
      elif tp[1].find('-') != -1:
        first_co = tp[1][:tp[1].find('-')]
        second_co = tp[1][tp[1].find('-') + 1:]
        temp_column = [tp[0], first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        tt_df = df[first_co] - df[second_co]
        min_v = tt_df < normal_value[0]
        max_v = tt_df > normal_value[1]
        tp_df = df[temp_column][min_v + max_v]
        new_co = tp_df.iloc[:, 1] - tp_df.iloc[:, -1]
      elif tp[1].find('*') != -1:
        first_co = tp[1][:tp[1].find('*')]
        second_co = tp[1][tp[1].find('*') + 1:]
        temp_column = [tp[0], first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        tt_df = df[first_co] * df[second_co]
        min_v = tt_df < normal_value[0]
        max_v = tt_df > normal_value[1]
        temp = min_v + max_v
        tp_df = df[temp_column][temp]
        new_co = tp_df.iloc[:, 1] * tp_df.iloc[:, -1]
      elif tp[1].find('/') != -1:
        first_co = tp[1][:tp[1].find('/')]
        second_co = tp[1][tp[1].find('/') + 1:]
        temp_column = [tp[0], first_co, second_co]
        normal_value = Constraints.strip('[]').split(', ')
        normal_value = [float(i) for i in normal_value]
        tt_df = df[first_co] * df[second_co]
        min_v = tt_df < normal_value[0]
        max_v = tt_df > normal_value[1]
        tp_df = df[temp_column][min_v + max_v]
        new_co = tp_df.iloc[:, 1] / tp_df.iloc[:, -1]

      tp_str = ' not in ' + str(normal_value)
      ttt = [str(i) + tp_str for i in new_co]
      tp_df[tp[1]] = ttt
      tp_df['order'] = [i for i in tp_df.index]
      value_support = 1- (int(Violations) / len(min_v))
      value_support = round(value_support, 4)
      value_support = [value_support for i in range(int(Violations))]
      Id = [ID for i in range(int(Violations))]
      print(tp_df, value_support)
      tp_df['Support'] = value_support
      tp_df['ID'] = Id
      return tp_df





