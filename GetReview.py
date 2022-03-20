import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests, json
import pandas as pd

listHotel = [1370955, 5056732]
url = "https://www.agoda.com/api/cronos/property/review/ReviewComments"
Headers = { "Host" : "www.agoda.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Content-type": "application/json; charset=utf-8",
            "AG-Language-Locale": "vi-vn",
            "AG-Language-Id": "24",
            "CR-Currency-Id": "78",
            "CR-Currency-Code": "VND",
            "Content-Length": "227",
            "Origin": "https://www.agoda.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
            }
pageRange = 20
hotelInfo = {
    "hotelId": 1370955,
    "providerId": 332,
    "demographicId": 0,
    "page": 1,
    "pageSize":10,
    "sorting":5,
    "providerIds":[332],
    "isReviewPage": False,
    "isCrawlablePage": True,
    "filters":{"language":[24],"room":[]},
    "searchKeyword":"",
    "searchFilters":[]
}

filename="ReviewsAgoda.csv"
f=open(filename,"w", encoding = 'utf-8')
headers="Rating, Review\n"
f.write(headers)
frame=[]
upperframe=[]
for hotelId in listHotel:
    hotelInfo["hotelId"] = hotelId
    for pageId in range(1,pageRange):
        hotelInfo["page"] = pageId
        page = requests.post(url, headers = Headers, json = hotelInfo)
        body = json.loads(page.text)
        for comment in body["comments"]:
            rating = str(comment["rating"])
            print("Rating :" + rating)
            commentText = comment["reviewTitle"] + ". " + ". ".join(comment["reviewComments"].splitlines())
            commentText = commentText.replace(". .", ".")
            commentText = commentText.replace(". -", ".")
            commentText = commentText.replace(",","^")
            print("Review :" + commentText)
            frame.append([rating,commentText])
            f.write(rating + "," + commentText + "\n")
upperframe.extend(frame)
f.close()
data=pd.DataFrame(upperframe, columns=['Rating','Review'])
data.head()
