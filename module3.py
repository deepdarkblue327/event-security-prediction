import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig = plt.figure("Module 3")
ax1 = fig.gca()
ax1.set_autoscale_on(False)
f = 0
g = 0
value = 0
count = 0
neg = 0

def calc(f):
    global value, count, neg
    if float(f) < -25 and float(f) > -50:
        value += 1
        neg += 1
    elif float(f) <-50 and float(f) > -75:
        value += 2
        neg += 1
    elif float(f) < -75:
        value += 3
        neg += 1
    count += 1

def calcagain(val,cnt,neg):
    if neg > cnt/2:
        return neg/val*100
    else:
        return val/cnt*100


def animate(i):
    global value,count,neg
    count = 0
    value = 0
    neg = 0
    global f,g
    pullData = open("input.txt", "r").read()
    dataArray = pullData.split("\n")
    xar = []
    yar = []
    for eachLine in dataArray:
        if(len(eachLine) > 1):
            x,y = eachLine.split(',')
            xar.append(float(x))
            yar.append(float(y))
            calc(y)

    ax1.clear()
    ax1.plot([0,200],[0,0],'k--')
    ax1.plot([0,200],[-25,-25],'y--')
    ax1.plot([0,200],[-50,-50],'m--')
    ax1.plot([0,200],[-75,-75],'r--')
    ax1.plot(xar,yar)
    ax1.axis([0,200,-100,100])
    plt.xlabel("Tweets\n Criticality: " + str(calcagain(value,count,neg)) + "%")
    plt.ylabel(g)


ani = animation.FuncAnimation(fig,animate,interval = 100)

plt.show()