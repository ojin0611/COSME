# Crawling Guide
by 영진

## 기본 골격



```python
from bs4 import BeautifulSoup as bs # url, text를 얻어올 때 사용
from selenium import webdriver # url 접속이 불가능할때 사용 (click 등)
# import other_modules

read(siteURL)

categoryList = getCategoryList() # 카테고리별 링크 또는 클릭대상
for category in categoryList:
	read(category)
	itemList = getItemList() # item별 링크
	for item in itemList:
		read(item)
		result += getItem()

write(result)
```

### read(siteURL)
```python
# Mac, Windows에 따라 읽는 chromedriver가 다르다
path = 'chromedriver.exe' if (platform.system() == 'Windows') else '/Users/jg/Desktop/develop/DataTeam/DataProcessing/product/crawling/chromedriver';

driver = webdriver.Chrome(path)

url_home = 'http://www.home.url' # /blah/blah 형태로 url이 나오기 때문에 앞에 더해주기 위해 저장
url_prod = 'http://www.prod.url'
driver.get(url_prod)


```


### getCategoryList
```python

html = driver.page_source
soup = bs(html, 'html.parser')
categories = findFunction() # 사이트마다 다름
categoryList = [category.something for category in categories]

return categoryList
```

### getItemList
```python

html = driver.page_source
soup = bs(html, 'html.parser')
items = findFunction() # 사이트마다 다름
itemList = [item.something for item in items]

return itemList # list
```

### getItem
```python

html = driver.page_source
soup = bs(html, 'html.parser')


item['name'] = findName
item['image'] = findListOfImages # 상품 1개당 이미지 여러개인 가능성 + 색상 바뀔때 이미지 변경되는것 고려
item['category'] = findSiteCategory 
item['volume'] = findVolume
item['originalPrice'] = getNumber(findOriginalPrice)
item['salePrice'] = getNumber(findSalePrice)
item['brand'] = brandName # 수기입력
item['url'] = driver.current_url
item['color'] = findListOfColors # 색으로 상품 구분!

items.append(item)

return items # list형태

```

### write(result)
```python
output = json.dumps(result, ensure_ascii=False, indent='\t')

with open(output_name, 'w', encoding='UTF-8' as file):
	file.write(output)

return itemList # list
```

#### 자주 쓰는 BeautifulSoup 기능
```python
soup = bs(html,'html.parser') # bs에서 사용하기 위해 parsing
soup.find('tag',{'id':'id_of_tag'})
soup.find_all('tag',{'class':'class_name'})
tag.a['href']
tag.img['src']

```

#### 자주 쓰는 selenium 기능
```python
driver = webdriver.Chrome(path_chromedriver)  # 시작
driver.get(url) # url 접속
driver.page_source # 해당 페이지의 html 가져오기

driver.find_element_by_link_text(text)
driver.find_elements_by_class_name(class_name)
something.click()


```

#### column 설정
1. name,
2. image, (메인이미지 * 색 개수)
3. category, (사이트 기준)
4. volume, 
5. originalPrice, getNumber(Regular Expression) 이용하여 숫자 추출
6. salePrice,
7. brand,
8. url, (대부분 1개)
9. color, (text)

