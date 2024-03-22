import json
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status


class DownloadImageAPITest(APITestCase):
    def test_download_image_api(self):

        # Test data
        data = {
            'imageUrl': 'https://myschool.ng/storage/classroom/12822986898_scan work.jpg',
            'structure': 'OBJECTIVE',
            'number': 45,
            'type': 'JAMB',
            'subject': 'CHEMISTRY',
            'year': 2002
        }
        
        # Send POST request to API
        response = self.client.post('/download-image/', data, format='json')
        
        # Check response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Image downloaded successfully')


