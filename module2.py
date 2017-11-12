import string
from tkinter import ttk, Tk, N, W, E, S, Text, END, StringVar, LEFT, X, Scrollbar, RIGHT, Y, Canvas
import normalsenti
from nltk.corpus import sentiwordnet as swn
from pymongo import MongoClient
import math

client1 = MongoClient()
db1 = client1.tweets_database
print("initiated")
list=db1.search_tweets_keyword.find()
print(str(list.count())+" number of tweets obtained from database")
tweets=[]


arrayoftweetsvalues = []
wp = 0
wn = 0
ap = 0
an = 0
fp = 0
fn = 0
fullcount=0
pvar1=0
pvar2=0
pvar3=0

nvar1=0
nvar2=0
nvar3=0

neutralvar1=0
normalsenti.start()
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
#normalsenti.checkWords()
index=0
root = Tk()
rw=2
root.title(" Module #3 ")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe2=ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0,rowspan = 3, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
#scrollbar = Scrollbar(root)
#scrollbar.pack( side = RIGHT, fill=Y )
#canvas.grid(column=0, row=1, sticky=(N, W, E, S))
canvas = Canvas(mainframe2, borderwidth=0)
mainframe2.grid(column=0, row=3, sticky=(N, W, E, S))
subframe=ttk.Frame(canvas,padding="3 3 12 12")
subframe.columnconfigure(1, weight=1)
subframe.columnconfigure(0, weight=1)
subframe.rowconfigure(0, weight=1)
vsb = Scrollbar(mainframe2, orient="vertical", command=canvas.yview)
vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.configure(yscrollcommand=vsb.set)
canvas.create_window((4,4), window=subframe, anchor="nw")
subframe.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
tx1=Text(mainframe,width=130,height=10)
resultEntry=ttk.Entry(mainframe, width=120)
#tx1.grid(column=1,row=1,sticky=(W,E))
tx1.pack(fill=X)
label=ttk.Label(subframe, text="Words after splitting:")
label.grid(column=0, row=1, sticky=(W, E))
#label.pack(padx=5, pady=10, side=LEFT)
sentilabel=ttk.Label(subframe, text="Values:")
sentilabel.grid(column=1, row=1, sticky=(W,E))
#sentilabel.pack(padx=5, pady=10, side=LEFT)
wordslabel=ttk.Label(subframe, text="Words list:")
wordslabel.grid(column=0, row=2, sticky=(W, E))
entr=[]
vals=[]
negcount=0
negCheck=False
intCheck=0
intenValue=0
cleared= False
def cumulate():
    for num in range(0,200):
        nexttweet()
    print("statistics: "+str(pvar1)+" "+str(pvar2)+" "+str(pvar3)+" "+str(neutralvar1)+" "+str(nvar1)+" "+str(nvar2)+" "+str(nvar3))
def addGUIelements():
    global rw
    entr.clear()
    vals.clear()
    for num in range(0,40):
        entr.append(ttk.Entry(subframe, width=90))
    for n in range(0,40):
        vals.append(ttk.Entry(subframe, width=90))
        #.grid(column=0, row=rw, sticky=(W, E))
    rw=2
    for e in entr:
        e.grid(column=0, row=rw, sticky=(W, E))
        rw=rw+1
    rw1=2
    for e1 in vals:
        e1.grid(column=1, row=rw1, sticky=(W, E))
        rw1=rw1+1
    return
addGUIelements()

for t in list:
   tweets.append(t.get("TWEET"))
def negFormula(value): #Negation formula
    if value < 0:
        neg = (value+100)/2
        if 10 < neg:
            return neg
        else:
            return 10
    else:
        neg = (value-100)/2
        if -10 > neg:
            return neg
        else:
            return -10

def finalSenti(f,e):
        if(abs(f)>25 or abs(e)>0.5):
            return f
        else:
            return 0
def clear():
    global cleared
    cleared=True
    for c in subframe.winfo_children():
        c.destroy()
        # label=ttk.Label(subframe, text="Words after splitting:")
        # label.grid(column=0, row=1, sticky=(W, E))
        # #label.pack(padx=5, pady=10, side=LEFT)
        # sentilabel=ttk.Label(subframe, text="Values:")
        # sentilabel.grid(column=1, row=1, sticky=(W,E))
        # #sentilabel.pack(padx=5, pady=10, side=LEFT)
        # wordslabel=ttk.Label(subframe, text="Words list:")
        # wordslabel.grid(column=0, row=2, sticky=(W, E))
    return
def removePunctuations(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s if ch not in exclude)
    return s


def countingposnegwords():
    global wp,wn,fp,fn
    global ap,an
    wp = 0
    wn = 0
    ap = 0
    an = 0
    fp = 0
    fn = 0
    for a in arrayoftweetsvalues:
        if a >= 0.0:
            wp += 1
            ap += a
        if a < 0:
            wn += 1
            an += a
    if wp!=0:
        ap /= wp
    else:
        ap=0
    if wn!=0:
        an /= wn
    else:
        an=0


def fpfn():
    global fp,fn
    if ap==0:
        somevaluep=0
    else:
        somevaluep = ap/(2 - math.log10(3.5*wp))
    if an==0:
        somevaluen=0
    else:
        somevaluen = an/(2 - math.log10(3.5*wn))
    if(100 > somevaluep):
        fp = somevaluep
    else:
        fp = 100

    if(-100 < somevaluen):
        fn = somevaluen
    else:
        fn = -100

arrayoftweetsprobabilities = []

ep = 0
en = 0

def countingposnegwords_e():
    global wp,wn
    global ap,an,ep,en
    ep=0
    en=0
    ap=0
    an=0
    wp=0
    wn=0
    count = 0
    for a in arrayoftweetsvalues:
        b = arrayoftweetsprobabilities[count]
        if b > 0.5:
            if a > 0:
                wp += 1
                ap += b
            if a < 0:
                wn += 1
                an += b
        count += 1
    if wp==0:
        ap=0
    else:
         ap /= wp
    if wn==0:
         an=0
    else:
         an /= wn

def epen():
    global ep,en
    ep=en=0
    if ap==0:
        somevaluep=0
    else:
        somevaluep = ap/(2 - math.log10(3.5*wp))
    if an==0:
        somevaluen=0
    else:
        somevaluen = an/(2 - math.log10(3.5*wn))
    if(1 > somevaluep):
        ep = somevaluep
    else:
        ep = 1

    if(-1 < somevaluen):
        en = somevaluen
    else:
        en = -1

def nexttweet(): #Function triggered by button press
    global arrayoftweetsvalues,pvar1,pvar2,pvar3,nvar1,nvar2,nvar3,neutralvar1
    global index,negCheck,negcount,intCheck,fullcount
    global cleared,intenValue
    global rw,resultEntry
    del arrayoftweetsvalues[:]
    del arrayoftweetsprobabilities[:]
    fullcount+=1
    #Check if last tweet reached
    if index>=len(tweets):
        resultEntry.insert(0,"End of tweets")
        clear()
        return
    #select next tweet for analysis
    tw=tweets[index]
    arr=tw.split()
    count=0 #row number
    if cleared==False:
        for e in vals:
            e.delete(0, 'end')
        for e in entr:
            e.delete(0, 'end')
    else:
        addGUIelements()
    for s in arr:
        #Process every word in current tweet.
      #try:
        s1=removePunctuations(s)
        #Applying negation
        if negCheck==True and negcount<=2:
            negcount+=1
            stri=normalsenti.getValues(s1)
            if stri=="neutral":
                vals[count].insert(0,stri)
                entr[count].insert(0,s1+" ")
                count+=1
                print("Negation: Word "+s1+" found with : "+stri)
                continue
            else:
                vl= negFormula(stri[0])
                print("Negation: formula returned: "+str(vl))
                vals[count].insert(0,vl)
                arrayoftweetsvalues.append(vl)
                arrayoftweetsprobabilities.append(stri[1])
                entr[count].insert(0,s1+" ")
                negCheck=False
                print("Word "+s1+" found with value after negation considered: "+str(vl))
                negcount=0
                count+=1
                continue
        #Applying intensification for the word that follows the intensifier(Found in previous
        # Iteration)
        if intCheck!=0:
             #check second intensifier
             intCheck2=normalsenti.intensify_find(s1)
             if intCheck2!=0:
                entr[count].insert(0,s+" ")
                print("Applying Intensifier for word: "+s1)
                vals[count].insert(0,"Applying Intensifier for word")
                count+=1
                continue
             vl=normalsenti.getValues(s1)
             if vl!="neutral":
                if intCheck == 1:
                    vl[0] = 0.5*vl[0] #intensity application
                if intCheck == 2:
                    vl[0] = 1.5*vl[0] #intensity application
                if intCheck == 3:
                    vl[0] = 2.0*vl[0] #intensity application
                print(str(intCheck)+" Intens "+str(vl[0]))
                arrayoftweetsvalues.append(vl[0])
                arrayoftweetsprobabilities.append(vl[1])
                vals[count].insert(0,vl[0])
             if vl=="neutral":
                 vals[count].insert(0,vl)
             #arrayoftweetsvalues.append(vl[0])
             #arrayoftweetsprobabilities.append(vl[1])
             entr[count].insert(0,s1+" ")
             intCheck=0
             print("Word "+s1+" value after Intensification considered: "+str(vl[0]))
             count += 1
             continue
        #Intensifier Check. Check next word to apply intensification
        intCheck=normalsenti.intensify_find(s1)
        if intCheck!=0:
            entr[count].insert(0,s+" ")
            print("Applying Intensifier for word: "+s1+" "+str(intCheck))
            vals[count].insert(0,"Applying Intensifier for word")
            count+=1
            continue
        #Negation check. Using negCheck boolean to indicate that following 3 words should be checked.
        negCheck=normalsenti.checkNegation(s1)
        if negCheck==True:
            entr[count].insert(0,s+" ")
            vals[count].insert(0,"Negation applied")
            count+=1
            continue
        #Analysis without intensifier or negation. Normal analysis of tweet words
        vl=normalsenti.getValues(s1)
        if vl!="neutral":
            vals[count].insert(0,vl[0])
            arrayoftweetsvalues.append(vl[0])
            print("Word: "+s1+" found with value "+str(vl[0]))
            print(str(vl[0])+" appended")
            arrayoftweetsprobabilities.append(vl[1])
        else:
            try:
                vals[count].insert(0,vl)
                print("Word: "+s1+" found with value "+str(vl))
            except Exception as e:
             print(e)
             pass

        try:
             entr[count].insert(0,s+" ")
        except Exception as e:
             print(e)
             pass
        count+=1
      #except Exception as e:
          #print("Exception in outer most for loop")
    #End of For loop. All words of tweet calculated.
    try:
        tx1.insert(END,str(index)+" \t"+tweets[index]+"\n")
    except Exception as e:
            print(e)
    index+=1 #Tweets iterator variable
    cleared=False
    for value in arrayoftweetsvalues:
         print("Added "+str(value)+" for calculating Fp/Fn")
    print("length of arrayoftweetvalues is : "+str(len(arrayoftweetsvalues)))
    for value in arrayoftweetsprobabilities:
         print("Added "+str(value)+" for calculating ep/en")
    print("length of arrayoftweetsprobabilities is : "+str(len(arrayoftweetsprobabilities)))
    countingposnegwords()
    fpfn()
    countingposnegwords_e()
    epen()
    resultEntry.delete(0,END)
    resultEntry.insert(0,"\t Fp: "+str(fp)+"\t Fn: "+str(fn))
    resultEntry.insert(0,"\t Ep: "+str(ep)+"\t En: "+str(en))
    final_value = 0
    if wn == 0:
        final_value = finalSenti(fp,ep)
    elif wp == 0:
            final_value = finalSenti(fn,en)
    else:
        if ep - en > 0.1:
            final_value = finalSenti(fp,ep)
        elif en - ep > 0.1:
            final_value = finalSenti(fn,en)
        else:
            if fp + fn > 0:
                final_value = finalSenti(fp,ep)
            elif fp + fn < 0:
                final_value = finalSenti(fn,en)
            else:
                final_value = 0
    resultEntry.insert(0,"\t Final value is "+str(final_value))
    print("-------------------------------------------------------------"+str(fullcount))
    with open("input.txt","a") as f:
        f.write(str(index)+","+str(final_value)+"\n")
    if final_value<25 and final_value>-25:
        neutralvar1+=1
    elif final_value>=25 and final_value<50:
            pvar1+=1
    elif final_value>=50 and final_value<75:
            pvar2+=1
    elif final_value>=75 and final_value<=100:
            pvar3+=1
    elif final_value<=-25 and final_value>-50:
            nvar1+=1
    elif final_value<=-50 and final_value>-75:
            nvar2+=1
    elif final_value<=-75 and final_value>=-100:
            nvar3+=1
    return


#Adding buttons to GUI and starting main loop to listen for events
ttk.Button(mainframe, text="Analyze Next Tweet",command=cumulate).pack()
resultEntry.pack()
nexttweet()
ttk.Button(mainframe, text="Clear screen",command=clear).pack()

#for()
root.mainloop()
