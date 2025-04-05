import requests
import json
import math
from pymongo import MongoClient
from datetime import datetime,date
import time
reqUrl = "https://api.ted.europa.eu/private-search/api/v1/notices/search"
todays_date=date.today().strftime("%Y%m%d")

headersList = {
 "accept": "application/json, text/plain, */*",
 "accept-encoding": "gzip, deflate, br, zstd",
 "accept-language": "en-US,en;q=0.9",
 "content-length": "718",
 "content-type": "application/json",
 "cookie": "COOKIE_SUPPORT=true; cck1=%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D; route=1736954110.584.30.160967|726825d00aba56cccab96f4e82375684; GUEST_LANGUAGE_ID=en_GB; ted-public-api-route=1736959210.315.31.197074|9b69c7a6a9bf351194f4c6cc2e746297; JSESSIONID=6C65D00722DFC966E012C50778156FE5.liferay-prod-0",
 "origin": "https://ted.europa.eu",
 "priority": "u=1, i",
 "referer": "https://ted.europa.eu/",
 "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
 "sec-ch-ua-mobile": "?0",
 "sec-ch-ua-platform": '"Windows"',
 "sec-fetch-dest": "empty",
 "sec-fetch-mode": "cors",
 "sec-fetch-site": "same-site",
 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
}

# payload = '{"query":"(publication-date=20250117) SORT BY publication-number DESC","page":1,"limit":50,"fields":["publication-number","BT-5141-Procedure","BT-5141-Part","BT-5141-Lot","BT-5071-Procedure","BT-5071-Part","BT-5071-Lot","BT-727-Procedure","BT-727-Part","BT-727-Lot","place-of-performance","procedure-type","contract-nature","buyer-name","buyer-country","publication-date","deadline-receipt-request","notice-title","official-language","notice-type","change-notice-version-identifier"],"validation":false,"scope":"ACTIVE","language":"EN","onlyLatestVersions":false,"facets":{"business-opportunity":[],"cpv":[],"contract-nature":[],"place-of-performance":[],"procedure-type":[],"publication-date":[],"buyer-country":[]}}'

payload = f'''{{
    "query": "(publication-date={todays_date}) SORT BY publication-number DESC",
    "page": 1,
    "limit": 50,
    "fields": [
        "publication-number",
        "BT-5141-Procedure",
        "BT-5141-Part",
        "BT-5141-Lot",
        "BT-5071-Procedure",
        "BT-5071-Part",
        "BT-5071-Lot",
        "BT-727-Procedure",
        "BT-727-Part",
        "BT-727-Lot",
        "place-of-performance",
        "procedure-type",
        "contract-nature",
        "buyer-name",
        "buyer-country",
        "publication-date",
        "deadline-receipt-request",
        "notice-title",
        "official-language",
        "notice-type",
        "change-notice-version-identifier"
    ],
    "validation": false,
    "scope": "ACTIVE",
    "language": "EN",
    "onlyLatestVersions": false,
    "facets": {{
        "business-opportunity": [],
        "cpv": [],
        "contract-nature": [],
        "place-of-performance": [],
        "procedure-type": [],
        "publication-date": [],
        "buyer-country": []
    }}
}}'''
response = requests.request("POST", reqUrl, data=payload,  headers=headersList)






raw_data = response.content.decode('utf-8')

json_data = json.loads(raw_data)

total_tenders=json_data['totalNoticeCount']

total_pages=math.ceil(total_tenders/99)

tenders=json_data['notices']

tender_count=1
tender_details=[]


page=1
while page <=total_pages:
    payload = {
        "query": f"(publication-date={todays_date}) SORT BY publication-number DESC",
        "page": page,
        "limit": 99,
        "fields": [
            "publication-number", "BT-5141-Procedure", "BT-5141-Part", "BT-5141-Lot", 
            "BT-5071-Procedure", "BT-5071-Part", "BT-5071-Lot", "BT-727-Procedure", 
            "BT-727-Part", "BT-727-Lot", "place-of-performance", "procedure-type", 
            "contract-nature", "buyer-name", "buyer-country", "publication-date", 
            "deadline-receipt-request", "notice-title", "official-language", 
            "notice-type", "change-notice-version-identifier"
        ],
        "validation": False,
        "scope": "ACTIVE",
        "language": "EN",
        "onlyLatestVersions": False,
        "facets": {
            "business-opportunity": [], "cpv": [], "contract-nature": [],
            "place-of-performance": [], "procedure-type": [], "publication-date": [], 
            "buyer-country": []
        }
    }


    response = requests.post(reqUrl, json=payload, headers=headersList)


    raw_data = response.content.decode('utf-8')
    # time.sleep(5)
    try:
        json_data = json.loads(raw_data)
    except:
        json_data = json.loads(raw_data)
    
    tenders=json_data['notices']

    for tender in tenders:
        print("<============================================>")
        print(f"Tender Count : {tender_count} / {total_tenders}")
        
        #deadline=tender[]
        tender_no=tender['publication-number']
        print(f"Tender No : {tender_no}")
        
        tender_title=tender['notice-title']['eng']
        print(f"Tender Title : {tender_title}")
        
        publication_date=tender['publication-date'].split('+')[0]
        publication_date=datetime.strptime(publication_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        
        tender_link=tender['links']['html']['ENG']
        country=tender['place-of-performance'][0].get('label')
        
        tender_count +=1
        print("<============================================>\n")
        
        tender_document = {
        "tender_number": tender_no,
        "publication_date": publication_date,
        "deadline": "",
        "tender_title": tender_title,
        "tender_link": tender_link,
        "country": country
        }
        tender_details.append(tender_document)
    
        
    page +=1

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
        
        