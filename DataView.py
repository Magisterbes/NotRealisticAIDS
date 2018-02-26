import numpy as np
import IOPart as io
import Classes as cl
from tqdm import tqdm
import Output as ou
import matplotlib.pyplot as plt
from matplotlib import animation
import datetime as dt


def DrawProgess(Pointsdata):

    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, 1), ylim=(0, 1.07))
    ax.grid()
    
    scatter = plt.scatter([], [])
    time_text = plt.text(0.01, 1,'')

    a=1
    def init():
        res = PointsToTwo(Pointsdata[0])
        scatter = plt.scatter(res[0], res[1], c=res[2],marker =".")
        time_text = plt.text(0.01, 1.02,"Week: %s, Infected: %s, Diagnosed: %s" % (str(0), str(res[3][0]+res[3][1]), str(res[3][1])))
        return scatter,time_text


    def animate(i):
        plt.clf()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, 1), ylim=(0, 1.05))
        ax.grid()
        res = PointsToTwo(Pointsdata[i])
        try:
            scatter = plt.scatter(res[0], res[1], c=res[2],marker ="." )
        except:
            a=1
        time_text = plt.text(0.01, 1.02,"Week: %s, Infected: %s, Diagnosed: %s" % (str(i), str(res[3][0]+res[3][1]), str(res[3][1])))
       # time_text.set_text()

        return scatter,time_text

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 520),
                             interval=1, blit=False , init_func=init)

    tm = (dt.datetime.now()- dt.datetime(2017,7,1)).total_seconds()
    ani.save('animation'+str(tm) +'.gif', writer='imagemagick', fps=15) 
    #mng = plt.get_current_fig_manager() 
    #mng.frame.Maximize(True) 
    plt.show()
   

def PointsToTwo(Points):
    bluex = []
    redx = []
    bluey = []
    redy = []

    for point in Points:
        if point[2] ==0:
            bluex.append(point[0])
            bluey.append(point[1])
        else:
            redx.append(point[0])
            redy.append(point[1])
    
    color = []
    if len(bluex)>0:
        color = ('g '*len(bluex)).strip().split(' ')
    if len(redx)>0:
        color.extend(('r '*len(redx)).strip().split(' '))
    count = [len(bluex),len(redx)]
    bluex.extend(redx)
    bluey.extend(redy)
    color = color[:len(bluey)]
    return (np.array(bluex), np.array(bluey),np.array(color),count)





if __name__ == '__main__':
   
    lines = io.FillFromFileLines(io.dir + "aids2.dat")
    

    arr = []

    for line in tqdm(lines):
        temp =  []
        spl = line.split(';')
        for tup in spl:
            temp.append(list(map(float,tup.split(','))))

        arr.append(temp)
    DrawProgess(arr)
