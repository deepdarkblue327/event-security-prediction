reading=[]
words=[]

intensifiers = "never^d#much^w#amazingly^s#astoundingly^s#awful^s#barely^d#bloody^s#crazy^s#dead^s#dreadfully^s#colossally^s#especially^w#exceptionally^s#excessively^s#extremely^s#extraordinarily^s#fantastically^s#frightfully^w#fucking^s#fully^w#holy^s#incredibly^s#insanely^s#mightily^w#moderately^d#mostly^d#outrageously^s#phenomenally^s#preciously^w#quite^d#radically^w#rather^w#real^w#really^s#remarkably^w#right^w#sick^s#so^w#somewhat^d#strikingly^s#super^w#supremely^s#surpassingly^s#terribly^s#terrifically^s#too^w#totally^s#uncommonly^d#unusually^d#veritable^w#very^w#wicked^s"
inten = intensifiers.split("#")

negative = "no#is not#isnt#are not#arent#was not#wasnt#were not#werent#have not#havent#has not#hasnt#had not#hadnt#will not#wont#would not#wouldnt#do not#dont#does not#doesnt#did not#didnt#cannot#cant#could not#couldnt#should not#shouldnt#might not#mightnt#must not#mustnt"
arr=negative.split("#")

def checkWords():
    count=0
    for word in words:
        word.displayDetails()
    #     count+=1
    #     if count>5000:
    #         inputstring=input("continue?")
    #         if inputstring=="y":
    #             count=0
    # return
class Wrd:
    def __init__(self,word,value1,value2,prob1,prob2):
        self.word=word
        self.value1=value1
        self.value2=value2
        self.prob1=prob1
        self.prob2=prob2
    def displayDetails(self):
        print("Word: "+self.word+"\t values: "+str(self.value1)+" "+str(self.value2)+" "+str(self.prob1)+" "+str(self.prob2))

def start():
    f = open('valueswithprobability.txt')
    count=0
    while 1:
        readstring=f.readline()
        #print(readstring)
        #count+=1
        #print(str(count)+readstring)
        if readstring == "eof":
            #print("overLL")
            break
        reading.append(readstring)

    for word in reading:
        splitted=word.split("#")
        values=splitted[1].split()
        w=Wrd(splitted[0],float(values[1]),float(values[2]),float(values[3]),float(values[4]))
        words.append(w)
    return

def getValues(iword):

    vls=[]
    if len(iword)<=2:
        return "neutral"
    for w in words:
        if iword.lower() == w.word.lower():
            #print("Found "+iword+" and "+w.word)
            if w.prob1==w.prob2:
                return "neutral"
            if abs(w.prob1) > abs(w.prob2):
                vls.append(w.value1)
                vls.append(w.prob1)
                return vls
            else:
                vls.append(w.value2)
                vls.append(w.prob2)
                return vls

    return "neutral"

def checkNegation(word):
    for w in arr:
        if w==word or word.lower()=="not":
            print("negation found for "+word)
            return True
    #print("negation not found")
    return False

def intensify_find(arrk):
    for a in inten:
            strng = a.split("^")    #to get d,w,s value 1 2 and 3 respectively
            if strng[0] == arrk:
                if strng[1] == "d":
                    return 1
                else:
                    if strng[1] == "w":
                        return 2
                    else:
                        return 3
    return 0









#print(words)
