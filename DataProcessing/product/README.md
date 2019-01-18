# Crawling Guide
by 영진

## 기본 골격
```python
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



### column 설정
1. name,
2. image, (메인이미지 * 색 개수)
3. category, (사이트 기준)
4. volume, 
5. originalPrice, getNumber(Regular Expression) 이용하여 숫자 추출
6. salePrice,
7. brand,
8. url, (대부분 1개)
9. color, (text)

