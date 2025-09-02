from flask import Flask, render_template, request, redirect, flash, url_for, session
import MySQLdb
import time

import os
import subprocess

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pyttsx3
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


app = Flask (__name__)
app.secret_key = "secret key"

@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html')


# Admin Login
@app.route("/adminlogin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        uname=request.form["uname"]
        pword=request.form["pword"]

        if uname=="Admin" and pword=="Admin":
            return render_template("adminhome.html")
        else:
            return render_template("adminlogin.html", msg="Your Login attempt was not successful. Please try again!!")
    return render_template("adminlogin.html")

# New User Registration
@app.route("/userregistration", methods=["GET", "POST"])
def user_registration():
    db = MySQLdb.connect("localhost", "root", "root", "VQADB")
    c1 = db.cursor()

    if request.method == "POST" :
        if request.form["b1"] == "Register":
            emailid = request.form["emailid"]
            c1.execute("select * from usertable where emailid='%s'" %emailid)
            row =c1.fetchone()
            if (row is not None):
                return render_template("userregistration.html", msg="Email ID Already Found!!")

            name = request.form["name"]
            gender = request.form["gender"]
            age = int(request.form["age"])
            address = request.form["address"]
            cname = request.form["cname"]

            mno = request.form["mno"]
            pword = request.form["pword"]

            c1.execute("insert into usertable(name,gender,age,address,cname,mno,emailid,pword) values('%s','%s','%d','%s','%s','%s','%s','%s')" %(name,gender,age,address,cname,mno,emailid,pword))
            db.commit()

            return render_template("userregistration.html", msg="User Details Inserted!!!")

    return render_template("userregistration.html", msg="")


# Admin View User
@app.route("/adminviewuser")
def admin_viewuser():
    db = MySQLdb.connect("localhost", "root", "root", "vqadb")
    c1 = db.cursor()
    c1.execute("select * from usertable")
    data = c1.fetchall()
    return render_template("adminviewuser.html", data=data)


# User Login
@app.route("/userlogin", methods=["GET","POST"])
def userlogin():
    if request.method == "POST":
        db = MySQLdb.connect("localhost", "root", "root", "vqadb")
        c1 = db.cursor()
        emailid=request.form["emailid"]
        pword=request.form["pword"]

        c1.execute("select * from usertable where emailid='%s' and pword='%s'"%(emailid,pword))
        if c1.rowcount>=1:
            row=c1.fetchone()
            session["emailid"]=emailid
            return render_template("userhome.html", msg="")
        else:
            return render_template("userlogin.html", msg="Your Login attempt was not successful. Please try again!!")

    return render_template("userlogin.html")

#User View Profile
@app.route("/userviewprofile")
def user_viewprofile():
    db=MySQLdb.connect("localhost","root","root","vqadb")
    c1 = db.cursor()
    emailid=session["emailid"]
    c1.execute("select * from usertable where emailid='%s'"%emailid)
    if c1!=None:
        row=c1.fetchone()
        return render_template("userviewprofile.html", data=row)


#User Search Image
@app.route("/usersearchimage1", methods=["GET","POST"])
def user_searchimage1():
    res=""
    db=MySQLdb.connect("localhost","root","root","vqadb")
    c1 = db.cursor()
    emailid=session["emailid"]
    if request.method == "POST":
        if request.form["b1"] == "Search":
            c1.execute("select ifnull(max(fid),100)+1 from imagetable")
            row = c1.fetchone()
            fid = int(row[0])
            f1 = request.files['imgfile']
            f1.save(os.getcwd() + "\\static\\uploadimage\\" + f1.filename)
            fname = f1.filename
            ptext=fname

            t = time.localtime()
            s = str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday)
            sdate = s
            session["r5"] = sdate
            c1.execute("insert into imagetable values('%d','%s','%s','%s','%s')" % (fid, emailid,fname,ptext,sdate))
            db.commit()

            s1 =str(t.tm_mday)+ "-" +  time.strftime("%b") + "-" +str(t.tm_year)



            subprocess.run("python  yolo.py  --image " + f1.filename)
        if request.form["b1"] == "Search from WebCam":
            c1.execute("select ifnull(max(fid),100)+1 from imagetable")
            row = c1.fetchone()
            fid = int(row[0])



            subprocess.run("python  yolo.py")

        if request.form["b1"] == "Result":
            c1.execute("select ifnull(max(fid),100) from imagetable")
            row = c1.fetchone()
            fid = int(row[0])
            f1 = request.files['imgfile']
            fname = f1.filename
            emailid=session["emailid"]
            t = time.localtime()
            s = str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday)
            sdate = s


            c1.execute("SELECT descr FROM imagedet order by id desc")
            row = c1.fetchone()

            res = chatbot_response(row[0])

            print("question: ", row[0])
            print("value is: ", res)
            c1.execute("insert into imagedet1 values('%s','%s','%s','%s','%s','%s')" % (res, fid, emailid, fname,'', sdate))
            db.commit()
            c1.execute("select descr,fid,emailid,fname,ptext,sdate from imagedet1 order by fid desc")
            row1 = c1.fetchone()
            r1=row1[0]
            r2=row1[1]
            r3 = row1[2]
            r4 = row1[3]
            r5 = row1[4]
            r6 = row1[5]

            return render_template("usersearchimage2.html", fid=r2, emailid=r3, fname=r4, ptext=r5,sdate=r6, res=res)

    return render_template("usersearchimage1.html")


# User Search Video
@app.route("/usersearchvideo1", methods=["GET", "POST"])
def user_searchvideo1():
    res=""
    db = MySQLdb.connect("localhost", "root", "root", "vqadb")
    c1 = db.cursor()
    emailid = session["emailid"]
    if request.method == "POST":
        if request.form["b1"] == "Search":
            c1.execute("select ifnull(max(fid),1000)+1 from videotable")
            row = c1.fetchone()
            fid = int(row[0])
            f1 = request.files['videofile']
            f1.save(os.getcwd() + "\\static\\uploadvideo\\" + f1.filename)
            fname = f1.filename
            ptext = fname

            t = time.localtime()
            s = str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday)
            sdate = s
            c1.execute("insert into videotable values('%d','%s','%s','%s','%s')" % (fid, emailid, fname, ptext, sdate))
            db.commit()

            s1 = str(t.tm_mday) + "-" + time.strftime("%b") + "-" + str(t.tm_year)



            c1.execute("insert into videodet1 values('%s','%s','%s','%s','%s','%s')" % (res, fid, emailid, fname, ptext, sdate))
            db.commit()
            subprocess.run("python yolo.py --video-path " + f1.filename)
        if request.form["b1"] == "Result":
            c1.execute("select descr,fid,emailid,fname,ptext,sdate from videodet1 order by fid desc")
            row1 = c1.fetchone()
            r1 = row1[0]
            r2 = row1[1]
            r3 = row1[2]
            r4 = row1[3]
            r5 = row1[4]
            r6 = row1[5]
            c1.execute("SELECT descr FROM videodet order by id desc")
            row = c1.fetchone()
            print(row[0])
            res = chatbot_response(row[0])
            return render_template("usersearchvideo2.html", fid=r2, emailid=r3, fname=r4, ptext=r5,sdate=r6, res=res)

    return render_template("usersearchvideo1.html")

# Admin View User Search Image
@app.route("/adminviewsearchimage")
def admin_viewsearchimage():
    db = MySQLdb.connect("localhost", "root", "root", "vqadb")
    c1 = db.cursor()
    c1.execute("select fid,emailid,fname,ptext,Date_Format(sdate,'%d-%b-%Y') from imagetable")
    data = c1.fetchall()
    return render_template("adminviewsearchimage.html", data=data)

# Admin View User Search Video
@app.route("/adminviewsearchvideo")
def admin_viewsearchvideo():
    db = MySQLdb.connect("localhost", "root", "root", "vqadb")
    c1 = db.cursor()
    c1.execute("select fid,emailid,fname,ptext,Date_Format(sdate,'%d-%b-%Y') from videotable")
    data = c1.fetchall()


    return render_template("adminviewsearchvideo.html", data=data)

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    print(str(ints)+" by sasi")

    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res



if __name__ == "__main__":
    app.run (debug=True)
