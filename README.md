

## 📌 Project Overview
The Research Paper Extractor is a Python command-line tool that fetches research papers from PubMed based on a user-specified query. It identifies papers with at least one author affiliated with a pharmaceutical or biotech company and exports the results as a CSV file.
## 🚀 Features

Fetch research papers using the PubMed API.
Filter authors to identify non-academic affiliations (e.g., pharmaceutical or biotech companies).
Save results to a CSV file with structured data.
Command-line options for flexibility in fetching and exporting results.
Error handling for API failures and invalid queries.
Modular code design with reusable components.

## 📂 Output Format (CSV)
The results are saved in a CSV file with the following columns:

PubmedID - Unique identifier for the paper.


Title - Title of the research paper.


Publication Date - Full date of publication (YYYY-MM-DD).


Non-academic Authors - Names of authors affiliated with non-academic institutions.


Company Affiliations - Names of pharmaceutical/biotech companies.


Corresponding Author Email - Email address of the corresponding author (if available).



## 🛠️ Installation &amp; Setup
This project uses Poetry for dependency management.
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Avni2002/Research_paper_Extraction.git
cd Research_paper_Extraction
```

### 2️⃣ Install Dependencies

```sh
pip install poetry
```

### 3️⃣ Run the Program
```sh
poetry run python -m research_paper_extraction.main "Cancer Treatment" --max-results 10 --file 
```

## 🎯 Usage &amp; CLI Options
Run the script using the following syntax:
```sh
poetry run python -m research_paper_extraction.main &lt;query&gt; [options]
```

### Command-Line Options:
-h, --help - Show help message and exit.


-d, --debug - Enable debug mode to print logs.


-f, --file &lt;filename&gt; - Specify CSV filename (default: filtered_papers.csv).


--max-results &lt;N&gt; - Limit the number of results (default: 5).



## 🛠️ Development &amp; Contribution

Fork the repository on GitHub.
Create a new branch for your feature:
```sh
git checkout -b feature-branch
```


Commit your changes and push to GitHub:
```sh
git commit -m "Added feature XYZ"
git push origin feature-branch
```


Submit a Pull Request!

## ⚡ Example Run
```sh
poetry python -m research_paper_extraction.main "Cancer Immunotherapy" --max-results 5 --file output.csv
```

Example output:
```sh
🔎 Fetching papers for query: Cancer Immunotherapy
📄 Saving 5 papers to output.csv...
✅ Results saved to output.csv
```

## 📜 License
This project is licensed under the MIT License.
## 💡 Acknowledgments

NCBI PubMed API for providing research data.
Open-source contributors for their valuable support.

## 📧 Contact
For queries, reach out to Ritu at [your.meherrituparna@example.com](mailto:your.meherrituparna@example.com).
