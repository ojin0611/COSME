# Crawling Guide
by 영진

## 기본 골격
```python
read(siteURL)

categoryList = getCategoryList() # 카테고리별 링크
for category in categoryList:
	category.click()
	items = getItems() # item별 링크
	for item in items:
		item.click()
		result += getItem()

write(result)
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

