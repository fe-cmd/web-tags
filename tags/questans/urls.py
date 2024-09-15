from django.urls import path
from . import views


from .views import download_image_api, create_newdir_api, extract_data_api, next_page_api, \
    convert_to_json_api, convert_to_pdf_api, get_options_api, get_number_api, get_image_url_api, \
        get_question_api, get_correct_answer_explanation_api, cook_soup_api, write_to_file_api, \
    fetch_me_soup_api, fetch_me_stew_api, eat_sweet_soup_api, \
        result_home_api, extract_theory_data_api, next_pagetheory_api, extract_theory1_data_api
        
app_name = "questans"

urlpatterns = [
    path('', views.result, name="result"),
    path('filters/', views.show_filters, name="show_filters"), 
    path('filters1/', views.show_filters1, name="show_filters1"), 
    path('filters/fetch_questions/', views.fetch_questions, name="fetch_questions"),    
    path('filters1/fetch_questions1/', views.fetch_questions1, name="fetch_questions1"),
    path('filters/fetch_questions/downloads/', views.downloadpq, name="downloadpq"),
    path('filters1/fetch_questions1/downloads/', views.downloadpq, name="downloadpq"),
    path('download-image/', views.download_image_api, name='download_image_api'),
    path('create-directory/', views.create_newdir_api, name='create_newdir_api'),
    path('extract-data/', views.extract_data_api, name='extract_data_api'),
    path('extract-theory-data/', views.extract_theory_data_api, name='extract_theory_data_api'),
    path('extract-theory1-data/', views.extract_theory1_data_api, name='extract_theory1_data_api'),
    path('next-page/', views.next_page_api, name='next_page_api'),
    path('next-pagetheory/', views.next_pagetheory_api, name='next_pagetheory_api'),
    path('convert-to-json/', views.convert_to_json_api, name='convert_to_json_api'),
    path('convert-to-pdf/', convert_to_pdf_api, name='convert_to_pdf_api'),
    path('get-options/', views.get_options_api, name='get_options_api'),
    path('get-number/', views.get_number_api, name='get_number_api'),
    path('get-image-url/', views.get_image_url_api, name='get_image_url_api'),
    path('get-question/', views.get_question_api, name='get_question_api'),
    path('get_questiontheory/', views.get_questiontheory_api, name='get_questiontheory_api'),
    path('get-correct-answer-explanation/', views.get_correct_answer_explanation_api, name='get_correct_answer_explanation_api'),
    path('cook-soup/', views.cook_soup_api, name='cook_soup_api'),    
    path('write-to-file/', write_to_file_api, name='write_to_file_api'),    
    path('fetch-me-soup/', fetch_me_soup_api, name='fetch_me_soup_api'),   
    path('fetch-me-stew/', fetch_me_stew_api, name='fetch_me_stew_api'),   
    path('eat-sweet-soup/', eat_sweet_soup_api, name='eat_sweet_soup_api'),   
    path('result-view/', result_home_api, name='result_home_api'),   
]
