import nltk
import db_handler
from tkinter import messagebox

question = ""
typ = None

def process_what():
    tk = nltk.word_tokenize(question)
    tagged = nltk.pos_tag(tk)
    gram = '''
            Chunk: {<WP.?><VBZ.?><JJ|JJS|JJR|NN|NNS|NNP|NNPS>*}
            '''
    chunk_parser = nltk.RegexpParser(gram)
    parsed = chunk_parser.parse(tagged)

    ret_val = []
    try:
        temp = parsed[0].label()
        def_item = ''
        for i in range(2, len(tk)):
            def_item += tk[i]

        if(tk[2] == 'difference'):
            typ = 'diff'
            ret_val.append(0)
            return ret_val

        strb = def_item.strip()
        search_term = strb.lower()
        res = db_handler.get_definition(search_term)
        if res[0] == 1:
            ret_val.append(1)
            ret_val.append(res[1])
            return ret_val
        else:
            typ = "def"
            ret_val.append(2)
            return ret_val
    except:
        ret_val.append(0)
        return ret_val


def process_def():
    tk = nltk.word_tokenize(question)
    ret_val = []
    if(tk[0] == 'define' or tk[0] == 'explain'):
        def_item = '';
        for i in range(1, len(tk)):
            def_item += tk[i]

        strb = def_item.strip()
        search_term = strb.lower()
        res = db_handler.get_definition(search_term)
        if res[0] == 1:
            ret_val.append(1)
            ret_val.append(res[1])
            return ret_val
        else:
            typ="def"
            ret_val.append(2)
            return ret_val
    else:
        ret_val.append(0)
        return ret_val


def process_diff():
    tk = nltk.word_tokenize(question)
    tagged = nltk.pos_tag(tk)
    gram = '''
            Chunk: {<WP.?><VBZ.?><NN.?><IN.?><JJ|JJS|JJR|NN|NNS|NNP|NNPS|VBG>*<CC.?><JJ|JJS|JJR|NN|NNS|NNP|NNPS|VBG>*}
            '''
    chunk_parser = nltk.RegexpParser(gram)
    parsed = chunk_parser.parse(tagged)

    ret_val = []
    try:
        temp = parsed[0].label()

        term1 = ''
        term2 = ''
        last = 0
        for i in range(4, len(tk)):
            if(tk[i] == 'and'):
                last = i+1
                break
            term1 += ' ' + tk[i]

        for i in range(last, len(tk)):
            term2 += ' ' + tk[i]

        #print("term1 : "+term1+"\t Term2 : "+term2)
        t1 = term1.strip().lower()
        t2 = term2.strip().lower()

        res = db_handler.get_diff(t1, t2)

        if res[0] == 1:
            ret_val.append(1)
            ret_val.append(res[1])
            return ret_val
        else:
            typ = "diff"
            ret_val.append(2)
            return ret_val
    except:
        ret_val.append(0)
        return ret_val


def process_dict():
    res = db_handler.get_normal_question(question)
    ret_val = []
    if res[0] == 1:
        ret_val.append(1)
        ret_val.append(res[1])
        return ret_val
    else:
        ret_val.append(0)
        return ret_val


def process_question(que):
    global question
    question = que

    wh = process_what()
    if wh[0] == 1:
        return [wh, typ]

    wdi = process_diff()
    if wdi[0] == 1:
        return [wdi, typ]

    wdf = process_def()
    if wdf[0] == 1:
        return [wdf, typ]

    wd = process_dict()
    if wd[0] == 1:
        return [wd, typ]

    if db_handler.internet_on():
        ed = db_handler.get_exp_ans(que)
        if ed['flag'] == 1:
            return [[1, ed['answer']], typ]

    ret_val = [[0], typ]
    return ret_val

'''
question = "what is difference between good method overloading and bad method overriding"
parsed  = process_diff()
if parsed[0]:
    print("chunk is available "+ str(parsed[1]))
else:
    print("chunk is not available" + str(parsed[1]))
'''