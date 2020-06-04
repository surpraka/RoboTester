# -*- coding: utf-8 -*-
"""
Created on Wed May 13 11:03:20 2020

@author: surpraka
"""

import os                                                                       
from multiprocessing import Pool                                                
import sys                                                                      
                                                                                
def run_process(process):                                                             
    os.system('python {}'.format(process))                                       
                                                                                
if __name__ == "__main__":
    processes = ('Regg1.py '+sys.argv[1]+' '+sys.argv[4], 'Regg2.py '+sys.argv[2]+' '+sys.argv[4],'Regg3.py '+sys.argv[3]+' '+sys.argv[4])                                   
    pool = Pool(processes=3)                                                        
    pool.map(run_process, processes) 
