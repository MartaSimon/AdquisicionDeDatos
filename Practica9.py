import requests
from bs4 import BeautifulSoup
import csv

'''
url = "https://en.wikipedia.org/wiki/Lists_of_universities_and_colleges_by_country"
response = requests.get(url)

# Parseamos el HTML
soup = BeautifulSoup(response.content, "html.parser")

ul_list = soup.find_all("ul")

countries = []
for item in ul_list[3:12]:
    continent  = item.find_all("li")
    for country in continent:
        if not 'United Kingdom' in country.get_text():
            countries.append([country.get_text(), country.a['href']])
            # print(country.get_text())
            # print(country.a['href'])

# Eliminamos duplicados 
for element in countries:
    if countries.count(element) > 1:
        countries.remove(element)
        # print(element)

with open("countries.csv", "w",newline='') as output_file:
    writer = csv.writer(output_file , delimiter =";")
    for row in countries:
        if not row: continue
        writer.writerow(row)
        '''

# ----------------------------------- Apartado 2 ---------------------------------------------


with open("countries.csv", "r") as input_file:
    reader = csv.reader(input_file , delimiter =";")
    country_matrix = [row for row in reader] 

for country in country_matrix:
    if(country[0] == "Germany"):
        url_aux = country[1]
        url = "https://en.wikipedia.org" + url_aux
        print(url)
        response = requests.get(url)

        # Parseamos el HTML
        soup = BeautifulSoup(response.content, "html.parser")
        
        table_germany = soup.find("table", class_="wikitable sortable")

        saved_universities = []

        for item in table_germany:
            universities_row  = table_germany.find_all("tr")
            # print(universities)
            for university in universities_row[1:]:
                univ_col = university.find_all("td")[0]
                # print(univ_col.a["href"], univ_col.get_text())
                saved_universities.append([country[0],url,univ_col.get_text().replace("\n", ""), univ_col.a['href']])

print(saved_universities)
with open("universities.csv", "w",newline='') as output_file:
    writer = csv.writer(output_file , delimiter =";")
    for row in saved_universities:
        if not row: continue
        writer.writerow(row)
