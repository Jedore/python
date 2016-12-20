from urllib import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://hr.tencent.com/index.php')
soup = BeautifulSoup(html)

for i in soup.body.table.contents:
    if i%2 == 1:
        for j in soup.body.table.contents[i].
