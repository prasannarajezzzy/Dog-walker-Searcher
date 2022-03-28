import requests
from bs4 import BeautifulSoup
import re


def get_phone(soup,response):
    try:
        phone = soup.select("a[href*=callto]")[0].text
        return phone
    except:
        pass

    try:
        phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', response.text)[0]
        return phone
    except:
        pass

    try:
        phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', response.text)[-1]
        return phone
    except Exception as e:
        print ('Email not found',e)
        phone = ''
        return phone



def get_email(soup,response):
    try:
        email = re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', response.text)[-1]
        return email
    except:
        pass

    try:
        email = soup.select("a[href*=mailto]")[-1].text
    except Exception as e:
        print ('Email not found',e)
        email = ''
        return email

def companyName(query):
    # query="dog walker in delhi"
    query=query.replace(" ","+")
    page = requests.get("https://www.google.dz/search?q="+query)

    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    listOflinks=[]


    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        link_new = re.split(":(?=http)",link["href"].replace("/url?q=",""))
        print(link_new )
        if "google" not in link_new[0]:
            if ".in" in link_new[0]:
                listOflinks.append(link_new[0])
            elif ".com" in link_new[0]:
                listOflinks.append(link_new[0])
    dictList=[]
    for i in listOflinks:
        raw=i
        if "www" in i:
            raw = i.replace("www.",'')
        print(i)
        response = requests.get(i,verify= False)
        soup = BeautifulSoup(response.text, 'html.parser')
        mob=get_phone(soup,response)
        mail=get_email(soup,response)
        print("got data",mob,mail)
        raw = raw.replace("https://",'')
        lastIndex = raw.index(".")
        dictData = dict({
            "name":raw[:lastIndex],
            "link":i,
            "mobile":mob,
            "mail":mail
        })

        dictList.append(dictData)
    return dictList

# for url in listOflinks:
#     response = requests.get(url,verify= False)
#     print(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     print(get_phone(soup))



