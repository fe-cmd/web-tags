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
logger = logging.getLogger(__name__)
import requests_html

# Create your views here.
from questans.scrappers import  cookSoup1, getImageUrl1, convertToJson1,  getOptions1, \
getCorrectAnswer, getQuestion1, convertToJson1

def get_param(request):
    subject = request.data.get('subject')       
    topic = request.data.get('topic')
    house = request.data.get('house')
    return subject, house, topic

@csrf_exempt
@api_view(['GET','POST'])
def extract1_data_api(request):
    logger.info(f"Request content type: {request.content_type}")

    if request.content_type != 'application/json':
        return Response({'error': 'Invalid content type. Expected application/json.'}, status=400)

    try:
        subject, house, topic = get_param(request)
        additional_url = subject.lower().replace(" ", "-") + "/" + topic + "/review/quiz/"
        url = "https://www.sparknotes.com/" + additional_url

        session = requests_html.HTMLSession()
        soup, session = cookSoup1(url, session)
        if soup:
            results = soup.find_all("div", class_="quick-quiz-question")
            if results:
                for item in results:
                    question_details = {}
                    correctAnswer = getCorrectAnswer(item)
                    question_details["correctOption"] = correctAnswer
                    question_Text = getQuestion1(item)
                    question_details["text"] = question_Text
                    imageUrl = getImageUrl1(item, subject)
                    question_details["imageUrl"] = imageUrl
                    options = getOptions1(item, subject)
                    question_details["options"] = options
                    question_details["subject"] = subject
                    house.append(question_details)
                    print(house)
                    logger.info(f"Extracted question: {question_details}")
                convertToJson1(house, subject)
                logger.info("End of site reached, thank you for tiffing questions")

        return Response({'message': 'Results extracted successfully', 'results': house}, status=200)
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return Response({'error': str(e)}, status=500)