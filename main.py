from bs4 import BeautifulSoup
import requests
import pandas as pd
#just modified a little bit my ipynb and collected all to this py
services = []
url='https://egov.kz/cms/ru/online-services/for_citizen'
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            } ### to prevent the security and access issues

def request_sender(url, headers):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res

def info_getter(service):   ### optional function, but it is used to get service description
    req2 = request_sender(f'https://egov.kz{service}')
    soup2 = BeautifulSoup(req2.content, 'lxml')
    info_block = soup2.find_all(class_='info-block-horizontal')
    if len(info_block) < 2: return 'Empty'
    return '\n'.join([text.text.strip() for text in info_block[1].find_all('p')])

def csv(path):
    return pd.read_csv(path, index_col=0)

def parse_services(url):
    soup = BeautifulSoup(request_sender(url).content, 'lxml')
    services = []
    for category_div in soup.find_all('div', class_='category-item'):
        category = category_div.h2.text.strip()
        for link in category_div.find_all('li'):
            services.append({'category': category, 
                             'service': link.text.strip(), 
                             'link': link.a['href'], 
                             'info': info_getter(link.a['href'])})
    return services

def search(df, column, word):
    df = df[df[column].str.contains(word, case=False, na=False)]
    return df   ### specified column in argument to make this function more flexible


def main():
    url = 'https://egov.kz/cms/ru/online-services/for_citizen'
    df = pd.read_csv('egov_parsing_for_job_interview/egov_parsed.csv', index_col=0)

    while True:
        choice = int(input("1-update database\n2-search\n3-view database\n0-exit: "))
        if choice == 0: break
        elif choice == 1:
            new_services = parse_services(url)
            new_df = pd.DataFrame(new_services)
            new_df.to_csv('egov_parsing_for_job_interview/egov_parsed.csv', mode='a', header=False, index=False)
            print("Database updated.")
        elif choice == 2:
            word = input("Enter word to search for: ")
            results = search(df, 'service', word)
            print(results)
        elif choice == 3:
            print(df)
main()
     
     
     
