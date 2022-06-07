import random
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
    ch=int(input('choose chapter: '))
    doRandom=input('random?[y/n] ')=='y'
    qb=qs[ch]
    idxs=list(range(len(qb)))
    tries=input("tries per question(default 1): ")
    tries=1 if tries=='' else int(tries)
    if doRandom:
        random.shuffle(idxs)
    correct=0
    total=0
    skipped=0
    for q in idxs:
        result=askQuestion(qb[q],tries)
        if result ==-1:
            break
        if result is None:
            skipped+=1
        else:
            total+=1
            correct+=result<tries
    print(f'{correct}/{total} questions correctly answered, {skipped} skipped')

if __name__=='__main__':
    with open('testBank.txt','r') as f:
        txt=list(f)
    a=getChapterQuestions(txt, list(range(1, 57)))
    print(len(a))
    print(list(a))
    simpleQuiz(a)
