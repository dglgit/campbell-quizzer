import random
import json
import datetime
import os
savePrefix='./saves/'

def isQuestionStart(line):
    nums='0123456789'
    if line[0] not in nums:
        return False
def getProblem(s,j):
    for l in range(j,len(s)):
        line=s[l]
        if line.startswith('A)'):
            question=''.join(s[j:l])
            for k in range(j,len(s)):
                if s[k].startswith('Answer'):
                    break
            return (question,''.join( s[l:k]).strip(),s[k][-2],k)


def getChapterQuestions(s:list,chapterNum):
    problems={}
    #{chapterNumber:[(question, choices, answer),...],...}
    i=0
    count=0
    while i<len(s) and count<len(chapterNum):
        
        line=s[i]
        if line.startswith(f'Chapter {chapterNum[count]}'):
            questions=[]
            for j in range(i,len(s)):
                line=s[j]
                if line[0] in '123456789' and (line.find(')')==1 or line.find(')')==2):
                    question, choices, answer, k=getProblem(s,j)
                    questions.append((question, choices, answer)) 
                if line.startswith(f'Chapter {chapterNum[count]+1}'):
                    break
            problems[chapterNum[count]]=questions
            count+=1
            i=k
            
        else:
            i+=1
    return problems
def printQuestion(q):
    """
    enum{
        stop: -1
        save: -2
        reset: -3
        Skip: None
        default: tried(int)
    }
    """
    print(q[0])
    print(q[1])
    print(q[2])
def askQuestion(q, tries=3):
    question, choices,answer=q
    print(question)
    print(choices)
    tried=0
    while tried<tries:
        pred=input('answer: ')
        if pred=='stop':
            return -1
        if pred=='save':
            return -2
        if pred=='skip':
            print('skipping question')
            return None
        if pred.lower()==answer.lower():
            print("correct")
            return tried
        else:
            print('incorrect')
            tried+=1
    print(f'the correct answer was: {answer}')
    return tried

def simpleQuiz(qs):
    ch=input('choose chapter: ')
    chapterSaves=[]
    for f in os.listdir(savePrefix):
        if ch in f.split('_')[0]:
            chapterSaves.append(savePrefix+f)
    if len(chapterSaves)==0:    
        doRandom=input('random?[y/N] ')=='y'
        qb=qs[ch]
        idxs=list(range(len(qb)))
        questionHistory={}
        tries=input("tries per question(default 1): ")
        tries=1 if tries=='' else int(tries)
        if doRandom:
            random.shuffle(idxs)
    else:
        print("chapter save file(s) found, please choose one")
        print(''.join([f'{i}: {chapterSaves[i]} ' for i in range(len(chapterSaves))]))
        realCh=input("save (press enter to make new file): ")
        if not realCh:#if user doesnt want to load from file
            doRandom=input('random?[y/N] ')=='y'
            qb=qs[ch]
            idxs=list(range(len(qb)))
            questionHistory={}
            tries=input("tries per question(default 1): ")
            tries=1 if tries=='' else int(tries)
            if doRandom:
                random.shuffle(idxs)
        else:
            with open(chapterSaves[int(realCh)], 'r') as ff:
                questionHistory=json.load(ff)
                qb=qs[ch]
                idxs=[int(i) for i in set(questionHistory.keys())^set([str(i) for i in range(len(qb))])]
                doRandom=input('random?[y/N] ')=='y'
                tries=input("tries per question(default 1): ")
                tries=1 if tries=='' else int(tries)
                if doRandom:
                    random.shuffle(idxs)
                else:
                    idxs=sorted(idxs)
    correct=0
    total=0
    skipped=0
    avgTries=0
    for q in idxs:
        r=askQuestion(qb[q],tries)
        if r==-2:
            fname=input("save session name(press enter to autogenerate file or 'same' to use the current file): ")
            if not fname:
                fname=savePrefix+f'save{ch}_'+datetime.datetime.now().strftime("%m-%d-%y")
            elif fname=='same':
                fname=chapterSaves[int(realCh)]
            
            with open(fname, 'w') as f:
                json.dump(questionHistory,f)
        if r==-1:
            break
        if r is None:
            skipped+=1
            questionHistory[int(q)]=-1
            continue
        else:
            avgTries+=r
            correct+=r<tries
            questionHistory[int(q)]=r<tries
            total+=1
    print(f'{correct}/{total} questions correctly answered, {skipped} skipped, average amount of tries: {avgTries/total}')

if __name__=='__main__':
    #with open('testBank.txt','r') as f:
    #    txt=list(f)
    #a=getChapterQuestions(txt, list(range(1, 57)))
    #with open('testBank.json','r') as j:
        #json.dump(a,j) #for some reason when you dump to json the keys get turned to strings
    with open('testBank.json','r') as j:
        a=json.load(j)
    print(list(a))
    simpleQuiz(a)
