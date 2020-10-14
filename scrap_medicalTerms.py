import requests
from bs4 import BeautifulSoup
import html5lib
import string
import json
import csv


def scrap_me():
    
    lst_pages = [i for i in string.ascii_lowercase]
    
    lst_pages.insert(0,"~")
    print(lst_pages)
    base_url = "https://www.online-medical-dictionary.org"
    lst_data = list()

    for page in lst_pages:
        print(f"Scraping  page {page}")
        url = f"https://www.online-medical-dictionary.org/glossary/{page}.html"
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html5lib')
        unorder_list = soup.find('ul', attrs = {'id' : "listing"})
        #print(unorder_list)
        term = iter(unorder_list.findAll('li'))
        while True:
            try:
                dict_data= {}
                dict_data['term_name'] = next(term).text
                inner_url = next(term).a['href']
                print(f"Scraping  term {dict_data['term_name']}")
                lst_synonyms_nDetail = get_details(inner_url)
                dict_data['synonyms'] = lst_synonyms_nDetail['synonyms']
                dict_data['details'] = lst_synonyms_nDetail['detail']
                lst_data.append(dict_data)
            except StopIteration:
                break
        
        #print(lst_data[1:5])

        with open("output.json", 'w') as outfile:
            json.dump(lst_data, outfile)

        '''
        for term in unorder_list.findAll('li'):
            dict_data= {}
            dict_data['term_name'] = term.text
            inner_url = term.a['href']
            lst_synonyms_nDetail = get_details(inner_url)
            dict_data['synonyms'] = lst_synonyms_nDetail['synonyms']
            dict_data['details'] = lst_synonyms_nDetail['detail']
            lst_data.append(dict_data)
        print(lst_data[1:5]) 
        '''
       
        
def get_details(inner_url):

    dict_synonyms_nDetail = dict()

    sub_url = f"https://www.online-medical-dictionary.org{inner_url}"
    #print(sub_url)
    request = requests.get(sub_url)
    #print(request.content)
    soup = BeautifulSoup(request.content, 'html5lib')
    # Get synonyms
    #print(soup.prettify())
    try:
        div_synonyms = soup.find('div', attrs = { 'class' : 'card synonyms'})
        syn_list = ""
        div_body  = div_synonyms.find('div', attrs = {'class' : 'card-body'})
        synonyms = iter(div_body.find_all('h2'))

        while True:
            try:
                if syn_list == "":
                    syn_list = next(synonyms).text
                else:
                    syn_list = syn_list + ";" + next(synonyms).text
                
            except StopIteration:
                break
        
        dict_synonyms_nDetail['synonyms'] = syn_list
        
    except AttributeError:
        dict_synonyms_nDetail['synonyms'] = ""
    
    try:
        dict_synonyms_nDetail['detail'] = soup.find('p').text
    except AttributeError:
        dict_synonyms_nDetail['detail'] = ""
    
    return dict_synonyms_nDetail


#get_link("/definitions-a/a-kinase-anchor-proteins.html")
scrap_me()
