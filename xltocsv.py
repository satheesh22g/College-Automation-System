import pandas as pd

read_file = pd.read_excel (input("input filename(without xtension)")+'.xlsx')
read_file.to_csv (input("output filename(without xtension)")+'.csv', index = None, header=True)