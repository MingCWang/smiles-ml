from pymongo import MongoClient, server_api
import pandas as pd

# local
# uri = "mongodb://localhost:27017/"

def get_database():
 
   CONNECTION_STRING = "mongodb://localhost:27017/defaultdb"
 
   client = MongoClient(CONNECTION_STRING, server_api=server_api.ServerApi(
 version="1", strict=True, deprecation_errors=True))

   return client['data']
  
  
def insert_data():
    csv_file_path = './data.csv'  # Replace with the path to your CSV file
    df = pd.read_csv(csv_file_path)
    
    data = df.to_dict(orient='records')
    dbname = get_database()
    collection = dbname["smiles"]
 
    collection.insert_many(data)

if __name__ == "__main__":   
    insert_data()