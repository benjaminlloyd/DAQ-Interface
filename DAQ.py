class DAQ:
    
    def __init__(self,task1,task2,task3):
        import time
        import numpy as np
        import matplotlib.pyplot as plt
        from lmfit import Model, Parameter
        from lmfit.models import LorentzianModel
        import pandas as pd
        import csv
        
        self.task1=task1
        self.task2=task2
        self.task3=task3
        
    def polarization_triggering(arg,Vfin,poin,delay):
        import time
        task1=arg.task1
        task2=arg.task2
        sett=np.asarray(np.linspace(0,Vfin,poin)) #sets the resolution and scope of the piezo wavelength sweep
        try:
            i=0
            while True:
                x=sett[i] #all the piezo lengths to try
                if i==0:
                    time.sleep(delay) #delay for DAQ #normally 0.00006
                    task2.write(0)#sends TTL falling edge trigger
                    task1.write(x) #sets piezo length
                    task2.write(3.6)#resets trigger signal
                task1.write(x) #sets piezo length
                time.sleep(delay) #delay for DAQ
                i=(i+1)%(len(sett)-1) #repeat
        except:
            pass
        finally:
                print("Done")
                
    def sweep(arg,Vfin,poin,delay):
        task1=arg.task1
        task2=arg.task3
        data=[] #data list
        sett=np.asarray(np.linspace(0,Vfin,poin)) #sets scan parameters
        try:
            for i in sett:
                task1.write(i)
                time.sleep(delay)
                data.append(task3.read(5))
                time.sleep(delay)
                
        except:
            pass
        finally:
            print("Done")
            task1.write(0) #resets the piezo when done
        return data
                
    def takedata(arg):
        task1=arg.task1
        task3=arg.task3
        task1.write(0)
        time.sleep(3)
        x=sweep(task1,task3)
        xx=[np.mean(i) for i in x]
        return xx
   
    def processdata(data,stop):
        maxx=max(data)
        start=0
        #stop should be (actual voltage)/(15*0.689/7) * 20 pm
        #if raw 2 V sweep,this corresponds to 25.414 pm
        y=[10*np.log10(i/maxx) for i in x]
        wave=np.asarray(np.linspace(start,stop,len(x)))
        return wave,y
    
    def loretntzian(x,A,Q,x0):
        gamma=x0/(2*Q)
        f=[A/(np.pi*gamma)*1/(1+4*np.power(Q*(i-x0)/x0,2)) for i in x]
        return f
    
    def Qextraction(rawdata,lambdaa):
        inputt=np.asarray(refine(rawdata)[1])
        xputt=np.asarray(refine(rawdata)[0])
        model=LorentzianModel()
        params=model.guess(inputt,x=xputt)
        result=model.fit(inputt,params,x=xputt)
        print(result.fit_report())
        result.plot_fit()
        result.params.pretty_print()
        plt.show()
        print(lambdaa*1000/result.params['fwhm'])
        