from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your connection string
db = client["newDB2"]                  # Replace with your database name
collection = db["users"]            # Replace with your collection name

# Define the keyword to search
keyword = "india"

# Fetch records containing the keyword (case-insensitive search)
# Assuming the keyword is to be searched in a field named 'text_field'
query = {"tender_title": {"$regex": keyword, "$options": "i"}}

# Execute the query
results = collection.find(query)

# Print the matching records
for record in results:
    print(record)

# Close the connection
client.close()
