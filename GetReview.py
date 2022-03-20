import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests, json, re
import pandas as pd

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

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
            commentText = deEmojify(commentText)
            print("Review :" + commentText)
            frame.append([rating,commentText])
            f.write(rating + "," + commentText + "\n")
upperframe.extend(frame)
f.close()
data=pd.DataFrame(upperframe, columns=['Rating','Review'])
data.head()
