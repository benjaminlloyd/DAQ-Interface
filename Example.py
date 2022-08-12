from DAQconnect import Connect
from DAQ import DAQ

connect=Connect()
D=DAQ(connect.task1,connect.task2,connect.task3)
D.polarization triggering(.18,400,0.0006)

D.task1.close()
D.task2.close()
D.task3.close()