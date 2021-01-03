import datetime
import time

def times():
    d=datetime.date.today()
    d1=str(d)
    t=time.localtime()
    t1=str(t[3])+':'+str(t[4])+':'+str(t[5])
    d3=d1+'  '+t1
    print(d3)
times()