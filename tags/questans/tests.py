import json
import bs4
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from requests_html import HTMLSession

class DownloadImageAPITest(APITestCase):
    def test_download_image_api(self):

        # Test data
        data = {
            'imageUrl': 'https://myschool.ng/storage/classroom/21371649570_co1.jpg',
            'structure': 'OBJECTIVE',
            'number': 47,
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': 2002
        }     
        # Send POST request to API
        response = self.client.post('/download-image/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'Image downloaded successfully')
        
class CreateNewDirAPITest(APITestCase):
    def test_create_newdir_api(self):
        data = {
            'structure': 'OBJECTIVE',
            'number': '47',
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': '2002'
        }
        
         # Send POST request to API
        response = self.client.post('/create-directory/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'Directory created successfully')
 
class ExtractDataAPITest(APITestCase):
    def test_extract_data_api(self):
        subject = "CHEMISTRY"
        structure = "OBJECTIVE"
        exam_type = "JAMB"
        exam_year = 2002
        st = ""
        subtype = st
        house = []
        if subtype == "MAY/JUNE" or subtype == "MAR":
              subtype = st
        subtype = None
        data = {
          'structure': structure,
          'type': exam_type,
          'subject': subject,
          'year': exam_year,
          'subtype': subtype,
          'house': house
        }
         
         # Send POST request to API
        response = self.client.post('/extract-data/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         # Check if the response contains the expected result key
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'results extracted successfully')
        
class NextPageAPITest(APITestCase):
    def test_next_page_api(self):
        subject = "CHEMISTRY"
        structure = "OBJECTIVE"
        exam_type = "JAMB"
        exam_year = 2002
        st = ""
        subtype = st
        house = []
        if subtype == "MAY/JUNE" or subtype == "MAR":
              subtype = st
        subtype = None
        data = {
          'structure': structure,
          'type': exam_type,
          'subject': subject,
          'year': exam_year,
          'subtype': subtype,
          'house': house
        }
         
         # Send POST request to API
        response = self.client.post('/next-page/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         # Check if the response contains the expected result key
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'next page results tapped successfully')    
        
class ConvertToJsonAPITest(APITestCase):
    def test_convert_to_json_api(self):
        subject = "CHEMISTRY"
        structure = "OBJECTIVE"
        exam_type = "JAMB"
        exam_year = 2002
        st = ""
        subtype = st
        house = []
        if subtype == "MAY/JUNE" or subtype == "MAR":
              subtype = st
        subtype = None
        data = {
          'structure': structure,
          'type': exam_type,
          'subject': subject,
          'year': exam_year,
          'subtype': subtype,
          'house': house
        }
         
         
        response = self.client.post('/convert-to-json/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'Data converted to JSON successfully')   

class GetOptionsAPITest(APITestCase):
    def test_get_options_api(self):
        # Test data
        data = {
            'structure': 'OBJECTIVE',
            'number': 1,
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': 2002,
            
        }     
        response = self.client.post('/get-options/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'options listed out successfully for your choice')

class GetNumberAPITest(APITestCase):
    def test_get_number_api(self):
        data = {
            'structure': 'OBJECTIVE',
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': 2002
        }     
        response = self.client.post('/get-number/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'numbers here successfully')
        
class GetImageUrlAPITest(APITestCase):
    def test_get_image_url_api(self):
        data = {
            'structure': 'OBJECTIVE',
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': '2002',
            'number': '45',
        }     
          # Send POST request to API
        response = self.client.post('/get-image-url/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'Image url extracted successfully')
        
class GetQuestionAPITest(APITestCase):
    def test_get_question_api(self):
        data = {
            'structure': 'OBJECTIVE',
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': 2002,
        }     
        response = self.client.post('/get-question/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'questions passed success!')
        
class GetCorrectAnswerExplanationAPITest(APITestCase):
    def test_get_correct_answer_explanation_api(self):
        data = {
            'structure': 'OBJECTIVE',
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': 2002
        }
        
        response = self.client.post('/get-correct-answer-explanation/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'correct answer explanation success!')
        
class CookSoupAPITest(APITestCase):
    def test_cook_soup_api(self):
        subject = "CHEMISTRY"
        structure = "OBJECTIVE"
        exam_type = "JAMB"
        exam_year = 2002
        st = ""
        subtype = st
        house = []
        if subtype == "MAY/JUNE" or subtype == "MAR":
              subtype = st
        subtype = None
        data = {
          'structure': structure,
          'type': exam_type,
          'subject': subject,
          'year': exam_year,
          'subtype': subtype,
          'house': house
        }
        response = self.client.post('/cook-soup/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Response message:", response.data['message'])
        self.assertEqual(response.data['message'], 'soup prepared deliciously successfully!')
        