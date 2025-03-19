
import argparse
from pubmed_module import fetch_pubmed_papers, fetch_paper_details, extract_non_academic_authors, save_to_csv
    
    
def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers and extract non-academic authors.")
    
    parser.add_argument("query", type=str, help="Search query for PubMed (e.g., 'Cancer Treatment')")
    parser.add_argument("--max-results", type=int, default=5, help="Number of results to fetch (default: 5)")
    parser.add_argument("-f","--file", type=str, default="filtered_papers.csv", help="Output CSV file name")
    parser.add_argument("-d","--debug", action="store_true", help="Enable debugging mode to print additional logs")

    args = parser.parse_args()

    # Step 1: Get PubMed IDs
    print(f"🔎 Fetching papers for query: {args.query}")
    pubmed_ids = fetch_pubmed_papers(args.query, args.max_results)

    if not pubmed_ids:
        print("❌ No PubMed IDs found.")
        return

    # Step 2: Get Full Paper Details in XML Format
    xml_data = fetch_paper_details(pubmed_ids)

    if not xml_data:
        print("❌ No paper details retrieved. Exiting...")
        return

    # Step 3: Extract Non-Academic Authors
    results = extract_non_academic_authors(xml_data)
    
    # Step 4: Save Results
    save_to_csv(results, args.file)

    # Summary
    print(f"📄 Total papers fetched: {len(pubmed_ids)}")
    print(f"✅ Papers saved to CSV: {len(results)}")
    print(f"⚠️ Papers skipped (only academic authors): {len(pubmed_ids) - len(results)}")    

