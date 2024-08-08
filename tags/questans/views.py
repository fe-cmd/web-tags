from logging import exception
import logging
import bs4
from requests_html import HTMLSession
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from reportlab.pdfgen import canvas
import json
import requests
from os.path  import basename
import os
from django.shortcuts import render, redirect
import argparse
from django.contrib import messages
from django.db import connection
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 
from  questans.database import questions_collection
from requests.exceptions import RequestException, InvalidSchema
logger = logging.getLogger(__name__)


# Create your views here.
        

#house = []
#house1 = []
from .scrappers import downloadImage, extract, createNewDir, nextPage, convertToJson, \
    convertToPdf, getCorrectAnswerExplanation, getImageUrl, getNumber, getOptions, getQuestion, \
        cookSoup,  writeToFile, getTheoryQuestion, \
        result, show_filters, show_filters1, convertToJsonT,\
        downloadpq, fetch_questions,fetch_questions1, createNewDir1, convertToPdf1, \
        fetch_me_soup, fetch_me_stew, eat_sweet_soup,upload_json_to_api

#API engineered endpoints for website myschool.ng
def get_param1(request):
    subtype = request.data.get('subtype')
    structure = request.data.get('structure')    
    num = request.data.get('number') 
    exam_type = request.data.get('type') 
    subject = request.data.get('subject')   
    exam_year = request.data.get('year') 
    house = request.data.get('house')
    return structure,num,exam_type,subject,exam_year,subtype,house

@api_view(['GET','POST'])
def download_image_api(request):
    # Extract required data from request, if any
    # For example, if you're expecting the image URL as a parameter in the request
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)
    img_url = request.data.get('imageUrl')     
    # Call the downloadImage function
    try:
       downloadImage(img_url, structure, num, exam_type,subject,exam_year)  
       return Response({'message': 'Image downloaded successfully'}, status=201)     
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
  
@api_view(['GET','POST'])
def create_newdir_api(request):
    struct,num,exam_type,subject,exam_year,subtype,house = get_param1(request)
    try:
       path = createNewDir(struct,num,exam_type,subject,exam_year)   
       print("Path:",path)
       return Response({'message': 'Directory created successfully', 'path': path}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
   
@api_view(['GET','POST'])
def extract_data_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup,newsession =cookSoup(url,session)
    if(soup != None and session != None):
        results = soup.find_all("div",class_="media question-item mb-4")
        questext = []
        correctAns = []
        quesopt = []
        form = []
        subt = []
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
                imageUrl = getImageUrl(item,number,structure,exam_type,subject,exam_year)
                question_details["imageUrl"] = imageUrl
                options = getOptions(item,structure,number,exam_type,subject,exam_year)
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
        if(soup != None and session != None):   
            results2 = soup.find("ul",class_= "pagination flex-wrap")
            links = results2.find_all("a")
            nextPage = None
            #for x in range(1,7):
            if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    results1 = next.find_all("div",class_="media question-item mb-4")
                    for item in results1:
                       question_details = {}
                       correctAnswer,explanation = getCorrectAnswerExplanation(item)
                       question_details["correctOption"] = correctAnswer
                       correctAns.append(question_details["correctOption"])
                       question_details["explanation"] = {"text":explanation}
                       question_Text = getQuestion(item)
                       question_details["text"] = question_Text
                       questext.append(question_details["text"])
                       question_details["structure"] = structure
                       form.append(question_details["structure"])
                       number = getNumber(item)
                       question_details["number"] = int(number) 
                       figures = int(number)
                       imageUrl = getImageUrl(item,structure,number,exam_type,subject,exam_year)
                       question_details["imageUrl"] = imageUrl
                       options = getOptions(item,structure,number,exam_type,subject,exam_year)
                       question_details["options"] = options
                       for item in question_details["options"]:
                           quesopt.append(item["text"][1:200])                       
                       if exam_type == "WAEC":
                           question_details["subType"] = subtype
                           subt.append(question_details["subType"])
                       else:
                            question_details["subType"] = subtype
                            subt.append(question_details["subType"])
                       question_details["subject"] = subject
                       question_details["type"] = exam_type
                       question_details["year"] = exam_year
                       print(question_details)
                       house.append(question_details)
                       #num = len(house)
                       print("\n\n")
                       print(house)
                       #return house                     
        json_file_path = convertToJson(house, exam_type, subject, exam_year, structure)
        if json_file_path:  # Check if the file path is valid
            print("End of site reached, thank you for tiffing questions")
            response = upload_json_to_api(json_file_path, 'https://afternoonprep-tagging.onrender.com/objective')
            print(response)
        else:
            print("Error: JSON file path is invalid.")
   
    return Response({'message': 'results extracted successfully', 'results':house}, status=200)


  
@api_view(['GET', 'POST'])
def extract_theory_data_api(request):
    session = HTMLSession()
    structure, num, exam_type, subject, exam_year, subtype, house = get_param1(request)
    if structure == "OBJECTIVE":
        url_Struc = "obj"
    elif structure == "THEORY":
        url_Struc = "theory"
    additional_url = subject.lower().replace(" ", "-") + "?exam_type=" + exam_type.lower() + "&exam_year=" + str(exam_year) + "&type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup, newsession = cookSoup(url, session)
    if soup is not None and session is not None:
        results = soup.find_all("div", class_="media question-item mb-4")
        for item in results:
            question_details = {}
            answerLink = item.find("a")
            base_url = answerLink['href']
            newsession = HTMLSession()
            newsoup, newSession = cookSoup(base_url, newsession)
            if newsoup is not None and newsession is not None:
                result = newsoup.select("div[class='mb-4']")
                explanations = []
                for element in result:
                    if element.find("img"):
                        image_new = element.find("img")['src']
                        explanations.append({"imageUrl": image_new})
                    else:
                        explanations.append({"imageUrl": None})
                    for val in element.find_all("p"):
                        explanation = val.text.strip()
                        if val.find("img"):
                            image_src = val.find("img")['src']
                            explanations.append({"explanation": explanation, "imageUrl": image_src})
                        else:
                            explanations.append({"explanation": explanation, "imageUrl": None})
                question_details["correct explanation"] = {"text": explanations}
                question_Text = getTheoryQuestion(item)
                question_details["text"] = question_Text
                question_details["structure"] = structure
                number = getNumber(item)
                question_details["number"] = int(number)
                imageUrl = getImageUrl(item, number, structure, exam_type, subject, exam_year)
                question_details["imageUrl"] = imageUrl
                options = getOptions(item, structure, number, exam_type, subject, exam_year)
                question_details["options"] = options
                question_details["subType"] = subtype
                question_details["subject"] = subject
                question_details["type"] = exam_type
                question_details["year"] = exam_year
                house.append(question_details)
                print(house)

        results2 = soup.find("ul", class_="pagination flex-wrap")
        if results2:
            links = results2.find_all("a")
            if links and links[-1].text.lower().strip() == "»":
                for x in range(1, len(links)):
                    nextPage = links[x]["href"]
                    next, newSession1 = cookSoup(nextPage, session)
                    if next is not None and newSession1 is not None:
                        results1 = next.find_all("div", class_="media question-item mb-4")
                        for item in results1:
                            question_details = {}
                            answerLink = item.find("a")
                            newsession1 = HTMLSession()
                            base_url = answerLink['href']
                            newsoup1, newSession = cookSoup(base_url, newsession1)
                            if newsoup1 is not None and newsession1 is not None:
                                result = newsoup1.select("div[class='mb-4']")
                                explanations = []
                                for element in result:
                                    if element.find("img"):
                                        image_new = element.find("img")['src']
                                        explanations.append({"imageUrl": image_new})
                                    else:
                                        explanations.append({"imageUrl": None})
                                    for val in element.find_all("p"):
                                        explanation = val.text.strip()
                                        if val.find("img"):
                                            image_src = val.find("img")['src']
                                            explanations.append({"explanation": explanation, "imageUrl": image_src})
                                        else:
                                            explanations.append({"explanation": explanation, "imageUrl": None})
                                question_details["correct explanation"] = {"text": explanations}
                                question_Text = getTheoryQuestion(item)
                                question_details["text"] = question_Text
                                number = getNumber(item)
                                question_details["number"] = int(number)
                                imageUrl = getImageUrl(item, structure, number, exam_type, subject, exam_year)
                                question_details["imageUrl"] = imageUrl
                                options = getOptions(item, structure, number, exam_type, subject, exam_year)
                                question_details["options"] = options
                                question_details["subType"] = subtype
                                question_details["subject"] = subject
                                question_details["type"] = exam_type
                                question_details["year"] = exam_year
                                house.append(question_details)
                                print(house)

        json_file_path = convertToJsonT(house, exam_type, subject, exam_year, structure)
        if json_file_path:
            print(f"JSON file saved successfully at {json_file_path}, End of site reached, thank you for tiffing questions" )
            response = upload_json_to_api(json_file_path, 'https://afternoonprep-tagging.onrender.com/objective')
            print(response)
        else:
            print("Error: JSON file path is invalid.")

    return Response({'message': 'results extracted successfully', 'results': house}, status=200)

@api_view(['GET','POST'])
def next_page_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    try:
       soup,newsession1 =cookSoup(url,session)
       if(soup != None and session != None): 
            questext = []
            correctAns = []
            quesopt = []
            form = []
            subt = []  
            results2 = soup.find("ul",class_= "pagination flex-wrap")
            links = results2.find_all("a")
            nextPage = None
            #for x in range(1,7):
            if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    results1 = next.find_all("div",class_="media question-item mb-4")
                    for item in results1:
                       question_details = {}
                       correctAnswer,explanation = getCorrectAnswerExplanation(item)
                       question_details["correctOption"] = correctAnswer
                       correctAns.append(question_details["correctOption"])
                       question_details["explanation"] = {"text":explanation}
                       question_Text = getQuestion(item)
                       question_details["text"] = question_Text
                       questext.append(question_details["text"])
                       question_details["structure"] = structure
                       form.append(question_details["structure"])
                       number = getNumber(item)
                       question_details["number"] = int(number) 
                       figures = int(number)
                       imageUrl = getImageUrl(item,structure,number,exam_type,subject,exam_year)
                       question_details["imageUrl"] = imageUrl
                       options = getOptions(item,structure,number,exam_type,subject,exam_year)
                       question_details["options"] = options
                       for item in question_details["options"]:
                           quesopt.append(item["text"][1:200])                       
                       if exam_type == "WAEC":
                           question_details["subType"] = subtype
                           subt.append(question_details["subType"])
                       else:
                            question_details["subType"] = subtype
                            subt.append(question_details["subType"])
                       question_details["subject"] = subject
                       question_details["type"] = exam_type
                       question_details["year"] = exam_year
                       print(question_details)
                       house.append(question_details)
                       #num = len(house)
                       print("\n\n")
                       print(house)
                       #return house                     
            else:
                convertToJson(house,exam_type,subject,exam_year)
                print("End of site reached,thank you for tiffing questions")
       return Response({'message': 'next page results tapped successfully', 'results':house}, status=200)
    except Exception as e:
       return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
        
@api_view(['GET','POST'])
def next_pagetheory_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    try:
       soup,newsession1 =cookSoup(url,session)
       if(soup != None and session != None): 
            questext = []
            correctAns = []
            quesopt = []
            form = []
            subt = []  
            results2 = soup.find("ul",class_= "pagination flex-wrap")
            links = results2.find_all("a")
            nextPage = None
            #for x in range(1,7):
            if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    results1 = next.find_all("div",class_="media question-item mb-4")
                    for item in results1:
                       question_details = {}
                       answerLink = item.find("a")
                       base_url = answerLink['href']
                       newsession = HTMLSession()
                       newsoup, newSession = cookSoup(base_url, newsession)
                       if newsoup is not None and newsession is not None:
                           result =newsoup.select("div[class='mb-4']")
                           explanations = []
                           for element in result:
                             if element.find("img"):
                               image_new = element.find("img")['src']
                               explanations.append({"imageUrl": image_new})
                             else:
                               explanations.append({"imageUrl": None})
                             for val in element.find_all("p"):
                               explanation = val.text.strip() 
                               if val.find("img"):
                                  image_src = val.find("img")['src']  # Extract the src attribute of the img tag
                                  explanations.append({"explanation": explanation, "imageUrl": image_src})  # Append image URL with explanation
                               else:
                                  explanations.append({"explanation": explanation, "imageUrl": None})  # Use default image URL if no image found in paragraph
                       question_details["correct explanation"] = {"text":explanations}
                       question_Text = getTheoryQuestion(item)
                       question_details["text"] = question_Text
                       questext.append(question_details["text"])
                       question_details["structure"] = structure
                       form.append(question_details["structure"])
                       number = getNumber(item)
                       question_details["number"] = int(number) 
                       figures = int(number)
                       imageUrl = getImageUrl(item,structure,number,exam_type,subject,exam_year)
                       question_details["imageUrl"] = imageUrl
                       options = getOptions(item,structure,number,exam_type,subject,exam_year)
                       question_details["options"] = options
                       for item in question_details["options"]:
                           quesopt.append(item["text"][1:200])                       
                       if exam_type == "WAEC":
                           question_details["subType"] = subtype
                           subt.append(question_details["subType"])
                       else:
                            question_details["subType"] = subtype
                            subt.append(question_details["subType"])
                       question_details["subject"] = subject
                       question_details["type"] = exam_type
                       question_details["year"] = exam_year
                       print(question_details)
                       house.append(question_details)
                       #num = len(house)
                       print("\n\n")
                       print(house)
                       #return house                     
            else:
                convertToJson(house,exam_type,subject,exam_year)
                print("End of site reached,thank you for tiffing questions")
       return Response({'message': 'next page results tapped successfully', 'results':house}, status=200)
    except Exception as e:
       return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
        
@api_view(['GET','POST'])
def convert_to_json_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    try:
        soup,newsession1 =cookSoup(url,session)
        if(soup != None and session != None): 
            questext = []
            correctAns = []
            quesopt = []
            form = []
            subt = []  
            results2 = soup.find("ul",class_= "pagination flex-wrap")
            links = results2.find_all("a")
            nextPage = None
            #for x in range(1,7):
            if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    results1 = next.find_all("div",class_="media question-item mb-4")
                    for item in results1:
                       question_details = {}
                       correctAnswer,explanation = getCorrectAnswerExplanation(item)
                       question_details["correctOption"] = correctAnswer
                       correctAns.append(question_details["correctOption"])
                       question_details["explanation"] = {"text":explanation}
                       question_Text = getQuestion(item)
                       question_details["text"] = question_Text
                       questext.append(question_details["text"])
                       question_details["structure"] = structure
                       form.append(question_details["structure"])
                       number = getNumber(item)
                       question_details["number"] = int(number) 
                       figures = int(number)
                       imageUrl = getImageUrl(item,structure,number,exam_type,subject,exam_year)
                       question_details["imageUrl"] = imageUrl
                       options = getOptions(item,structure,number,exam_type,subject,exam_year)
                       question_details["options"] = options
                       for item in question_details["options"]:
                           quesopt.append(item["text"][1:200])                       
                       if exam_type == "WAEC":
                           question_details["subType"] = subtype
                           subt.append(question_details["subType"])
                       else:
                            question_details["subType"] = subtype
                            subt.append(question_details["subType"])
                       question_details["subject"] = subject
                       question_details["type"] = exam_type
                       question_details["year"] = exam_year
                       print(question_details)
                       house.append(question_details)
                       #num = len(house)
                       print("\n\n")
                       print(house)
                       #return house                     
            else:
                convertToJson(house,exam_type,subject,exam_year)
                print("End of site reached,thank you for tiffing questions")
        
        # Call the convertToJson function
        
        return Response({'message': 'Data converted to JSON successfully', 'Json formats for results': convertToJson(house,exam_type,subject,exam_year)}, status=200)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET','POST'])
def convert_to_pdf_api(request):
    try:
        # Call the convertToPdf function
        convertToPdf()

        return Response({'message': 'Data converted to PDF successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)   
    
@api_view(['POST'])
def get_options_api(request):
    quesopt = []
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup,newsession1 =cookSoup(url,session)
    try:
      if(soup != None and session != None):
        res = soup.find_all("div",class_="media question-item mb-4")
        for item in res:
            # Calling getOptions function to retrieve options data
            options = getOptions(item,structure,num,exam_type,subject,exam_year)
            quesopt.append(options)
        print(quesopt)
        if(soup != None and session != None):   
               res2 = soup.find("ul",class_= "pagination flex-wrap")
               links = res2.find_all("a")
               nextPage = None
               #for x in range(1,7):
               if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    res1 = next.find_all("div",class_="media question-item mb-4")
                    for item in res1:
                       options2 = getOptions(item,structure,num,exam_type,subject,exam_year)
                       quesopt.append(options2)   
                 print(quesopt)
      return Response({'message': 'options listed out successfully for your choice','options': quesopt}, status=200)  # Returning the options data
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
        
@api_view(['POST'])
def get_number_api(request):
    numbers = []
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup,newsession1 =cookSoup(url,session)
    try:
      if(soup != None and session != None):
        res = soup.find_all("div",class_="media question-item mb-4")
        for item in res:
            number = getNumber(item)
            nums = int(number)
            print(nums)
            numbers.append(nums)
        if(soup != None and session != None):   
               res2 = soup.find("ul",class_= "pagination flex-wrap")
               links = res2.find_all("a")
               nextPage = None
               #for x in range(1,7):
               if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    res1 = next.find_all("div",class_="media question-item mb-4")
                    for item in res1:
                        number = getNumber(item)
                        nums = int(number)
                        print(nums)
                        numbers.append(nums)

        return Response({'message': 'numbers here successfully','List of numbers for this year of questions': numbers}, status=200)  # Returning the number data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_image_url_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup,newsession1 =cookSoup(url,session)
    try:
      if(soup != None and session != None):
        res = soup.find_all("div",class_="media question-item mb-4")
        for item in res:
            question_details = {}
            imageurl = getImageUrl(item,num,structure,exam_type,subject,exam_year)
            question_details["imageUrl"] = imageurl
            house.append(question_details)
            print(house)
        if(soup != None and session != None):   
               res2 = soup.find("ul",class_= "pagination flex-wrap")
               links = res2.find_all("a")
               nextPage = None
               #for x in range(1,7):
               if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    res1 = next.find_all("div",class_="media question-item mb-4")
                    for item in res1:
                       question_details = {}
                       imageurl = getImageUrl(item,num,structure,exam_type,subject,exam_year)
                       question_details["imageUrl"] = imageurl
                       house.append(question_details)
                       print(house)  
      return Response({'message': 'Image url extracted successfully','resulturl': house}, status=200)  # Returning the options data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_question_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup,newsession1 =cookSoup(url,session)
    try:
      if(soup != None and session != None):
        res = soup.find_all("div",class_="media question-item mb-4")
        for item in res:
            question_details = {}
            question = getQuestion(item)
            question_details["text"] = question
            house.append(question_details)
            print(house)
        if(soup != None and session != None):   
               res2 = soup.find("ul",class_= "pagination flex-wrap")
               links = res2.find_all("a")
               nextPage = None
               #for x in range(1,7):
               if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    res1 = next.find_all("div",class_="media question-item mb-4")
                    for item in res1:
                      question_details = {}
                      question = getQuestion(item)
                      question_details["text"] = question
                      house.append(question_details)
                      print(house)
        return Response({'message': 'questions passed success!','question': house}, status=200)  # Returning the question data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_questiontheory_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup,newsession1 =cookSoup(url,session)
    
    if(soup != None and session != None):
        res = soup.find_all("div",class_="media question-item mb-4")
        for item in res:
            question_details = {}
            question = getTheoryQuestion(item)
            question_details["text"] = question
            house.append(question_details)
            print(house)
        if(soup != None and session != None):   
               res2 = soup.find("ul",class_= "pagination flex-wrap")
               links = res2.find_all("a")
               nextPage = None
               #for x in range(1,7):
               if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    res1 = next.find_all("div",class_="media question-item mb-4")
                    for item in res1:
                      question_details = {}
                      question = getTheoryQuestion(item)
                      question_details["text"] = question
                      house.append(question_details)
                      print(house)
    return Response({'message': 'questions passed success!','question': house}, status=200)  # Returning the question data
    
@api_view(['POST'])
def get_correct_answer_explanation_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)    
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup,newsession1 =cookSoup(url,session)
    try:
      if(soup != None and session != None):
        res = soup.find_all("div",class_="media question-item mb-4")
        for item in res:
            question_details = {}
            answer, explanation = getCorrectAnswerExplanation(item)
            question_details["correctOption"] = answer
            question_details["explanation"] = {"text":explanation}
            house.append(question_details)
            print("the correct answer is {} and its explanation is {}.".format(answer, explanation ))
        if(soup != None and session != None):   
               res2 = soup.find("ul",class_= "pagination flex-wrap")
               links = res2.find_all("a")
               nextPage = None
               #for x in range(1,7):
               if links[-1].text.lower().strip() == "»":
                 for x in range(1,len(links)):
                  nextPage = links[x]["href"]
                  next,newSession1 = cookSoup(nextPage,session)
                  if(next != None and session != None):
                    res1 = next.find_all("div",class_="media question-item mb-4")
                    for item in res1:
                        question_details = {}
                        answer, explanation = getCorrectAnswerExplanation(item)
                        question_details["correctOption"] = answer
                        question_details["explanation"] = {"text":explanation}
                        house.append(question_details)  
                        print("the correct answer is {} and its explanation is {}.".format(answer, explanation ))
        return Response({'message': 'correct answer explanation success!', 'correct answer & Explanation': house}, status=200)  # Returning the question data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def cook_soup_api(request):
    session = HTMLSession()
    structure,num,exam_type,subject,exam_year,subtype,house = get_param1(request)
    if structure == "OBJECTIVE":
            url_Struc = "obj"
    elif structure == "THEORY":
            url_Struc = "theory"
    additional_url = subject.lower().replace(" ","-") + "?exam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    try:
        resp = session.get(url)
        if(url != "" and session != ""):
            html = resp.html.html
            soup = bs4.BeautifulSoup(html, "html.parser")
            extracted_data = resp.html.text
            extracted_text = soup.get_text()
        print(f'{soup} and also {session}')
        return Response({'message': 'soup prepared deliciously successfully!',  'soup':extracted_text, 'session':extracted_data}, status=200)  # Returning the soup object as a string
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def write_to_file_api(request):
    try:
        # Extracting data from request
        text = request.data.get('text')  # Assuming 'text' data is sent in the request body

        # Calling writeToFile function to write the text to a file
        writeToFile(text)

        return Response({'message': 'Text written to file successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


#API engineered endpoints for website nigerianscholars.com

@api_view(['GET','POST'])
def fetch_me_stew_api(request):
    try:
        result = fetch_me_stew()
        
        return Response({'result': result}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET','POST'])
def fetch_me_soup_api(request):
    try:
        result = fetch_me_soup()
        
        return Response({'result': result}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET','POST'])
def eat_sweet_soup_api(request):
    try:
        eat_sweet_soup()
        
        return Response({'message': 'Soup downloaded and eaten good successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET','POST'])
def result_home_api(request):
    try:
        result()
        return Response({'message': 'results gotten o'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)