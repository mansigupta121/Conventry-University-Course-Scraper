import requests
from bs4 import BeautifulSoup
import time
import json
import re

from config import BASE_URL, COURSE_LISTING_URL, HEADERS, MAX_COURSES, REQUEST_DELAY



#Helper Functions

def get_text_safe(element):
    return element.get_text(strip=True) if element else "NA"


def clean_url(url):
    return url.split("?")[0]


def extract_sentence(text, keyword):
    text_lower = text.lower()
    keyword_lower = keyword.lower()

    if keyword_lower in text_lower:
        start = text_lower.find(keyword_lower)

        chunk = text[start:start+300]
        sentences = chunk.split(".")

        if len(sentences) > 1:
            return sentences[0] + "."
        return chunk

    return "NA"



# Step 1: Discover Course URLs

def discover_course_urls():
    response = requests.get(COURSE_LISTING_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/course-structure/" in href:
            full_url = href if href.startswith("http") else BASE_URL + href
            clean = clean_url(full_url)
            links.add(clean)

        if len(links) >= MAX_COURSES * 2:
            break

    return list(links)[:MAX_COURSES]



# Extract Course Data

def extract_course_data(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    full_text = soup.get_text(separator=" ", strip=True)

    data = {
        "program_course_name": "NA",
        "university_name": "Coventry University",
        "course_website_url": url,
        "campus": "NA",
        "country": "UK",
        "address": "NA",
        "study_level": "NA",
        "course_duration": "NA",
        "all_intakes_available": "NA",
        "mandatory_documents_required": "NA",
        "yearly_tuition_fee": "NA",
        "scholarship_availability": "NA",
        "gre_gmat_mandatory_min_score": "NA",
        "indian_regional_institution_restrictions": "NA",
        "class_12_boards_accepted": "NA",
        "gap_year_max_accepted": "NA",
        "min_duolingo": "NA",
        "english_waiver_class12": "NA",
        "english_waiver_moi": "NA",
        "min_ielts": "NA",
        "kaplan_test_of_english": "NA",
        "min_pte": "NA",
        "min_toefl": "NA",
        "ug_academic_min_gpa": "NA",
        "twelfth_pass_min_cgpa": "NA",
        "mandatory_work_exp": "NA",
        "max_backlogs": "NA"
    }

    
    # Course Name
    
    title = soup.find("h1")
    data["program_course_name"] = get_text_safe(title)

    
    # Study Level
    if "/ug/" in url:
        data["study_level"] = "Undergraduate"
    elif "/pg/" in url:
        data["study_level"] = "Postgraduate"

    
    # Campus
    if "london" in url.lower():
        data["campus"] = "London"
    else:
        data["campus"] = "Coventry"

    
    # Duration
    duration_match = re.search(r"\d+\s*(year|years)", full_text.lower())
    if duration_match:
        data["course_duration"] = duration_match.group()

    
    # Intakes
    if "september" in full_text.lower():
        if "start date" in full_text.lower():
            start = full_text.lower().find("start date")
            chunk = full_text[start:start+150]

            # stop before "How to apply"
            end = chunk.lower().find("how to apply")
            if end != -1:
                chunk = chunk[:end]

            data["all_intakes_available"] = chunk.strip()


    # Tuition Fees
    fee_match = re.search(r"International\s*£\d{1,3},?\d{3}", full_text)

    if fee_match:
        fee = fee_match.group()
        amount = re.search(r"£\d{1,3},?\d{3}", fee)
        if amount:
            data["yearly_tuition_fee"] = amount.group()
    
    
    # Scholarships
    data["scholarship_availability"] = extract_sentence(
    full_text,
    "We offer a range of International scholarships"
    )
    
     
    # Entry Requirements
    data["ug_academic_min_gpa"] = extract_sentence(
    full_text,
    "Select your region to find detailed information about entry requirements"
    )

    
    # English Requirements
    data["min_ielts"] = extract_sentence(full_text, "IELTS")
    data["min_pte"] = extract_sentence(full_text, "PTE Academic")
    data["min_toefl"] = extract_sentence(full_text, "TOEFL")
    data["min_duolingo"] = extract_sentence(full_text, "Duolingo")

    
    # Document
    if "apply" in full_text.lower():
        data["mandatory_documents_required"] = "Refer course page application section"

    return data



# Main

def main():
    print("Discovering course URLs...")
    urls = discover_course_urls()

    print("\n Selected Unique Course URLs:")
    for url in urls:
        print(url)

    courses = []

    for url in urls:
        try:
            print(f"\n Scraping: {url}")
            course_data = extract_course_data(url)
            courses.append(course_data)
            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print(f"Error: {e}")

    # Save JSON
    with open("courses.json", "w", encoding="utf-8") as f:
        json.dump(courses, f, indent=4, ensure_ascii=False)

    print("\n Data saved to courses.json successfully")



if __name__ == "__main__":
    main()