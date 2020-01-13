from tkinter import messagebox
import nltk
import pyttsx3
import pymongo
import db_handler
import threading
import time

questions = ["blank"]
threads = []
statusobj = []

def printl(str):
    statusobj[0].configure(text=statusobj[0].cget("text")+"--"+str)

class myThread (threading.Thread):
   def __init__(self, text):
       threading.Thread.__init__(self)
       self.engine = pyttsx3.init()
       self.engine.setProperty('rate', self.engine.getProperty('rate') - 50)
       self.text = text

   def run(self):
       time.sleep(2)
       printl("speech Started")
       self.engine.say(self.text)
       self.engine.runAndWait()
       printl("Speech Stoppeed")

   def stop(self):
       try:
           self.engine.endLoop()
       except:
           printl("Run loop is not started caught")
       self.engine.stop()
       del(self.engine)

   def __del__(self):
       printl("Deleting  Thread")


def show_message(str):
    msg = messagebox.askyesnocancel("Question input",str)
    print("Input is : ", msg)

def sayIt(str=""):

    thread1 = myThread(str)
    if (len(threads) == 1):
        threads.pop(0)
    threads.append(thread1)
    thread1.start()

def stopIt():
    if(len(threads) == 1):
        threads[0].stop()
        del(threads[0])
    else:
        printl("Thread is already Deleted.")


def process_what_question(tokenized):
    #sayIt(str="Getting answer from database")
    def_item = ''
    for i in range(2, len(tokenized)):
        def_item += tokenized[i]

    strb = def_item.strip()
    search_term = strb.lower()
    res = db_handler.get_definition(search_term)
    if res[0] == 1:
        sayIt(res[1])
        messagebox.showinfo("Answer", "Answer in def: " + res[1])
        return True
    print("definition not available ")
    return False

def process_direct_question():
    print("processing direct question : "+questions[0])
    res = db_handler.get_normal_question(questions[0])
    if res[0] == 1:
        sayIt(res[1])
        messagebox.showinfo("Answer", "Answer in direct: " + res[1])
        return True
    else:
        sayIt(res[1])
        messagebox.showinfo("Answer", "Answer is not available here also: " + res[1])
        return True



def process_question(question):
    questions.pop(0)
    questions.append(question)

    try:
        tokenized = nltk.word_tokenize(question)
        tagged = nltk.pos_tag(tokenized)

        gram2 = '''
        Chunk: {<WP.?><VBZ.?><JJ|JJS|JJR|NN|NNS|NNP|NNPS>*}
        '''
        chunkParser = nltk.RegexpParser(gram2)
        chunked = chunkParser.parse(tagged)


        try:
            temp = chunked[0].label()
            rrr = process_what_question(tokenized)
            if(rrr == False):
                process_direct_question()
        except:
            print("In Direct questions bcs grammer not matched")
            process_direct_question()

    except Exception as e:
        print(str(e))


def process_question(question):
    questions.pop(0)
    questions.append(question)

    try:
        tokenized = nltk.word_tokenize(question)
        tagged = nltk.pos_tag(tokenized)

        gram2 = '''
        Chunk: {<WP.?><VBZ.?><JJ|JJS|JJR|NN|NNS|NNP|NNPS>*}
        '''
        chunkParser = nltk.RegexpParser(gram2)
        chunked = chunkParser.parse(tagged)


        try:
            temp = chunked[0].label()
            rrr = process_what_question(tokenized)
            if(rrr == False):
                process_direct_question()
        except:
            print("In Direct questions bcs grammer not matched")
            process_direct_question()

    except Exception as e:
        print(str(e))


#test_mt()