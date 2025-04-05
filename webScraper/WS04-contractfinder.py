import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

tender_count=1
tender_details=[]
for page in range(1,51):
    url=f"https://www.contractsfinder.service.gov.uk/Search/Results?&page={page}#dashboard_notices"
    response=requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    
    tenders=soup.select("#dashboard_notices > div.gadget-body > div")
    for tender in tenders:
        print("============================================================")
        print(f"Tender Count : {tender_count}")
        
        tender_title=tender.select_one("div.search-result-header").text.strip()
        print(f"Tender Title : {tender_title}")
        
        tender_description=tender.select_one("div:nth-child(4)").text.strip()
        try:
            deadline=tender.select_one("div:nth-child(8)").text.strip().split(', ')[0].replace("Closing  ","").replace("Closing ","")
        except:
            deadline=tender.select_one("div:nth-child(8)").text.strip().split(', ')[0].replace("Closing ","")
        try:
            deadline=datetime.strptime(deadline, '%d %B %Y').strftime('%d-%m-%Y')
        except:
            deadline=""
        try:
            publication_date=tender.select_one("div:nth-child(11) > strong").text.strip()
        except:
            publication_date=""
        
        tender_link=tender.select_one("div.search-result-header > h2 > a").get('href')
        
        tender_count +=1
        print("============================================================\n")
        
        tender_document = {
        "tender_number": "",
        "publication_date": publication_date,
        "deadline": "",
        "tender_title": tender_title,
        "tender_link": tender_link,
        "country": "United Kingdom"
        }
        tender_details.append(tender_document)
    
        
client = MongoClient('mongodb://localhost:27017/') 
db = client["newDB2"]
collection = db["users"]


inser_count=1
duplicate_count=1
for tender_detail in tender_details:
    existing_document = collection.find_one({"tender_link": tender_detail["tender_link"]})

    if existing_document:
        print("Duplicate detected. This tender_link already exists in the database.")
        print(f"{duplicate_count } duplicate row rejected")
        duplicate_count +=1
    else:
        
        
        collection.insert_one(tender_detail)
        print("Document inserted successfully.")
        print(f"{inser_count } row inserted")
        inser_count +=1
        print("Data inserted successfully!")