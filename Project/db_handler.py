import pymongo
from urllib.request import urlopen, URLError
import requests

db = None
global_db = None

def check_first():
    global db
    if db is None:
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.be

def check_global():
    global global_db
    if global_db is None:
        client = pymongo.MongoClient("mongodb://ankur:ankur1234@ds213229.mlab.com:13229/be")
        global_db = client.be

def get_definition(question):
    ans = db.definitions.find_one({"question": question})
    ret = [0, ""]
    if ans:
        print("answer is available")
        ret[0] = 1
        ret[1] = ans['answer']
    else:
        print("ans is not available")
        ret[0] = 0
        ret[1] = "Definition is not available in database"
    return ret


def get_normal_question(question):
    ans = db.questions.find_one({"question": question})
    print(ans)
    ret = [0, ""]
    if ans:
        print("answer is available")
        ret[0] = 1
        ret[1] = ans['answer']
    else:
        print("ans is not available in direct")
        ret[0] = 0
        ret[1] = "Answer is not available in database"
    return ret


def get_diff(term1, term2, fg=0):
    ans = db.differences.find_one({"term1": term1, "term2": term2})
    print(ans)
    ret = [0, ""]
    if ans:
        print("answer is available")
        ret[0] = 1
        ret[1] = ans['difference']
    else:
        if fg == 0:
            ret = get_diff(term2, term1, 1)
        else:
            print("ans is not available in direct")
            ret[0] = 0
            ret[1] = "Answer is not available in database"
    return ret


def get_reading_content(chapter_id):
    ans = db.reading_content.find_one({"chapter_id": chapter_id})
    return ans


def get_all_chapters():
    res = db.reading_content.find({}).sort("chapter_id", 1)
    ret = []
    for rs in res:
        ret.append([rs['chapter_id'], rs['chapter_name']])
    return ret


def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err:
        return False


def synchronize_database():
    if not internet_on():
        return False

    check_first()
    check_global()
    db.definitions.delete_many({})
    db.questions.delete_many({})
    db.reading_content.delete_many({})
    db.differences.delete_many({})

    ans = global_db.definitions.find({})
    ans_list = []
    for an in ans:
        ans_list.append(an)
    db.definitions.insert_many(ans_list)

    ans = global_db.questions.find({})
    ans_list = []
    for an in ans:
        ans_list.append(an)
    db.questions.insert_many(ans_list)

    ans = global_db.reading_content.find({})
    ans_list = []
    for an in ans:
        ans_list.append(an)
    db.reading_content.insert_many(ans_list)

    ans = global_db.differences.find({})
    ans_list = []
    for an in ans:
        ans_list.append(an)
    db.differences.insert_many(ans_list)

    return True


def send_to_expert_system(que, typ):
    if not internet_on():
        return False
    check_first()

    url2 = "http://www.a3n.in/project/add_expert_question.php"
    PARAMS = {'question': que, "user_id": "12345", "type": typ}
    r = requests.get(url=url2, params=PARAMS)
    data = r.text
    if data == "true":
        return True
    return False

def get_exp_user_data():
    url2 = "http://www.a3n.in/project/get_expert_user.php"
    PARAMS = {"user_id": "12345"}
    r = requests.get(url=url2, params=PARAMS)
    data = r.json()
    newData = []
    fullData = {"check": 0, "data": None}
    try:
        for i in data:
            print("value of dlag" + i['flag'])
            if i['flag'] == '0':
                print("Null answer found")
                newData.append({"question": i['question'], "answer": "The question is not yet answered by Experts"})
            else:
                print("Ready answer found")
                newData.append(i)
        fullData['check'] = 1
        fullData['data'] = newData
    except:
        fullData['check'] = 0
        fullData['data'] = newData
    return fullData

def get_exp_ans(que):
    url2 = "http://www.a3n.in/project/get_expert_ans.php"
    PARAMS = {"question": que}
    r = requests.get(url=url2, params=PARAMS)
    data = r.json()
    return data

def test_fun():
    check_first()
    check_global()
    ans = global_db.expert_questions.find({})
    print(type(ans))
    ans_list = list(ans)
    print(ans_list)



#test_fun()
#synchronize_database()

#send_to_expert_system("ex", "ll")