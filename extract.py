import requests
import pandas as pd
from time import sleep

def get_data_from_internet_archive():
    print("Getting data from Internet Archive...")
    
    url = "https://archive.org/advancedsearch.php"
    
    fields = ["identifier", "title", "creator", "date", "subject", "language", "collection"]
    
    params = {
        "q": "collection:opensource AND mediatype:texts",
        "fl[]": fields,
        "rows": 500,
        "output": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    records = data["response"]["docs"]
    
    df = pd.DataFrame(records)
    df.to_csv("data/raw_collections.csv", index=False)
    
    print(f"Done! Got {len(df)} records")
    print(f"Saved to: data/raw_collections.csv")
    
    print(f"\nQuick check:")
    print(f"  Missing titles: {df['title'].isnull().sum()}")
    print(f"  Missing creators: {df['creator'].isnull().sum()}")
    print(f"  Missing dates: {df['date'].isnull().sum()}")

if __name__ == "__main__":
    get_data_from_internet_archive()
