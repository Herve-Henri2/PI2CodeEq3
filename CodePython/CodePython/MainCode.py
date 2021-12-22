#Le code se fera ici
#regarder un tuto sur git hub / git hub desktop
#installer les librairies nécessaires si non installées
# pip install bs4       pip install google      pip install spacy

# On commence par l'exemple de SolarWinds, grande entreprise de contrôle de systèmes informatiques, victime d'une Cyberattaque de grande ampleur en 2020.
# A priori nous aurons déjà nos sources prédéfinies et lorsque que nous nous intéresserons au statut d'une entreprise en particulier,
# nous parcourrons nos sources à l'aide de mots clé (dont le nom de l'entreprise).
# Cependant ici à titre de découverte du web scraping l'approche est un peu différente, nous automatisons le processus de recherche qu'une personne lamba ferait sur Google.
import requests, webbrowser
from bs4 import BeautifulSoup
from googlesearch import search
import spacy 
nlp = spacy.load('en_core_web_sm') #python -m spacy download en

def introwebscraping():
    query= "SolarWinds Cyberattaque" #La recherche que l'on effectue sur Google
    links =[] #Liste qui contiendra tous les liens des sites webs que nous allons "scraper" à l'issue de la recherche.

    for j in search(query, num=3, stop=3, pause=0.5): #On se contente des 3 résultats jugés les plus pertinents par Google dans cet exemple, idéalement en prendre le plus possible.
    #print(j)
        webbrowser.open(j)
        links.append(j) #On sauvegarde les liens

    for link in links:
        print("-------------------------------------------------------------------------------------------------------------------------------------------------------")
        page=requests.get(link)
        soup=BeautifulSoup(page.text, "lxml")  #Lecture du code source de la page
        print(link+"\n")
        print(soup.find("title").text+"\n") #Titre de la page (à priori un article)
        paragraphs=soup.find_all("p")
        keywords=["cyberattaque"] #mots clé pour nous aider à extraire l'information voulue
        keysentences=[] #phrases clé qu'il faudra analyser 
        for paragraph in paragraphs: #Parcourir les paragraphes pour en extraire les informations relatives à une attaque ou faille de sécurité.
            c=nlp(paragraph.text) #Conversion du texte en un objet spacy
            sentences=list(c.sents) 
            for sentence in sentences:
                for keyword in keywords:
                    if keyword in str(sentence):
                        print(sentence)
                        keysentences.append(sentence)
 
                        


#L'idée est de créer un algorithme de scraping pour chaque source suivant une architecture commune selon le type de site
#On implémentera par la suite le traitement de Texte

def ScrapeHackerNews(company): 
    URL="https://thehackernews.com/"
    found=False
    page_counter=0
    
    mainpage=requests.get(URL)
    if(mainpage.ok): 
        soup=BeautifulSoup(mainpage.text, "lxml") #On scrape la première page
        anchors=soup.find_all('a')
        for a in anchors:
            if(a.get('href') != None): #On vérifie que le href n'est pas nul
                if (company in a.get('href')) or (company in a.text):
                    newpage=requests.get(a.get('href'))
                    newsoup=BeautifulSoup(newpage.text, "lxml")
                    for paragraph in newsoup.find_all('p'):
                        print(paragraph.text)
                    found=True
                    #webbrowser.open(a.get('href'))
        while(found==False and page_counter<2): #Tant que l'on a pas trouvé ou scrapé moins de 2 pages, on scrape la page suivante.
            nextpageURL=""
            for a in anchors: #Recherche de la page suivante
                anchor=str(a)
                if(("Next" in anchor) or ("next" in anchor) or ("Page" in anchor) or ("page" in anchor) or \
                  ("Older" in anchor) or ("older" in anchor) ):
                    if(a['href'].startswith("https://")):
                        nextpageURL=a['href']
            if(nextpageURL!=""):
                page_counter=page_counter+1
                nextpage=requests.get(nextpageURL)
                if nextpage.ok:
                    #webbrowser.open(nextpageURL)
                    soup=BeautifulSoup(nextpage.text, "lxml")
                    anchors=soup.find_all('a')
                    for a in anchors:
                        if(a.get('href') != None):
                            if (company in a.get('href')) or (company in a.text):
                                newpage=requests.get(a.get('href'))
                                newsoup=BeautifulSoup(newpage.text, "lxml")
                                for paragraph in newsoup.find_all('p'):
                                    print(paragraph.text)
                                #webbrowser.open(a.get('href'))
                                found=True
                else: #Requête page suivante échoue, on sort de la boucle
                    print("Request Failure: "+nextpageURL)
                    break
            else: #Pas de page suivante, on sort de la boucle
                break
        if(found==False):
            print("Could not scrape any information about "+ company+" on "+URL)
    else: #L'URL de base est invalide
        print("Request Failure: "+URL)


def ScrapeDarkReading(company): #Site à scroll infini
    print("Nothing for now.")

def ScrapeCesin(company): # :/!\ Redirection, login nécessaire
    URL="https://www.cesin.fr/alerteSecus.html"
    found=False
    page_counter=0

    mainpage=requests.get(URL) 
    if(mainpage.ok):
        soup=BeautifulSoup(mainpage.text, "lxml") #On scrape la première page
        anchors=soup.find_all('a')
        for a in anchors:
            if (company in a.get('href')) or (company in a.text):
                newpage=requests.get(a.get('href'))
                newsoup=BeautifulSoup(newpage.text, "lxml")
                for paragraph in newsoup.find_all('p'):
                    print(paragraph.text)
                found=True
                #webbrowser.open(a.get('href'))
        while(found==False and page_counter<2): #Tant que l'on a pas trouvé ou scrapé moins de 2 pages, on scrape la page suivante.
            nextpageURL=""
            for a in anchors:
                anchor=str(a)
                if("page-numbers" in anchor):
                    if(a['href'].startswith("https://")):
                        nextURL=a['href']
            if(nextpageURL!=""):
                page_counter=page_counter+1
                nextpage=requests.get(nextpageURL)
                if(nextpage.ok):
                    #webbrowser.open(nextpageURL)
                    soup=BeautifulSoup(nextpage.text, "lxml")
                    anchors=soup.find_all('a')
                    for a in anchors:
                        if (company in a.get('href')) or (company in a.text):
                            newpage=requests.get(a.get('href'))
                            newsoup=BeautifulSoup(newpage.text, "lxml")
                            for paragraph in newsoup.find_all('p'):
                                print(paragraph.text)
                            #webbrowser.open(a.get('href'))
                            found=True
                else: #Requête échoue, on sort de la boucle
                    print("Request Failure: "+nextpageURL)
                    break
            else: #Pas de page suivante, on sort de la boucle
                break
        if(found==False):
            print("Could not scrape any information about "+ company+" on "+URL)
    else: #L'URL de base est invalide
        print("Request Failure: "+URL)

def ScrapeZDnet(company): #Reconstrucrtion d'URL nécessaire
    URL="https://www.zdnet.com/blog/security/"
    found=False
    page_counter=0

    mainpage=requests.get(URL)
    if(mainpage.ok): 
        soup=BeautifulSoup(mainpage.text, "lxml") #On scrape la première page
        anchors=soup.find_all('a')
        for a in anchors:
            anchor_link=a.get('href')
            if(anchor_link != None): #On vérifie que le href n'est pas nul
                if(anchor_link.startswith("/")): #On le reconsitue si besoin
                    anchor_link=anchor_link[1:] #Pour enlever le "/"
                    anchor_link=URL+anchor_link #Et ensuite le concaténer avec l'URL de base
                if (company in anchor_link) or (company in a.text):
                    newpage=requests.get(anchor_link)
                    newsoup=BeautifulSoup(newpage.text, "lxml")
                    for paragraph in newsoup.find_all('p'):
                        print(paragraph.text)
                    found=True
                    #webbrowser.open(anchor_link)
        while(found==False and page_counter<2): #Tant que l'on a pas trouvé ou scrapé moins de 2 pages, on scrape la page suivante.
            nextpageURL=""
            for a in anchors:
                anchor=str(a)
                if("class=\"next\"" in anchor):
                    if(a['href'].startswith("https://")):
                        nextpageURL=a['href']
            if(nextpageURL!=""):
                page_counter=page_counter+1
                nextpage=requests.get(nextpageURL)
                if nextpage.ok:
                    #webbrowser.open(nextpageURL)
                    soup=BeautifulSoup(nextpage.text, "lxml")
                    anchors=soup.find_all('a')
                    for a in anchors:
                        anchor_link=a.get('href')
                        if(anchor_link != None):
                            if(anchor_link.startswith("/")): #On le reconsitue encore si besoin
                                anchor_link=anchor_link[1:]
                                anchor_link=URL+anchor_link
                            if (company in anchor_link) or (company in a.text):
                                newpage=requests.get(anchor_link)
                                newsoup=BeautifulSoup(newpage.text, "lxml")
                                for paragraph in newsoup.find_all('p'):
                                    print(paragraph.text)
                                #webbrowser.open(anchor_link)
                                found=True
                else: #Requête page suivante échoue, on sort de la boucle
                    print("Request Failure: "+nextpageURL)
                    break
            else: #Pas de page suivante, on sort de la boucle
                break
        if(found==False):
            print("Could not scrape any information about "+ company+" on "+URL)
    else: #L'URL de base est invalide
        print("Request Failure: "+URL)







def WebScraping(company): #Attention, la recherche est case sensitive! (exemple: Microsoft!=microsoft)
    #ScrapeHackerNews(company)
    #ScrapeCesin(company)
    ScrapeZDnet(company)


def main():
    #print("Hello World!") #Remplacer cette ligne par la fonction à executer.
    WebScraping("Lyceum")


main()

# PS: Lorsque vous voulez que votre code trouve un élément en particulier de la page, faire un clique droit -> inspecter pour trouver l'élément html correspondant 
# et utiliser soup.find("nom de l'élément"). Pour plus d'infos sur html https://developer.mozilla.org/fr/docs/Web/HTML/Element
# Si vous souhaitez enregistrer du code test sans risquer de détruire le code principal vous pouvez toujours créer une nouvelle branche séparée de la branche main et y téléverser votre code.
# (/!\ Lorsque vous changez de branche et revenez à la branche principale ne les fusionnez pas à moins d'être sûr de la validité du code ajouté!)