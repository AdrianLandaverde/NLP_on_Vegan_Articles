import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import winsound

def make_noise():
  duration = 3000  # milliseconds
  freq = 440  # Hz
  winsound.Beep(freq, duration)


contenidos=[]
titulos=[]
ids=[]
errores=0
startTime= dt.datetime.now()
for i in range(1,1029):
    print("---------------------------------")
    page=requests.get("https://plantbasednews.org/all/page/"+str(i)+"/")
    soup= BeautifulSoup(page.text, "html.parser")
    posts= soup.find_all("figure")   
    links=[]
    for j in range(len(posts)-1):
        links.append(posts[j+1].a["href"])
    for j in links:
        try:
            page= requests.get(j)
            soup= BeautifulSoup(page.text, "html.parser")
            id1= soup.article["id"]
            titulo=soup.h1.text
            titulo=titulo.strip()
            contenido= soup.article.div.find_all("p")
            texto=""
            for k in range(len(contenido)):
                texto= texto+" " +contenido[k].text
            contenidos.append(texto.strip())
            titulos.append(titulo)
            ids.append(id1)
        except:
            errores+=1 
        print("Numer of articles scrapped: ",len(contenidos))
    print("Number of pages scrapped: ",i)
    print("Number of errors: ",errores)
    print("Time elapsed: " +str((dt.datetime.now())-startTime))
    print("---------------------------------")
    print(" ")
make_noise()
df= pd.DataFrame({"Id":ids, "Title":titulos, "Content":contenidos})
df.to_csv('articles_PlantBasedNews.csv',index=False, encoding="utf-8-sig")



