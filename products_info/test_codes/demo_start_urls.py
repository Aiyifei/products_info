
start_urls = ['https://search.jd.com/Search?keyword=iphone&page={}'.format(i) for i in range(0, 202, 2)]

print(start_urls)

for url in start_urls:
    print(url)