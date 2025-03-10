from bs4 import BeautifulSoup
import os
import re
import nltk
import pandas as pd
from datetime import datetime

nltk.download('punkt_tab', quiet=True) 

def extract_sections_from_xml(file_path):
    abstract_text = ""
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'xml')
    abstract_element = soup.find('AbstractText')
    abstract_text = abstract_element.get_text() if abstract_element else ""

    # Split the abstract into sentences for analysis
    sentences = nltk.sent_tokenize(abstract_text)

    # Initialize variables for context, objective, and conclusion
    context = []
    objective = []
    conclusion = []

    # Define regex patterns to identify sections
    context_pattern = re.compile(r'\b(Tauopathies|characterized|defined|phosphorylation|targetable|treatment|therapeutic|disease|condition|symptom|pathology|Alzheimer|cognition|memory|neurodegeneration|clinical|research|study|findings)\b', re.IGNORECASE)
    objective_pattern = re.compile(r'\b(aimed|objective|to determine|goal|purpose|aim|intended|focus|target|investigate|evaluate|assess|analyze|examine)\b', re.IGNORECASE)
    conclusion_pattern = re.compile(r'\b(conclusion|study supports|findings|demonstrated|results|outcomes|implications|suggests|indicates|evidence|concludes|recommendations|noted)\b', re.IGNORECASE)

    # Analyze sentences to categorize them
    for sentence in sentences:
        if context_pattern.search(sentence):
            context.append(sentence.strip())
        elif objective_pattern.search(sentence):
            objective.append(sentence.strip())
        elif conclusion_pattern.search(sentence):
            conclusion.append(sentence.strip())
    
    return abstract_text, context, objective, conclusion

def main():
    directory = datetime.now().strftime("%Y%m%d")  # Directory containing the XML files
    section_data = {}

    for filename in os.listdir(directory)[:50]:  # Limit to 50 files
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")  # Print the file being processed
            abstract, context, objective, conclusion = extract_sections_from_xml(file_path)
            section_data[filename] = {
                'abstract': abstract,
                'context': context,
                'objective': objective,
                'conclusion': conclusion
            }
            print(f"Extracted from {filename}:")
            print(f"Context: {context}")
            print(f"Objective: {objective}")
            print(f"Conclusion: {conclusion}\n")

if __name__ == '__main__':
    main()
