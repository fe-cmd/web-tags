from logging import exception
import bs4
from requests_html import HTMLSession
import json
import requests
from os.path  import basename
import os
from django.shortcuts import render, redirect
import argparse
from django.contrib import messages

# Create your views here.
        

house = []
def downloadImage(imgUrl,struct,num):
    try:
        path = createNewDir(struct,num)
        
        with open(os.path.join(path,basename(imgUrl)), "wb") as f:
            
            f.write(requests.get(imgUrl).content)
    except OSError as e:
        print(e.message,e.args)
        
def createNewDir(struct,num):
    try:
        path = os.path.join(exam_type,subject,structure,str(exam_year),str(num))
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    except exception as e:
        print(e.message,e.args)

def extract(soup,session):
    try:    
        if(soup != None and session != None):
            results = soup.find_all("div",class_="media question-item mb-4")
            for item in results:
                question_details = {}
                correctAnswer,explanation = getCorrectAnswerExplanation(item)
                question_details["correctOption"] = correctAnswer
                question_details["explanation"] = {"text":explanation}
                question_Text = getQuestion(item)
                question_details["text"] = question_Text
                question_details["structure"] = structure
                number = getNumber(item)
                question_details["number"] = int(number)
                imageUrl = getImageUrl(item,number)
                question_details["imageUrl"] = imageUrl
                options = getOptions(item,number)
                question_details["options"] = options
                if exam_type == "WAEC":
                    question_details["subType"] = subtype
                else:
                     question_details["subType"] = subtype
                question_details["subject"] = subject
                question_details["type"] = exam_type
                question_details["year"] = exam_year
                print(question_details)
                house.append(question_details)
                print("\n\n")
                print(house)
                #return house
            nap = nextPage(soup,session)
            if nap != None:
              return nap
           
            
    except exception as e:
        print(e.message,e.args)

def nextPage(soup,session):
    if(soup != "" and session != ""):
        results = soup.find("ul",class_= "pagination flex-wrap")
        
        links = results.find_all("a")
        nextPage = None
        if links[-1].text.lower().strip() == "»":
            nextPage = links[-1]["href"]
            next,newSession = cookSoup(nextPage,session)
            extract(next,session)
        else:
             convertToJson(house)
             print("End of site reached,thank you for tiffing questions")
    else:
       
        print("Soup burnt or session expired")

def convertToJson(data):
     filename = "output_" + exam_type + "_" + str(exam_year) + "_"  + subject + ".json"
     with open(filename, 'a') as outfile:
            json.dump(data, outfile,indent=2)
     house.clear()
            
def getOptions(item,num):
    try:
        options = []
        result = item.find("ul",class_="list-unstyled")
        optionsResult = result.find_all("li")
        for val in optionsResult:
            option = {}
            option["option"] = val.find("strong").text.replace(".","").strip()
            option["text"] = val.text.strip()[2:]
            #option_image = val.find("img")
            image_url = getImageUrl(item,num)
            if image_url != None:
                option["imageUrl"] = image_url
                #downloadImage(image_url,question_details["structure"],question_details["number"])
            else:
                option["imageUrl"] = None
            options.append(option)
        return options
    except exception as e:
        print(e.message,e.args)

def getNumber(item):
    try:
        result = item.find("div",class_="question_sn bg-danger mr-3")
        number = result.text.strip()
        return number
    except exception as e:
        print(e.message,e.args)
        
def getImageUrl(item,num):
    image = item.find("img")
    if not image == None :
        url =image["src"]
        downloadImage(url,structure,num)
        return url
    else:
        return None


def getQuestion(item):
    try:
        result = item.find("div",class_="question-desc mt-0 mb-3")
        question = result.find("p")
        if(question):
            text = question.text.replace('"',"").strip() 
        else:
            text = result.text.replace('"',"").strip() 
        return text
    except exception as e:
        print(e.message,e.args)
        
def getCorrectAnswerExplanation(item):
    try:
        if(item != None):
            answerLink = item.find("a")
            session = HTMLSession()
            base_url = answerLink['href']
            soup,newSession = cookSoup(base_url,session)
            if(soup != None and session != None):
                result =soup.select("div[class='mb-4']")
                answerResult = result[1].find("h5",class_="text-success mb-3")
                explationResult = result[1].text
                if not answerResult:
                    answerResult = result[0].find("h5",class_="text-success mb-3")
                    explationResult = result[0].text
                answer = answerResult.text.replace("Correct Answer: Option ","").strip()
                explanation = explationResult[explationResult.index("Explanation"):].strip()
                if explanation != None:
                    return answer,explanation
                else:
                    return answer,None
    except exception as e:
        print(e.message,e.args)
    
def cookSoup(url,session):
    try:
        resp = session.get(url)
        if(url != "" and session != ""):
            html = resp.html.html
            soup = bs4.BeautifulSoup(html, "html.parser")
            return soup,session
        else:
            print("Soup burnt or session expired")
    except exception as e :
        print(e.message,e.args)




   
def result(request):
    global subject, exam_type, structure, exam_year, subtype
    print()
    subject = "BIOLOGY"
    exam_type = "JAMB"
    structure = "OBJECTIVE"
    if structure == "OBJECTIVE":
        url_Struc = "obj"
    subtype = None
    exam_year = 2020
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    session = HTMLSession()
    base_url = "https://myschool.ng/classroom/" + additional_url
    soup,newSession = cookSoup(base_url,session)
    tran = extract(soup,newSession)
    return render(request, 'questans/home.html', {'tran':tran})

#def share_questions(subject, exam_type, structure, exam_year, subtype):
    
def show_filters(request):
    return render(request, 'questans/filters.html')





    
# Correct Answer: Option B
# Correct Answer: Option 



