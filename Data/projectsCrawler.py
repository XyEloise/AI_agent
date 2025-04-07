import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.zendalona
projects_collection = db.projects

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

project_urls = [
    {"project_name": "Accessible Coconut", "project_url": "https://zendalona.com/accessible-coconut/"},
    {"project_name": "SBW", "project_url": "https://zendalona.com/sbw/"},
    {"project_name": "LIOS", "project_url": "https://zendalona.com/lios/"},
    {"project_name": "IBus Braille", "project_url": "https://zendalona.com/ibus-braille/"},
    {"project_name": "Accessibility Extensions for TuxMath", "project_url": "https://zendalona.com/Accessibility-extensions-for-TuxMath/"},
    {"project_name": "Accessible Chess XBoard", "project_url": "https://zendalona.com/accessible-chess-xboard/"},
    {"project_name": "Accessibility Extensions for Tuxtype", "project_url": "https://zendalona.com/accessibility-extensions-for-tuxtype/"},
    {"project_name": "Online Six Key Braille Input", "project_url": "https://zendalona.com/online-six-keybraille-input/"},
    {"project_name": "Accessible Bluff", "project_url": "https://zendalona.com/accessible-bluff/"},
    {"project_name": "Online Braille Translator", "project_url": "https://zendalona.com/online-braille-translator/"},
    {"project_name": "Braille Translator GUI", "project_url": "https://zendalona.com/braille-translator-gui/"},
    {"project_name": "Accessible Snakes and Ladders", "project_url": "https://zendalona.com/accessible-snakes-and-ladders/"},
    {"project_name": "Accessible Maths Tutor", "project_url": "https://zendalona.com/accessible-maths-tutor/"},
    {"project_name": "Kanmani", "project_url": "https://zendalona.com/kanmani/"},
    {"project_name": "Map", "project_url": "https://zendalona.com/map/"},
    {"project_name": "Math Mantra", "project_url": "https://zendalona.com/math-mantra/"},
    {"project_name": "Zendesk", "project_url": "https://zendalona.com/Zendesk/"}
]

def get_project_details(project_url, project_name):
    response = requests.get(project_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract intro
    intro_section = soup.find('div', class_='et_pb_section et_pb_section_0 et_pb_with_background et_section_regular')  
    introduction_info = intro_section.find('p').text.strip() if intro_section.find('p') else "No introduction available."

    # extract features
    features = get_project_features(soup) 

    # extract links
    links = get_project_links(soup)

    project_data = {
        'project_name': project_name,
        'introduction_info': introduction_info,
        'features': features,
        'links': links
    }

    return project_data


def get_project_features(soup):
    section = soup.find('div', class_='et_pb_section et_pb_section_1 et_section_regular')

    if section:
        rows = section.find_all('div', class_='et_pb_row')
        features = {} 
        feature_counter = 1
  
        for row in rows:
            divs = row.find_all('div', class_='et_pb_column')
            
            for div in divs:
                feature_name = div.find('h4', class_='et_pb_module_header')
                if feature_name:
                    feature_name = feature_name.find('span').text.strip() 

                feature_description = div.find('div', class_='et_pb_blurb_description')
                if feature_description:
                    feature_description = feature_description.find('p').text.strip() 

                if feature_name and feature_description:
                  features[f'feature{feature_counter}'] = {
                      'feature_name': feature_name,
                      'feature_description': feature_description
                  }
                  feature_counter += 1
    return features

def get_project_links(soup):
    buttons = soup.find_all('a', class_='et_pb_button')
    links = {}
    link_counter = 1

    for button in buttons:
        button_name = button.text.strip()
        button_link = button.get('href')
        
        if button_name and button_link:
            links[f'link{link_counter}'] = {
                'button_name': button_name,
                'button_link': button_link
            }

    # for link in links:
    #     print(f"Button Name: {link['button_name']}, Button Link: {link['button_link']}")
    return links

def store_project_data(project_data):
    projects_collection.insert_one(project_data)

def main():
    for project in project_urls:
        project_name = project['project_name']
        project_url = project['project_url']
        project_details = get_project_details(project_url, project_name)  
        store_project_data(project_details)  

if __name__ == "__main__":
    main()
