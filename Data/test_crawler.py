from bs4 import BeautifulSoup
import requests

# Define headers for the HTTP request to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

url = 'https://zendalona.com/accessible-coconut/'

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

features = []
section = soup.find('div', class_='et_pb_section et_pb_section_1 et_section_regular')

if section:
    rows = section.find_all('div', class_='et_pb_row')
    
    for row in rows:
        divs = row.find_all('div', class_='et_pb_column')
        
        for div in divs:
            feature_name = div.find('h4', class_='et_pb_module_header')
            if feature_name:
                feature_name = feature_name.find('span').text.strip()  # Extract text 

            feature_description = div.find('div', class_='et_pb_blurb_description')
            if feature_description:
                feature_description = feature_description.find('p').text.strip()  

            if feature_name and feature_description:
                features.append({
                    'feature_name': feature_name,
                    'feature_description': feature_description
                })

# Print the extracted features
for feature in features:
    print("Feature Name:", feature['feature_name'])
    print("Feature Description:", feature['feature_description'])
    print("-" * 50)
