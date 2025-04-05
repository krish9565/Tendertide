import requests
from datetime import datetime
from pymongo import MongoClient

reqUrl = "https://search.worldbank.org/api/v2/procnotices?format=json&fct=procurement_group_desc_exact%2Cnotice_type_exact%2Cprocurement_method_code_exact%2Cprocurement_method_name_exact%2Cproject_ctry_code_exact%2Cproject_ctry_name_exact%2Cregionname_exact%2Crregioncode%2Cproject_id%2Csector_exact%2Csectorcode_exact&fl=id%2Cbid_description%2Cproject_ctry_name%2Cproject_name%2Cnotice_type%2Cnotice_status%2Cnotice_lang_name%2Csubmission_date%2Cnoticedate&srt=submission_date%20desc,id%20asc&apilang=en&rows=1000&srce=both&os=1000"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
json_data=response.json()
tender_count=1
page=1
tender_details=[]
while page<=5:
    if page!=1:
        reqUrl = f"https://search.worldbank.org/api/v2/procnotices?format=json&fct=procurement_group_desc_exact%2Cnotice_type_exact%2Cprocurement_method_code_exact%2Cprocurement_method_name_exact%2Cproject_ctry_code_exact%2Cproject_ctry_name_exact%2Cregionname_exact%2Crregioncode%2Cproject_id%2Csector_exact%2Csectorcode_exact&fl=id%2Cbid_description%2Cproject_ctry_name%2Cproject_name%2Cnotice_type%2Cnotice_status%2Cnotice_lang_name%2Csubmission_date%2Cnoticedate&srt=submission_date%20desc,id%20asc&apilang=en&rows=1000&srce=both&os={page*1000}"

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        json_data=response.json()
    for tender in json_data['procnotices']:
        print("=================================================")
        print(f"Tender Count : {tender_count}")
        
        publication_date=tender['noticedate']
        publication_date=datetime.strptime(publication_date, "%d-%b-%Y").strftime("%d-%m-%Y")
        
        tender_id=tender['id']
        print(f"Tender Id : {tender_id}")
        
        tender_title=tender['project_name']
        print(f"Tender Title : {tender_title}")
        try:
            project_description=tender['bid_description']
        except:
            pass
        
        country=tender['project_ctry_name']
        
        tender_link=f"https://projects.worldbank.org/en/projects-operations/procurement-detail/{tender_id}"
        print("=================================================\n")
        tender_count+=1
        tender_document = {
        "tender_number": tender_id,
        "publication_date": publication_date,
        "deadline": "",
        "tender_title": tender_title,
        "tender_link": tender_link,
        "country": country,
        "project_description" : project_description
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