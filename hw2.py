import requests
from bs4 import BeautifulSoup
url = "https://api.hh.ru/vacancies?text=middle python разработчик&per_page=100"
result = requests.get(url)
if result.status_code == 200:
    vacancies = result.json().get('items')
    for i, vacancy in enumerate(vacancies):
        responsibilitiy = ''
        reqirements = ''
        if (vacancy['snippet']['responsibility'] != None):
            responsibilitiy = BeautifulSoup(vacancy['snippet']['responsibility'], 'lxml').get_text()
        if (vacancy['snippet']['requirement'] != None):
            reqirements = BeautifulSoup(vacancy['snippet']['requirement'], 'lxml').get_text() 
        print(i + 1, vacancy['employer']['name'], vacancy['name'], responsibilitiy, reqirements, sep = '\n')