import requests
from bs4 import BeautifulSoup

# Obtenemos los datos
url = "https://en.wikipedia.org/wiki/Comillas_Pontifical_University"
response = requests.get(url)

# Parseamos el HTML
soup = BeautifulSoup(response.content, "html.parser")

# Buscamos el elemento que queremos inspeccionar
target_tables = soup.find_all("table", class_="infobox vcard")

# Comprobamos que el elemento que hemos obtenido es único
print(len(target_tables))

table = target_tables[0]
data_dic = {}

seal = table.find("td", class_="infobox-image")
data_dic["seal"] = seal.a["href"]

print(data_dic)

italics = table.find_all("i")
motto = ["motto_latin", "motto_spanish", "motto_english"]
for i in range(len(italics)):
    data_dic[motto[i]] = italics[i].getText()

print(data_dic)


rows = table.find_all("tr")
for item in rows:
    print(item)
    text = item.getText()
    print(text)
    




