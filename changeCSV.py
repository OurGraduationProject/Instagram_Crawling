import pandas as pd
import numpy as np


test = pd.read_csv('test.txt', sep=',', index_col=0)
test.index.name = 'Sequence'
test.columns = ['Address']
test.to_cv('data/Address.txt', index = False)

# https://doorbw.tistory.com/172 pandas 사이트