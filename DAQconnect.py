class Connect:
    def __init__(self):
        import nidaqmx as ni
        import time
        import numpy as np
        import matplotlib.pyplot as plt
        from lmfit import Model, Parameter
        from lmfit.models import LorentzianModel
        import pandas as pd
        import csv
        
        try:
            self.task1.close()
            self.task2.close()
            self.task3.close()
        except AttributeError:
            pass
            
        self.task1=ni.Task()
        self.task1.ao_channels.add_ao_voltage_chan('Dev1/ao0','mychannel',-10,10) #Output channel which controls the piezo for the laser
        self.task1.start()
        
        self.task2=ni.Task()
        self.task2.ao_channels.add_ao_voltage_chan('Dev1/ao1','mychannel',-10,10) #output channel which controls oscilloscope triggering
        self.task2.start()
        
        self.task3=ni.Task()
        self.task3.ai_channels.add_ai_voltage_chan('Dev1/ai0',max_val=6,min_val=-6) #input channel for photodetector
        self.task3.start()
