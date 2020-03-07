import urllib.request
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import csv
import time
from yelp_uri.encoding import recode_uri
from random import randrange
import os.path
from os import path

exceptions_file_name = "exceptions.txt"     # exceptions file
# jud = "Cluj"
# jud = "Bucure%2526%2523351%253Bti"
jud = "Ilfov"
base_link = "http://ghidulmuzeelor.cimec.ro/seljud.asp?judet=" + jud
output_file_name ="MUZ" + jud + ".csv"

### main function
def main():
    error_links, link_list = MUZ_scraper(base_link)
    while error_links:
        error_links, links = MUZ_scraper(error_links)
        link_list.extend(links)

    while link_list:
        link_list = scraper(link_list, output_file_name)

# MUZ scraper function -returns a list of links to all records
def MUZ_scraper(base_link):
    cod_list = []
    error_links = []
    try:
        req = urllib.request.Request(
            base_link, 
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0'
            }
        )
        
        f = urllib.request.urlopen(req)
        soup = bs(f.read().decode('utf-8'))
        
        for link in soup.find_all('a'):
            text = link.get_text()
            href = link.get('href')
            if re.match(re.compile(r"detalii"),text):
                cod_list.append("http://ghidulmuzeelor.cimec.ro/" + href)
                print("http://ghidulmuzeelor.cimec.ro/" + href)
    
    except Exception as e:
        exceptions_file = open(exceptions_file_name,'a')
        exceptions_file.write(str(e) + ": " + url + "\n")
        exceptions_file.close()
        error_links.append(url)

    time.sleep(1)
    return error_links, cod_list


# content scraper function -scraps relevant content from each page and saves it to .csv files
def scraper(link_list, output_file_name):
    rec = []    # stores information from all tables
    error_links = []    # stores links that raised errors when trying to open
    count = 0

    for url in link_list:
        url = recode_uri(url)   # re-encoding potentially poorly encoded urls
        try:
            req = urllib.request.Request(
                url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            f = urllib.request.urlopen(req)
            soup = bs(f.read().decode('utf-8'))

            count += 1
            print("count = " + str(count))
            ### Info
            try:
                cod_detinator = soup.find("td", string = "Cod deținător").find_next_sibling("td").contents[0]
            except:
                cod_detinator = "lipsa cod_detinator"
            print(cod_detinator)

            try:
                denumirea = soup.find("td", string = "Denumire").find_next_sibling("td").contents[0]
            except:
                denumirea = "lipsa denumire"
            print(denumirea)

            try:
                judet = soup.find("td", string = "Județ").find_next_sibling("td").contents[0]
            except:
                judet = "lipsa judet"
            print(judet)

            try:
                localitate = soup.find("td", string = "Localitatea").find_next_sibling("td").contents[0]
            except:
                localitate = "lipsa localitate"
            print(localitate)

            try:
                adresa = soup.find("td", string = "Adresa").find_next_sibling("td").contents[0]
            except:
                adresa = "lipsa adresa"
            print(adresa)

            try:
                cod_postal = soup.find("td", string = "Cod postal").find_next_sibling("td").contents[0]
            except:
                cod_postal = "lipsa cod postal"
            print(cod_postal)

            try:
                telefon = soup.find("td", string = "Telefon").find_next_sibling("td").contents[0]
            except:
                telefon = "lipsa telefon"
            print(telefon)

            try:
                email = soup.find("td", string = "Adresa E-MAIL").find_next_sibling("td").contents[0]['href']
                email = email.replace("mailto:","")
            except:
                email = "lipsa email"
            print(email)

            try:
                acces = soup.find("td", string = "Acces").find_next_sibling("td").contents[0]
            except:
                acces = "lipsa info acces"
            print(acces)

            try:
                program = soup.find("td", string = "Program").find_next_sibling("td").contents[0]
            except:
                program = "lipsa info acces"
            print(program)

            try:
                director = soup.find("td", string = "Director").find_next_sibling("td").contents[0]
            except:
                director = "lipsa info director"
            print(director)

            try:
                descriere = soup.find("td", string = "Descriere").find_next_sibling("td").contents[0]
            except:
                descriere = "lipsa descriere"
            print(descriere)

            try:
                cod_LMI = soup.find("td", string = re.compile(r'^([A-Z]+\-I)')).contents[0]
            except:
                cod_LMI = "lipsa cod_LMI"
            print(cod_LMI)

            try:
                categoria = soup.find("td", string = "Categoria").find_next_sibling("td").contents[0]
            except:
                categoria = "lipsa categorie"
            print(categoria)

            try:
                profil_general = soup.find("td", string = "Profil general").find_next_sibling("td").contents[0]
            except:
                profil_general = "lipsa profil general"
            print(profil_general)

            try:
                profil_principal = soup.find("td", string = "Profil principal").find_next_sibling("td").contents[0]
            except:
                profil_principal = "lipsa profil principal"
            print(profil_principal)

            try:
                web_site = soup.find("td", string = "Adresa WEB").find_next_sibling("td").contents[0]['href']
            except:
                web_site = "lipsa site web"
            print(web_site)

            try:
                persoana_contact = soup.find("td", string = "Persoana contact").find_next_sibling("td").contents[0]
            except:
                persoana_contact = "lipsa persoana contact"
            print(persoana_contact)

            try:
                an_infiintare = soup.find("td", string = "Anul înființării").find_next_sibling("td").contents[0]
            except:
                an_infiintare = "lipsa informatii an infiintare"
            print(an_infiintare)

            try:
                link_harta = soup.find("td", string = "Afişare pe hartă").find_next_sibling("td").contents[0]['href']
            except:
                link_harta = "lipsa link harta"
            print(link_harta)

            rec.append([cod_detinator, denumirea, judet, localitate, adresa, cod_postal, telefon, email, acces, program, director, descriere, cod_LMI, categoria, profil_general, profil_principal, web_site, persoana_contact, an_infiintare, link_harta])

            print("__________________________________________________________________________________________________________")    
        
        except Exception as e:
            exceptions_file = open(exceptions_file_name,'a')
            exceptions_file.write(str(e) + ": " + url + "\n")
            exceptions_file.close()
            error_links.append(url)

        time.sleep(randrange(3))
        if count % 10 == 0:
            print("sleeping 5")
            time.sleep(5)

    df = pd.DataFrame(rec, columns = ['cod_detinator', 'denumirea', 'judet', 'localitate', 'adresa', 'cod_postal', 'telefon', 'email', 'acces', 'program', 'director', 'descriere', 'cod_LMI', 'categoria', 'profil_general', 'profil_principal', 'web_site', 'persoana_contact', 'an_infiintare', 'link_harta'])
    df.to_csv(output_file_name, mode = 'a', header = not(path.exists(output_file_name)), index = False) # if the file doesn't exist, create it and write the dataframe with a header else it append the dataframe without header

    exceptions_file = open(exceptions_file_name,'a')
    exceptions_file.write("________________________________________________________________" + "\n")
    return error_links



# calling the main function
if __name__ == "__main__":
    main()