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
        

house = []
house1 = []
from .scrappers import downloadImage, extract, createNewDir, nextPage, convertToJson, \
    convertToPdf, getCorrectAnswerExplanation, getImageUrl, getNumber, getOptions, getQuestion, \
        cookSoup, getImageUrl1, extract1, nextPage1, convertToJson1, cookSoup1, writeToFile, \
            result, show_filters, show_filters1, downloadImage1, downloadpq, fetch_questions, \
            fetch_questions1, createNewDir1, convertToPdf1, fetch_me_soup, fetch_me_stew, eat_sweet_soup



@api_view(['GET','POST'])
def download_image_api(request):
    # Extract required data from request, if any
    # For example, if you're expecting the image URL as a parameter in the request
    
    img_url = request.data.get('imageUrl')  
    structure = request.data.get('structure')    
    num = request.data.get('number') 
    exam_type = request.data.get('type') 
    subject = request.data.get('subject')   
    exam_year = request.data.get('year')    
    # Call the downloadImage function
    try:
       downloadImage(img_url, structure, num, exam_type,subject,exam_year)  
       return Response({'message': 'Image downloaded successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs
 
    
@api_view(['GET','POST'])
def create_newdir_api(request):
    struct = request.data.get('struct')    
    num = request.data.get('num')   
    exam_type = request.data.get('type')   
    try:
        path = createNewDir(struct,num,exam_type)   
        return Response({'message': 'Directory created successfully', 'path': path}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs

@api_view(['GET','POST'])
def extract_data_api(request):
    soup = request.data.get('soup') 
    session = request.data.get('session') 
    try:
        result = extract(soup,session)
        return Response({'result': result}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)  # Return error response if any exception occurs

@api_view(['GET','POST'])
def next_page_api(request):
    try:
        # Extracting data from request
        soup = request.data.get('soup')       # Assuming soup is sent in the request body
        session = request.data.get('session') # Assuming session is sent in the request body

        # Calling nextPage function to process the data
        next_page = nextPage(soup, session)

        return Response({'next_page': next_page}, status=200)  # Returning the next page URL, adjust as needed
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET','POST'])
def convert_to_json_api(request):
    try:
        # Call the convertToJson function
        convertToJson()
        
        return Response({'message': 'Data converted to JSON successfully'}, status=200)
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
    try:
        # Extracting data from request
        item = request.data.get('item')  # Assuming 'item' data is sent in the request body
        num = request.data.get('num')    # Assuming 'num' data is sent in the request body

        # Calling getOptions function to retrieve options data
        options = getOptions(item, num)

        return Response({'options': options}, status=200)  # Returning the options data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_number_api(request):
    try:
        # Extracting data from request
        item = request.data.get('item')  # Assuming 'item' data is sent in the request body

        # Calling getNumber function to retrieve the number data
        number = getNumber(item)

        return Response({'number': number}, status=200)  # Returning the number data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_image_url_api(request):
    try:
        # Extracting data from request
        item = request.data.get('item')  # Assuming 'item' data is sent in the request body
        num = request.data.get('num')    # Assuming 'num' data is sent in the request body

        # Calling getImageUrl function to retrieve the image URL data
        image_url = getImageUrl(item, num)

        return Response({'image_url': image_url}, status=200)  # Returning the image URL data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_question_api(request):
    try:
        # Extracting data from request
        item = request.data.get('item')  # Assuming 'item' data is sent in the request body

        # Calling getQuestion function to retrieve the question data
        question = getQuestion(item)

        return Response({'question': question}, status=200)  # Returning the question data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_correct_answer_explanation_api(request):
    try:
        # Extracting data from request
        item = request.data.get('item')  # Assuming 'item' data is sent in the request body

        # Calling getCorrectAnswerExplanation function to retrieve the correct answer and explanation data
        answer, explanation = getCorrectAnswerExplanation(item)

        return Response({'correct_answer': answer, 'explanation': explanation}, status=200)  # Returning the correct answer and explanation data
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def cook_soup_api(request):
    try:
        # Extracting data from request
        url = request.data.get('url')  # Assuming 'url' data is sent in the request body
        session = HTMLSession()  # Create an HTMLSession object

        # Calling cookSoup function to retrieve the soup object
        soup, new_session = cookSoup(url, session)

        return Response({'soup': str(soup)}, status=200)  # Returning the soup object as a string
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