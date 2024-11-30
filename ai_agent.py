import os
import PyPDF2
import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI

def extract_text_from_pdfs(folder_path, error_code, make):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            with open(os.path.join(folder_path, filename), 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if error_code in text or make in text:
                        results.append(text)
    return results

def search_web(query):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links[:5]

def generate_solution(texts, error_code, make):
    prompt = f"""
    Error Code: {error_code}
    Make: {make}
    Context: {texts}

    Provide a step-by-step guide to fix this issue.
    """
    llm = OpenAI(api_key="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")
    return llm(prompt)

if __name__ == "__main__":
    error_code = input("Enter error code: ")
    make = input("Enter make: ")

    pdf_results = extract_text_from_pdfs('./PDF', error_code, make)
    web_results = search_web(f"{make} {error_code} fix")
    final_solution = generate_solution(" ".join(pdf_results), error_code, make)
    print("Step-by-Step Solution:")
    print(final_solution)

