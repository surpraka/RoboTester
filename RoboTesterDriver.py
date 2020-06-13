# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 23:45:40 2020

@author: surpraka
"""
import pandas as pd
import os

df = pd.read_excel(r"TestCases.xlsx", sheet_name= "Driver")
threadCount = int(df['Parallel - ThreadCount'].tolist()[0])
print(threadCount)

os.system('python -m pytest -n '+str(threadCount))
