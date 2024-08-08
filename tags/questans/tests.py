import json
import bs4
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from requests_html import HTMLSession
import os
import requests


#subjects below for cliffnotes websites
"""""accounting,
algebra,
basic-math,
biology,
calculus,
chemistry,
french,
spanish,
history,

writing,
american-government,
anatomy-and-physiology,
astronomy,
statistics,
trigonometry,
differential-equations,
criminal-justice,
psychology,
earth-science,
economics,
english,
geology,
geometryx,
grammar,
physicsx,
principles-of-management,
sociology,
"""


""""class DownloadImageAPITest(APITestCase):
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

class DownloadImageAPITest1(APITestCase):
    def test_download_image1_api(self):

        # Test data
        data = {
            'imageUrl': 'https://myschool.ng/storage/classroom/21371649570_co1.jpg',
            'structure': 'OBJECTIVE',
            'number': 45,
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': '2002'
        }     
        # Send POST request to API
        response = self.client.post('/download-image1/', data, format='json')
        
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
        response = self.client.post('/create-directory1/', data, format='json')
        
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
        self.assertEqual(response.data['message'], 'results extracted successfully')"""""

class Extract1DataAPITest(APITestCase):
    def test_extract1_data_api(self):
        subject = "MATH"
        house = []
        data = {
          'subject': subject,
          'house': house
        }
         
         # Send POST request to API
        response = self.client.post('/extract1-data/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse the JSON response
        response_data = response.json()
        # Check if the response contains the expected result key
        print("Response message:", response_data['message'])
        self.assertEqual(response_data['message'], 'results extracted successfully')





class Upload(APITestCase):
 def upload_json_to_api(file_path, api_url):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return
    
    # Read and print file content
    with open(file_path, 'r') as file:
        file_content = file.read()
        print(f"File content to be uploaded: {file_content[:500]}")  # Print first 500 characters for brevity
    
    # Open file in binary mode for upload
    with open(file_path, 'rb') as file:
        try:
            files = {'inputFile': file}
            data = {'index': '0'}
            print(f"Sending request to {api_url} with file {file_path}")
            response = requests.post(api_url, files=files, data=data)
            
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            
            print("File uploaded successfully")
            print(f"Response JSON: {response.json()}")
            return response.json()  # Return the response JSON for further processing if needed
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.content.decode()}")
        except Exception as err:
            print(f"Other error occurred: {err}")

# Example usage
file_path = 'output_WAEC_2023_chemistry_obj.json'  # Replace with your actual file path
api_url = 'https://afternoon-prep-taggging.onrender.com/objective'
upload_json_to_api(file_path, api_url)
