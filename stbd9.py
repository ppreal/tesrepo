import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def has_wikipedia_page(name):
    url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
    response = requests.head(url)
    return response.status_code == 200

def get_died_info(name):
    url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        born_element = soup.find('th', class_='infobox-label', string='Born')
        died_element = soup.find('th', class_='infobox-label', string='Died')

        if died_element:
            died_info = died_element.find_next('td')
            if died_info:
                return f"{name} died on {died_info.text.strip()}"
        else:
            birth_date_element = born_element.find_next('span', class_='bday')
            if birth_date_element:
                birth_date = birth_date_element.text.strip()
                age = calculate_age(birth_date)
                return f"{name} is alive and kickin' at {age} !!!"
    
def generate_html(names):
    today = date.today()
    formatted_date = today.strftime("%d.%m.%Y")
    
    html_content = f"<html><head><title>Wikipedia Pages</title></head><body><ul><font size='7'><i><li>Musicians/singers born before 1946:</li></i></font><font size='6'><li>(per Wikipedia - {formatted_date})</li><li>for Teddie Chinery see <a href='https://en.wikipedia.org/wiki/The_Beverley_Sisters'>The Beverly Sisters</a></li></font><font size='7'></ul><ol>"

    for name in names:
        wikipedia_url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
        if has_wikipedia_page(name):
            died_info = get_died_info(name)
            html_content += f"<li><a href='{wikipedia_url}'>{died_info}</a></li>"
            print(died_info)
        else:
            html_content += f"<li>{name}: no wikipedia page found.</li>"
            print(f"{name}: no wikipedia page found.")

    html_content += "</font></ol></body></html>"

    # Incorporate the formatted date into the file name
    file_name = f"Live&kick_{formatted_date}.html"
    
    # Save HTML file
    with open(file_name, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

if __name__ == "__main__":
    # Replace with the path to your names.txt file
    file_path = "names.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        names_list = [line.strip() for line in file]

    generate_html(names_list)
