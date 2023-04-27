from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
print('Imported Successfully!')
word_vectors = KeyedVectors.load_word2vec_format(r"C:\Users\mihir\Downloads\GoogleNews-vectors-negative300.bin.gz", binary=True)
print('Succesful')

import sys
import os
import math
import random
import smtplib

papers=[
    {
        "head_line":"Reduced cardiovascular reserve capacity in long-term allogeneic stem cell transplant survivors",
        "link":"https://www.nature.com/articles/s41598-023-28320-w",
        "speciality":"Cardiologist",
        "sub_speciality" : "Transplant",
        "tags":["survivors","allogenic","stem"]
    },
     {
        "head_line":"Mitochondrial transplantation improves rat recovery from cardiac arrest",
        "link":"https://medicalxpress.com/news/2023-03-mitochondrial-transplantation-rat-recovery-cardiac.html",
         "speciality":"Cardiologist",
         "sub_speciality" : "Transplant",
        "tags":["mitochondrial","cell","rat"]
    },
     {
        "head_line":"A new therapeutic target for the prevention of heart failure due to aortic stenosis",
        "link":"https://www.medicalnewstoday.com/articles/a-new-therapeutic-target-for-the-prevention-of-heart-failure-due-to-aortic-stenosis",
        "speciality":"Cardiologist",
         "sub_speciality" : "Preventive",
         "tags":["aortic","adrenergic","stenosis"]
    },
     {
        "head_line":"Cardiovascular disease: Can eating 1-3 eggs per week help protect the heart?",
        "link":"https://www.medicalnewstoday.com/articles/cardiovascular-disease-eating-eggs-weekly-lower-risk",
        "speciality":"Cardiologist",
         "sub_speciality" : "Preventive",
         "tags":["consumption","risk","eggs"]
    },
     {
        "head_line":"Common Problems In Pediatric Gynecology",
        "link":"https://www.sciencedirect.com/science/article/abs/pii/S0094014321010260",
         "speciality" : "Gynac",
         "sub_speciality" : "Pediatric",
        "tags":["physiology","pertinent","infection"]
    },
     {
        "head_line":"Ultrasonography in pediatric gynecology and obstetrics",
        "link":"https://www.ajronline.org/doi/abs/10.2214/ajr.128.3.423",
         "speciality" : "Gynac",
         "sub_speciality" : "Pediatric",
        "tags":["pregnancy","sonogram","Ultrasonography"]
    }   
]
reg=[16701,16702,16703]    

data=[
	{
		"reg_id" : 16701,
		"fname" : "Mihir",
		"lname" : "Chopdekar",
		"speciality" : "Cardiologist",
		"sub_speciality" : "Transplant",
		"email" : "mihirchopdekar00@gmail.com"
	},
	{
		"reg_id" : 16702,
		"fname" : "Nishant",
		"lname" : "Ambre",
		"speciality" : "Gynac",
		"sub_speciality" : "Pediatric",
		"email" : "nishantambre1999@gmail.com"
	},
	{
		"reg_id" : 16703,
		"fname" : "Sumedh",
		"lname" : "Dhotre",
		"speciality" : "Cardiologist",
		"sub_speciality" : "Preventive",
		"email" : "mihirchopdekar00@gmail.com"
	}
]

def suggest_papers(dict):
    y=dict["reg_id"]
    for i in data:
        if i["reg_id"]==y:
            spec=i["speciality"]
            sub_spec=i["sub_speciality"]
    ret_papers={'l1':"",'l2':"",'l3':""}
    i=1
    for j in papers:
        if j["speciality"]==spec and j["sub_speciality"]==sub_spec:
            pon="l"+str(i)
            di={'headline':j['head_line'],'link':j["link"]}
            ret_papers[pon]=di
            i=i+1
             
             
    return ret_papers
 
def ret_id(dict):
    y=dict["reg_id"]
    print(y)
    if y in reg:
        for i in data:
            if i["reg_id"]==y:
                d=i.copy()
        digits="0123456789"
        OTP=""
        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        otp = "Your DocBOT OTP is "+ OTP 
        OTP=int(OTP)
        msg= otp
        email=d["email"]
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("mihirchopdekar00@gmail.com", "sveucklqxylefyod")
        s.sendmail('mihirchopdekar00@gmail.com',email,msg)
        a={"exists":True,"otp":OTP}
        d.update(a)
        return d
    else:
        a={"exists":False}
        return a
    
def ret_paper(dict):
    y=dict["reg_id"]
    for i in data:
            if i["reg_id"]==y:
                d=i.copy()
    #y=str(dict["reg_id"])
    z=d["speciality"]
    z1=d["sub_speciality"]
    return papers[z][z1]
    
def ret_searched_paper(dict):
    word=dict["word"]
    a=word_vectors[word]
    threshold=30
    l=[]
    for i in papers:
        max=[0,0]
        for j in i["tags"]:
            b=word_vectors[j]
            cos=round(float(cosine_similarity([a],[b])*100),2)
            if cos>max[0]:
                max=[cos,j]
        l.append(max)
    l=(sorted(l, key=lambda x:x[0], reverse=True))
    a=l[0:3]
    b = [el[1] for el in a if el[0]>threshold]
    
    x={"l1":"","l2":"","l3":""}
    k=1
    for i in papers:
        for j in i["tags"]:
            if j in b and k<4:
                temp='l'+str(k)
                di={'headline':i['head_line'],'link':i["link"]}
                x[temp]=di
                k+=1
    
    if len(x)==0:
        #print("No matches found")
        pass
    else: 
        #print(x)
        return x
    
def main1(dict):
    
    if dict["type"]=="id":
        result=ret_id(dict)
    elif dict["type"]=="suggest":
        result=suggest_papers(dict)
    elif dict['type']=='search':
        result=ret_searched_paper(dict)
    else:
        result=ret_paper(dict)

    #ans={"message":result}
    #print(ans)
    return {"message":result}
     #return {"message":dict}

from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods= ["POST", "GET"])
def webhook() :
    # if request.method == "GET":
    #     return "Hello YouTube! - Not connected to DF"
    if request.method == "POST":
        payload = request.json
        a=main1(payload)
        return a
    else:
        print (request.data)
        return "200"

if __name__=='__main__':
    app.run(debug=True)

