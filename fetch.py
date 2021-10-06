Url = "https://www.imdb.com/chart/top/"

web = requests.get(Url)

soup = BeautifulSoup(web.content, "html.parser")

print(soup.prettify())

titleClass = soup.find_all("td" , class_= "titleColumn")

titles = []
for tag in titleClass:
  link = tag.find_all("a" , href = True)

  for tag in link:
    titles.append(tag.text)

ratingClass = soup.find_all("td" , class_="ratingColumn")

ratings = []
for tag in ratingClass:
  rating = tag.find_all("strong")

  for j in rating:
    ratings.append(float(j.text))

import pandas as pd
data = pd.DataFrame(zip(name , ratings),
                    columns = ["Name" , "Ratings"])

data.head(10)
