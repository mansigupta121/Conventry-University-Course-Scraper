# Coventry University Course Scraper

### Senbonzakura Consultancy Assignment

## Project Overview

This project is a web scraper built to extract structured course data from the official Coventry University website.

The scraper:

* Discovers course URLs automatically
* Extracts structured information for **exactly 5 unique courses**
* Outputs the data in **JSON format**
* Uses **only official Coventry University webpages** (no third-party sources)

---

## Tech Stack

* Python
* requests
* BeautifulSoup (bs4)

---

## Project Structure

```

├── scraper.py          # Main scraper script
├── config.py           # Configuration (URLs, headers, constants)
├── requirements.txt    # Dependencies
├── courses.json        # Output file (generated)
└── README.md           # Documentation
```

---

## Setup Instructions

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run the scraper:

```
python scraper.py
```

---

## Output

* The scraper generates a file:

```
courses.json
```

* It contains **exactly 5 unique course records**, each following the required schema.

### Example Fields:

* program_course_name
* university_name
* course_website_url
* campus
* course_duration
* yearly_tuition_fee
* min_ielts
* scholarship_availability
* etc.

---

## Methodology

### 1. Course Discovery

* Scrapes the official course finder page
* Filters URLs containing `/course-structure/`
* Removes duplicates by normalizing URLs (removing query parameters)

### 2. Data Extraction

* Visits each course page

* Uses keyword-based extraction from structured sections like:

  * Fees and funding
  * Entry requirements
  * Course overview

* Extracts **raw text** as allowed in the assignment

### 3. Data Handling

* Missing fields are handled gracefully using `"NA"`
* No manual data entry is used
* All data is extracted dynamically

---

## Assumptions & Notes

* Some fields (e.g., backlogs, Indian boards, GRE/GMAT) are not available on course pages → marked as `"NA"`
* English requirements and other fields are extracted as raw text (not normalized), as per assignment instructions
* Only undergraduate course pages were used for simplicity

---

## Key Features

* Fully automated (no manual intervention)
* Handles missing data safely
* Ensures **no duplicate courses**
* Clean and modular code structure
* Uses only official data sources

---

## Conclusion

This scraper meets all assignment requirements:

*  Official-source-only data
*  Exactly 5 unique courses
*  Structured output
*  Robust and reliable execution

---

## Author

Mansi Gupta
