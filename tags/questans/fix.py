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
import re

# Create your views here.

def extract_questions_and_answers(text):
    # Define patterns for questions and sub-questions
    question_patterns = [
        r"(?P<sub>[a-zA-Z]\))\s*(?P<text>.*?)((?=(?:[a-zA-Z]\))|\Z))",
        r"(?P<sub>[ivxlc]+\))\s*(?P<text>.*?)((?=(?:[ivxlc]+\))|\Z))",
    ]
    questions = []

    for pattern in question_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)
        for match in matches:
            questions.append({
                "sub": match.group('sub').strip(')'),
                "text": match.group('text').strip(),
                "Answer": "",
                "subs": []
            })

    return questions

def map_answers_to_questions(questions, answer_text):
    current_index = -1
    for question in questions:
        sub = question["sub"]
        sub_pattern = re.compile(rf"{sub}\)", re.IGNORECASE)
        match = sub_pattern.search(answer_text)
        if match:
            current_index = questions.index(question)
            next_question_index = current_index + 1
            if next_question_index < len(questions):
                next_question_sub = questions[next_question_index]["sub"]
                next_sub_pattern = re.compile(rf"{next_question_sub}\)", re.IGNORECASE)
                next_match = next_sub_pattern.search(answer_text)
                question["Answer"] = answer_text[match.end():next_match.start()].strip() if next_match else answer_text[match.end():].strip()
            else:
                question["Answer"] = answer_text[match.end():].strip()

    return questions

def nest_sub_questions(questions):
    """Function to nest sub-sub-questions under their respective parent sub-questions"""
    nested_questions = []
    current_parent = None

    for question in questions:
        # If the sub-question is a main sub (like a, b, c), set it as the current parent
        if re.match(r'[a-z]', question["sub"], re.IGNORECASE):
            current_parent = question
            nested_questions.append(current_parent)
        # If it's a sub-sub-question (like i, ii, iii), nest it under the current parent
        elif re.match(r'[ivxlc]+', question["sub"], re.IGNORECASE) and current_parent:
            current_parent["subs"].append(question)

    return nested_questions

def parse_questions_and_answers(input_text):
    question_answer_segments = input_text.split("\n(b)")
    
    parsed_data = []
    for segment in question_answer_segments:
        if segment.strip():
            text_parts = segment.split("\n")
            main_question = text_parts[0].strip()
            answer_text = "\n".join(text_parts[1:]).strip()

            questions = extract_questions_and_answers(main_question)
            mapped_questions = map_answers_to_questions(questions, answer_text)
            # Nest sub-sub-questions under their parent sub-questions
            nested_questions = nest_sub_questions(mapped_questions)
            parsed_data.extend(nested_questions)
    return parsed_data

def format_to_json(parsed_data, question_type):
    if question_type == "first":
        return {
            "subType": "MAY/JUNE",
            "flagged": False,
            "flags": [],
            "text": "",
            "subs": parsed_data,
            "year": "2020",
            "subject": "FURTHER MATHEMATICS",
            "type": "WAEC",
            "imageUrl": None,
            "structure": "THEORY",
            "sectionInstruction": ""
        }
    elif question_type == "second":
        return {
            "subType": "MAY/JUNE",
            "flagged": False,
            "flags": [],
            "text": "",
            "subs": parsed_data,
            "year": "2020",
            "subject": "FURTHER MATHEMATICS",
            "type": "WAEC",
            "imageUrl": None,
            "structure": "THEORY",
            "sectionInstruction": ""
        }
    elif question_type == "third":
        return {
            "subType": "MAY/JUNE",
            "flagged": False,
            "flags": [],
            "text": parsed_data[0]["text"] if parsed_data else "",
            "Answer": parsed_data[0]["Answer"] if parsed_data else "",
            "subs": [],
            "year": "2020",
            "subject": "FURTHER MATHEMATICS",
            "type": "WAEC",
            "imageUrl": None,
            "structure": "THEORY",
            "sectionInstruction": ""
        }

@api_view(['GET', 'POST'])
def extract_theory_data_api(request):
    session = HTMLSession()
    structure, num, exam_type, subject, exam_year, subtype, house = get_param1(request)
    url_Struc = "theory" if structure == "THEORY" else "obj"
    additional_url = subject.lower().replace(" ", "-") + "?exam_type=" + exam_type.lower() + "&exam_year=" + str(exam_year) + "&type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup, newsession = cookSoup(url, session)

    if soup is not None and session is not None:
        results = soup.find_all("div", class_="media question-item mb-4")
        for item in results:
            answerLink = item.find("a")
            base_url = answerLink['href']
            newsession = HTMLSession()
            newsoup, newSession = cookSoup(base_url, newsession)

            if newsoup is not None and newsession is not None:
                result = newsoup.select("div[class='mb-4']")
                
                # Extract explanations (answers)
                explanations = extract_explanations(result)  # Extract explanations from the page
                question_Text = getTheoryQuestion(item)  # Extract question text

                if question_Text and explanations:
                    # Build answer text by combining all extracted explanations
                    answer_text = "\n".join([explanation.get("explanation", "") for explanation in explanations])
                    
                    # Combine question and answers
                    full_text = f"{question_Text[0]}\n{answer_text}"

                    # Parse the questions and map them to the answers
                    parsed_data = parse_questions_and_answers(full_text)

                    # Determine question type
                    if len(parsed_data) > 1:
                        question_type = "first"
                    elif len(parsed_data) == 1:
                        question_type = "third"
                    else:
                        question_type = "second"

                    # Format the parsed data into the final JSON structure
                    formatted_json = format_to_json(parsed_data, question_type)
                    house.append(formatted_json)
                    print(house)

        # Check for pagination and get the next page
        next_page_link = soup.find("a", text="»")  # Updated to use the correct pagination text
        while next_page_link:
            next_page_url = next_page_link['href']
            soup, session = cookSoup(next_page_url, session)
            results = soup.find_all("div", class_="media question-item mb-4")

            for item in results:
                answerLink = item.find("a")
                base_url = answerLink['href']
                newsession = HTMLSession()
                newsoup, newSession = cookSoup(base_url, newsession)

                if newsoup is not None and newsession is not None:
                    result = newsoup.select("div[class='mb-4']")
                    
                    # Extract explanations and question text again
                    explanations = extract_explanations(result)
                    question_Text = getTheoryQuestion(item)

                    if question_Text and explanations:
                        answer_text = "\n".join([explanation.get("explanation", "") for explanation in explanations])
                        full_text = f"{question_Text[0]}\n{answer_text}"

                        # Parse and map the questions
                        parsed_data = parse_questions_and_answers(full_text)

                        # Determine question type and format JSON
                        if len(parsed_data) > 1:
                            question_type = "first"
                        elif len(parsed_data) == 1:
                            question_type = "third"
                        else:
                            question_type = "second"

                        formatted_json = format_to_json(parsed_data, question_type)
                        house.append(formatted_json)
                        print(house)

            # Update next page link
            next_page_link = soup.find("a", text="»")  # Look for the next page again
            
    convertToJsonT(house, exam_type, subject, exam_year, structure)
    """"if json_file_path:
        print(f"JSON file saved successfully at {json_file_path}, End of site reached, thank you for tiffing questions" )
        response = upload_json_to_api(json_file_path, 'https://afternoonprep-tagging.onrender.com/theory')
        print(response)                                  
    else:
        print("Error: JSON file path is invalid.")"""""

    return Response({'message': 'results extracted successfully', 'results': house}, status=200)
                            
def extract_question_data(question_data, explanations):
    extracted_data = {
        "subType": question_data.get("subType", ""),
        "flagged": False,
        "flags": [],
        "text": question_data.get("text", "").strip(),
        "Answer": "",
        "subs": [],
        "year": question_data.get("year", ""),
        "subject": question_data.get("subject", ""),
        "type": question_data.get("type", ""),
        "imageUrl": question_data.get("imageUrl", None),
        "structure": question_data.get("structure", ""),
        "sectionInstruction": ""
    }
    
    # Combine all paragraphs in explanations to form the full answer
    full_answer = "\n".join(
        explanation.get("explanation", "")
        for explanation in explanations
        if explanation.get("explanation")
    )
    extracted_data["Answer"] = full_answer

    # Extracting and merging text content
    if "subs" in question_data:
        for i, sub in enumerate(question_data["subs"]):
            sub_dict = {
                "sub": sub.get("sub", ""),
                "text": sub.get("text", ""),
                "Answer": "",
                "imageUrl": sub.get("imageUrl", None),
                "Score": sub.get("Score", None),
                "subs": []
            }
            # Combine explanations for sub-questions
            if i < len(explanations):
                sub_answer = "\n".join(
                    explanation.get("explanation", "")
                    for explanation in explanations[i::len(question_data["subs"])]
                    if explanation.get("explanation")
                )
                sub_dict["Answer"] = sub_answer

            # Handling sub-parts of sub-questions (i, ii, iii, etc.)
            if "subs" in sub:
                for j, sub_part in enumerate(sub["subs"]):
                    sub_part_dict = {
                        "sub": sub_part.get("sub", ""),
                        "text": sub_part.get("text", ""),
                        "Answer": "",
                        "imageUrl": sub_part.get("imageUrl", None),
                        "Score": sub_part.get("Score", None)
                    }      
                    # Combine explanations for sub-parts
                    if j < len(explanations):
                        sub_part_answer = "\n".join(
                            explanation.get("explanation", "")
                            for explanation in explanations[j::len(sub["subs"])]
                            if explanation.get("explanation")
                        )
                        sub_part_dict["Answer"] = sub_part_answer

                    sub_dict["subs"].append(sub_part_dict)
            extracted_data["subs"].append(sub_dict)
            # Extract and merge answers for sub-questions
            if "Answer" in sub and sub["Answer"]:
                sub_dict["Answer"] = "\n".join(
                    explanation.get("explanation", "")
                    for explanation in sub["Answer"]
                    if explanation.get("explanation")
                )

            extracted_data["subs"].append(sub_dict)

    # Handling the case where there are no sub-questions and only the main question text
    if not extracted_data["subs"] and extracted_data["text"]:
        if "Answer" in question_data and question_data["Answer"]:
            extracted_data["Answer"] = full_answer

    return extracted_data

def extract_explanations(elements):
    explanations = []
    
    # Check if elements is a list of BeautifulSoup objects
    if not isinstance(elements, list) or not all(hasattr(el, 'find_all') for el in elements):
        raise ValueError("Provided elements are not valid BeautifulSoup objects")
    
    for element in elements:
        # Extract text from paragraphs
        paragraphs = element.find_all("p")
        for para in paragraphs:
            text = para.get_text(strip=True)
            explanations.append({"explanation": text})
        
        # Extract text from table rows
        tables = element.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                row_text = "\t".join(cell.get_text(strip=True) for cell in cells)
                explanations.append({"explanation": row_text})
        
        # Extract images
        images = element.find_all("img")
        for img in images:
            img_src = img.get("src")
            explanations.append({"imageUrl": img_src})
    
    return explanations

def build_subs(question_Text, explanations):
    subs = []
    for i, text in enumerate(question_Text[1:]):  # Skip the first one as it's the main question
        sub_details = {
            "sub": chr(97 + i),  # 'a', 'b', 'c', etc.
            "text": text,
            "Answer": "",
            "imageUrl": None,
            "Score": None,  # Assuming score is not given
            "subs": []  # Recursive if there are further nested subs
        }
        # Extract explanations for this sub-question
        if i < len(explanations):
            sub_explanations = extract_explanations([bs4.BeautifulSoup(exp, 'html.parser') for exp in explanations[i]])
            if sub_explanations:
                sub_details["Answer"] = "\n".join(
                    exp.get("explanation", "")
                    for exp in sub_explanations
                    if exp.get("explanation")
                )
                # Handle images separately if needed
                sub_details["imageUrl"] = next((exp.get("imageUrl") for exp in sub_explanations if exp.get("imageUrl")), None)
        
        subs.append(sub_details)
    return subs


        

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

@api_view(['GET', 'POST'])
def extract_theory_data_api(request):
    session = HTMLSession()
    structure, num, exam_type, subject, exam_year, subtype, house = get_param1(request)
    url_Struc = "theory" if structure == "THEORY" else "obj"
    additional_url = subject.lower().replace(" ", "-") + "?exam_type=" + exam_type.lower() + "&exam_year=" + str(exam_year) + "&type=" + url_Struc
    url = "https://myschool.ng/classroom/" + additional_url
    soup, newsession = cookSoup(url, session)

    if soup is not None and session is not None:
        results = soup.find_all("div", class_="media question-item mb-4")
        for item in results:
            answerLink = item.find("a")
            base_url = answerLink['href']
            newsession = HTMLSession()
            newsoup, newSession = cookSoup(base_url, newsession)

            if newsoup is not None and newsession is not None:
                result = newsoup.select("div[class='mb-4']")
                
                explanations = extract_explanations(result)  # Pass BeautifulSoup elements
                
                question_Text = getTheoryQuestion(item)
                number = getNumber(item)
                imageUrl = getImageUrl(item, number, structure, exam_type, subject, exam_year)

                # Prepare question data
                question_data = {
                    "subType": subtype,
                    "text": question_Text[0] if question_Text else "",
                    "subs": build_subs(question_Text, explanations),
                    "year": exam_year,
                    "subject": subject.upper(),
                    "type": exam_type.upper(),
                    "imageUrl": imageUrl,
                    "structure": structure,
                    "Answer": []  # Initialize as empty list
                }

                # Extract explanations to populate the "Answer" field
                if explanations:
                    question_data["Answer"] = "\n".join(
                        explanation.get("explanation", "")
                        for explanation in explanations
                        if explanation.get("explanation")
                    )

                # Extract structured data for the question
                question_details = extract_question_data(question_data, explanations)
                house.append(question_details)
                print(house)

        # Pagination handling
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
                            answerLink = item.find("a")
                            base_url = answerLink['href']
                            newsession1 = HTMLSession()
                            newsoup1, newSession = cookSoup(base_url, newsession1)

                            if newsoup1 is not None and newsession1 is not None:
                                result = newsoup1.select("div[class='mb-4']")
                                
                                explanations = extract_explanations(result)  # Pass BeautifulSoup elements
                
                                question_Text = getTheoryQuestion(item)
                                number = getNumber(item)
                                imageUrl = getImageUrl(item, structure, number, exam_type, subject, exam_year)

                                # Prepare question data
                                question_data = {
                                    "subType": subtype,
                                    "text": question_Text[0] if question_Text else "",
                                    "subs": build_subs(question_Text, explanations),
                                    "year": exam_year,
                                    "subject": subject.upper(),
                                    "type": exam_type.upper(),
                                    "imageUrl": imageUrl,
                                    "structure": structure,
                                    "Answer": []  # Initialize as empty list
                                }

                                # Extract explanations to populate the "Answer" field
                                if explanations:
                                    question_data["Answer"] = "\n".join(
                                        explanation.get("explanation", "")
                                        for explanation in explanations
                                        if explanation.get("explanation")
                                    )

                                # Extract structured data for the question
                                question_details = extract_question_data(question_data, explanations)
                                house.append(question_details)
                                print(house)

        json_file_path = convertToJsonT(house, exam_type, subject, exam_year, structure)
        if json_file_path:
            print(f"JSON file saved successfully at {json_file_path}, End of site reached, thank you for tiffing questions" )
            response = upload_json_to_api(json_file_path, 'https://afternoonprep-tagging.onrender.com/theory')
            print(response)                                  
        else:
            print("Error: JSON file path is invalid.")

    return Response({'message': 'results extracted successfully', 'results': house}, status=200)


