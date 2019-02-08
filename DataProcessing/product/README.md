# Crawling Guide
by 영진
## Output

### column  definition
1. name (상품명) text
   - 브랜드명 섞여있으면 제거
2. image (이미지 url) text
   - 메인이미지 + 색상 선택했을 때 이미지
3. category (사이트 기준) text
   - 예시 : 메이크업 > 포인트 메이크업 > 립 
4. volume (용량/사이즈) text
5. originalPrice (판매가) int
6. salePrice (할인가) int
7. brand (브랜드명) text
8. url (상품정보 url) text(url)
9. color (색상) text

## main

```python
from bs4 import BeautifulSoup as bs # url, text를 얻어올 때 사용
from selenium import webdriver # url 접속이 불가능할때 사용 (click 등)
# import other_modules

read(siteURL)

categoryList = getCategoryList() # 카테고리별 링크 또는 클릭대상
result = []
for category in categoryList:
	read(category)
	clickSeeMoreButton() # 더보기 클릭 필요할 때도 있다.
	itemList = getItemList() # item별 링크
	for item in itemList:
        read(item)
        result += getItem()

write(result)
```

## functions

### read(siteURL)
```python
# Mac, Windows에 따라 읽는 chromedriver가 다르다
path = 'chromedriver.exe' if (platform.system() == 'Windows') else '/Users/jg/Desktop/develop/DataTeam/DataProcessing/product/crawling/chromedriver';

driver = webdriver.Chrome(path)

url_home = 'http://www.home.url' # url이 보통 /blah/blah 형태로 나오기 때문에 앞에 더해주기 위해 저장
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

### clickSeeMoreButton() / clickNextPage()
```python
    # nextPage 버튼 클릭 시 상품목록이 바뀐다면, 무조건 3초를 기다리는게 아니라
    # 그 페이지에서 itemList를 얻고 기존 itemList에 이미 존재한다면 time.sleep(n), continue
    # js로 작성된 경우 페이지가 아직 바뀌지 않아서 html이 그대로일 수 있다.
    while True:
        try:
            seeMoreButton = driver.find_element_by_class_name(seeMoreButton)
            # button에 커서가 위치하지 않을수도 있고, 그 위치에 다른게 덮어써져있는경우도 있다. 이 때 커서 위치를 조정한다.
            # driver.execute_script('arguments[0].scrollIntoView(true);', target) # target이 보이도록 scroll하기
            seeMoreButton.click()
            time.sleep(3)
            
        except:
            break
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


## how to use modules

### BeautifulSoup
```python
soup = bs(html,'html.parser') # bs에서 사용하기 위해 parsing
soup.find('tag',{'id':'id_of_tag'})
soup.find_all('tag',{'class':'class_name'})
tag.a['href']
tag.img['src']
tag.parent
```

### selenium
```python
driver = webdriver.Chrome(path_chromedriver)  # 시작
driver.get(url) # url 접속
driver.page_source # 해당 페이지의 html 가져오기

driver.find_element_by_link_text(text)
driver.find_elements_by_class_name(class_name)
something.click()
driver.execute_script("window.scrollTo(0, 0)") # 페이지 맨 위로 올리기 
driver.execute_script('arguments[0].scrollIntoView(true);', target) # target이 보이도록 scroll하기



```


