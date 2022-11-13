import pandas as pd

def save_dict_as_csv(file_name, dictionary):
  dataframe = pd.DataFrame(dictionary)
  dataframe.to_csv(file_name, index=False, header=True)