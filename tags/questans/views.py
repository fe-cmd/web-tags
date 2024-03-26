from logging import exception
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
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 

# Create your views here.
        

#house = []
#house1 = []
from .scrappers import downloadImage, extract, createNewDir, nextPage, convertToJson, \
    convertToPdf, getCorrectAnswerExplanation, getImageUrl, getNumber, getOptions, getQuestion, \
        cookSoup, getImageUrl1, extract1, nextPage1, convertToJson1, cookSoup1, writeToFile, \
            result, show_filters, show_filters1, downloadImage1, downloadpq, fetch_questions, \
            fetch_questions1, createNewDir1, convertToPdf1, fetch_me_soup, fetch_me_stew, eat_sweet_soup


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
    try:
        soup,newsession =cookSoup(url,session)
        result = extract(soup,session,house,structure,exam_type,subject,exam_year,subtype)
        print(result)
        return Response({'message': 'results extracted successfully', 'results':result}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
    
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
       result2 = nextPage(soup,session,house,structure,exam_type,subject,exam_year,subtype)
       print(result2)
       return Response({'message': 'next page results tapped successfully', 'results':result2}, status=200)
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
        result2 = nextPage(soup,session,house,structure,exam_type,subject,exam_year,subtype)
        # Call the convertToJson function
        converts = convertToJson(result2,exam_type,subject,exam_year)
        print(converts)
        return Response({'message': 'Data converted to JSON successfully', 'converts':converts}, status=200)
    
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
                       for item in options2:
                           quesopt.append(item["text"][1:200])   
                 print(quesopt)
      return Response({'message': 'options listed out successfully for your choice','options': quesopt}, status=200)  # Returning the options data
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
        
@api_view(['POST'])
def get_number_api(request):
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

        return Response({'message': 'numbers here successfully','number': nums}, status=200)  # Returning the number data
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
            imageurl = getImageUrl(item,num,structure,exam_type,subject,exam_year)
            print(imageurl)
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
                      imageurl = getImageUrl(item,num,structure,exam_type,subject,exam_year)
                      print(imageurl)  
      return Response({'message': 'Image url extracted successfully','resulturl': imageurl}, status=200)  # Returning the options data
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
            question = getQuestion(item)
            print(question)
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
                      question = getQuestion(item)
                      print(question) 
        return Response({'message': 'questions passed success!','question': question}, status=200)  # Returning the question data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

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
            answer, explanation = getCorrectAnswerExplanation(item)
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
                      answer, explanation = getCorrectAnswerExplanation(item)
                      print("the correct answer is {} and its explanation is {}.".format(answer, explanation ))
        return Response({'message': 'correct answer explanation success!'}, status=200)  # Returning the question data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

       
        return Response({'correct_answer': answer, 'explanation': explanation}, status=200)  # Returning the correct answer and explanation data
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
        soup,newsession =cookSoup(url,session)
        print(f'{soup} and also {session}')
        return Response({'message': 'soup prepared deliciously successfully!'}, status=200)  # Returning the soup object as a string
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

@api_view(['GET','POST'])
def download_image1_api(request):
    img_url = request.data.get('img_url')  
    struct = request.data.get('struct')    
    num = request.data.get('num')         
    # Call the downloadImage function
    try:
        downloadImage1(img_url, struct, num)  
        return Response({'message': 'Image downloaded successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs

@api_view(['GET','POST'])
def create_newdir1_api(request):
    struct = request.data.get('struct')    
    num = request.data.get('num')    
    try:
        path = createNewDir1(struct,num)   
        return Response({'message': 'Directory created successfully', 'path': path}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs

@api_view(['GET','POST'])
def extract1_data_api(request):
    soup = request.data.get('soup') 
    session = request.data.get('session') 
    try:
        result = extract1(soup,session)
        return Response({'result': result}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs

@api_view(['GET','POST'])
def next_page1_api(request):
    try:
        # Extracting data from request
        soup = request.data.get('soup')       # Assuming soup is sent in the request body
        session = request.data.get('session') # Assuming session is sent in the request body

        # Calling nextPage function to process the data
        next_page = nextPage1(soup, session)

        return Response({'next_page': next_page}, status=200)  # Returning the next page URL, adjust as needed
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET','POST'])
def convert_to_json1_api(request):
    try:
        # Call the convertToJson function
        convertToJson1()
        
        return Response({'message': 'Data converted to JSON successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET','POST'])
def convert_to_pdf1_api(request):
    try:
        # Call the convertToPdf function
        convertToPdf1()

        return Response({'message': 'Data converted to PDF successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)   
        
@api_view(['POST'])
def get_image_url1_api(request):
    try:
        # Extracting data from request
        soup = request.data.get('soup')   
        # Calling getImageUrl function to retrieve the image URL data
        image_url = getImageUrl1(soup)

        return Response({'image_url': image_url}, status=200)  # Returning the image URL data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def cook_soup1_api(request):
    try:
        # Extracting data from request
        url = request.data.get('url')  # Assuming 'url' data is sent in the request body
        session = HTMLSession()  # Create an HTMLSession object

        # Calling cookSoup function to retrieve the soup object
        soup, new_session = cookSoup1(url, session)

        return Response({'soup': str(soup)}, status=200)  # Returning the soup object as a string
    except Exception as e:
        return Response({'error': str(e)}, status=500)

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