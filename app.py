import os
import requests
from config import API_KEY, API_URL, KEYWORDS, RET_MAX
from datetime import datetime


def get_papers(study_type=None, publication_date=None, keywords=None):
    params = { 
        'db': 'pubmed',
        'term': keywords or KEYWORDS,
        'retmax': RET_MAX,
        'retmode': 'json',
        'api_key': API_KEY
    }

    # Add additional filters based on study type and publication date
    if study_type:
        params['study_type'] = study_type
    if publication_date:
        params['publication_date'] = publication_date

    # Create a directory with the current date and time
    current_time = datetime.now().strftime("%Y%m%d")
    os.makedirs(current_time, exist_ok=True)

    print(f'Requesting data with parameters: {params}')  # Debugging output
    response = requests.get(API_URL, params=params)


    if response.status_code == 200:
        # Fetch details for each paper in the idlist
        idlist = response.json().get('esearchresult', {}).get('idlist', [])
        for paper_id in idlist:
            paper_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={paper_id}&api_key={API_KEY}'  # Constructing the paper URL
            


            paper_response = requests.get(paper_url)
            if paper_response.status_code == 200:
                with open(os.path.join(current_time, f'paper_{paper_id}.xml'), 'w') as f:

                    f.write(paper_response.text)
            else:
                print(f'Error: Failed to fetch paper {paper_id}, status code: {paper_response.status_code}')
    else:
        print(f'Error: Failed to fetch data, status code: {response.status_code}')

if __name__ == '__main__':
    get_papers()
