
import requests
import json

url=" https://roark.com/products/mens-bless-up-breathable-stretch-shirt-fossil-print"

api_url = url + ".js"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/151.0.0.0 Safari/537.36"
}
datas=[]
res=requests.get(api_url,headers=headers,timeout=10)

data=res.json()

name = data["title"]
price = data["price"] / 100
images = data["images"]

variants = data["variants"]
color = variants[0]["option1"]
sizes = []
for item in variants:
    size = item["option2"]

    sizes.append(size)

result = {
        "name": name,
        "price": price,
        "image": images,
        "variants": sizes,
        "color": color,
        "sizes": sizes
    }
datas.append(result)
print(datas)

