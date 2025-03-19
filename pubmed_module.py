import requests
import csv
import argparse
import urllib.parse
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import xml.etree.ElementTree as ET

# Function to fetch PubMed IDs based on a query
def fetch_pubmed_papers(query, max_results=5):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    # Add retry mechanism
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(base_url, params=params, timeout=10)  # 10-second timeout
        response.raise_for_status()  # Raise error for bad responses
        return response.json()["esearchresult"]["idlist"]
    except requests.exceptions.RequestException as e:
        print("Error fetching PubMed IDs:", e)
        return None
    
    
def fetch_paper_details(pubmed_ids):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

        # Convert list of IDs into a comma-separated string
    id_string = ",".join(pubmed_ids)

    params = {
        "db": "pubmed",
        "id": id_string,  # ✅ Corrected: Use comma-separated IDs
        "retmode": "xml"
    }
        
    print(f"🔗 API Request: {base_url}?db=pubmed&id={id_string}&retmode=xml")

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.text  # ✅ Return XML instead of a list
    else:
        print(f"❌ Error fetching paper details: {response.status_code}")
        print(f"🔹 Response Text: {response.text}")
        return None  # ✅ Return None to prevent further errors    
    
    
        
    
# Function to identify non-academic authors
def extract_non_academic_authors(xml_data):
    """
    Extracts non-academic authors from PubMed XML response.
    """
    non_academic_keywords = [
    "inc", "ltd", "biotech", "pharma", "corporation", "technologies",
    "diagnostics", "biosciences", "laboratories", "therapeutics", "research",
    "genomics", "biosystems", "medical", "healthcare", "clinical", "solutions",
    "oncology", "cancer center", "hematology", "biomedical", "research institute",
    "blood disorders", "hematology oncology", "medical center",
    "sobi", "bleeding clotting disorders institute","bleeding clotting disorders institute", 
    "changsha hospital", 
    "hunan normal university hospital",
    "memorial sloan kettering", "cancer institute", "consumer advocate", 
    "independent health technology", "integrate medical professionals",
    "pathology lab", "medical diagnostics", "research center",
    "private healthcare", "oncology services", "bioscience lab",
    "first clinical college", "nebraska hematology oncology cancer center",
    "memorial sloan kettering", "mount sinai", "taipei veterans hospital",
    "independent consumer advocate", "independent health technology",
    "medical research center", "biotech", "private research lab",
    "oncology institute", "integrated medical professionals"
]

    academic_keywords = ["University", "Institute", "College", "Hospital", "School","faculty of pharmacy",
    "school of pharmaceutical",
    "school of physical sciences",
    "department of chemistry","md anderson cancer center",
    "harvard medical school", "university hospital", "university of texas", 
    "university of michigan", "university of toronto", "medical university","university of pennsylvania",
    "university hospital", "university health network", "faculty of medicine",
    "polytechnic university", "pathology department", "medical university",
    "university medical center", "department of pathology", "faculty of medicine"
    "pharmaceutical chemistry", "Department"]

    results = []
    root = ET.fromstring(xml_data)

    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "Unknown Title"
        # Extract full publication date
        year = article.find(".//PubDate/Year")
        month = article.find(".//PubDate/Month")
        day = article.find(".//PubDate/Day")

        # Format as YYYY-MM-DD if all parts are available, otherwise fallback to partial dates
        if year is not None:
            pubdate = f"{year.text}-{month.text if month is not None else '01'}-{day.text if day is not None else '01'}"
        else:
            pubdate = "Unknown Date"


        authors = article.findall(".//Author")
        non_academic_authors = []
        company_affiliations = []
        corresponding_email = "Not Available"

        for author in authors:
            last_name = author.find("LastName")
            first_name = author.find("ForeName")
            affiliation = author.find(".//AffiliationInfo/Affiliation")

            name = f"{first_name.text} {last_name.text}" if first_name is not None and last_name is not None else "Unknown Author"
            affiliation_text = affiliation.text if affiliation is not None else ""

            # Normalize text
            affiliation_clean = re.sub(r"[^\w\s@.-]", "", affiliation_text).lower().strip()

            # Extract email from affiliation
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation_text)
            if email_match:
                corresponding_email = email_match.group(0)

            # Extract email from ELocationID
            email_field = author.find(".//ELocationID[@EIdType='email']")
            if email_field is not None and "@" in email_field.text:
                corresponding_email = email_field.text  # ✅ Use official email if available

            # Check if author is from a non-academic institution
            if any(keyword in affiliation_clean for keyword in non_academic_keywords):
                non_academic_authors.append(name)
                company_affiliations.append(affiliation_clean)

        # Store results only if there are non-academic authors
        if non_academic_authors:
            results.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pubdate,
                "Non-academic Authors": ", ".join(non_academic_authors),
                "Company Affiliations": ", ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })

    return results        


# Function to save results to CSV
def save_to_csv(results, filename="filtered_papers.csv"):
    if not results:
        print("⚠️ No non-academic authors found in any papers.")
        return

    print(f"📄 Saving {len(results)} papers to {filename}...")

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Results saved to {filename}")