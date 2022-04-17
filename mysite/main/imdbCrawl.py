import time
import os
import psycopg2
import datetime
import schedule
from bs4 import BeautifulSoup
from requests import get

# Connect to postgreSQL
conn = psycopg2.connect(
    host="ec2-54-209-221-231.compute-1.amazonaws.com",
    database="d45ml82v09ghlu",
    user="crzrodeqjnabav",
    password="73a195303f3caa3afd0a60471a7609b7f537dc73426923a68a1b3dd28288e8f3",
    port="5432")

print(conn)

cur = conn.cursor()

# Retrieve Movie Max ID 
print('Retrieve Movie Max ID ')
cur.execute('SELECT max(id) from main_movielist')
db_version = cur.fetchone()
print(db_version[0])

max_id = db_version[0]

# Retrieve Movie Records
print('Retrieve Movie Records ')
cur.execute('SELECT movie_name from main_movielist')
all_movie = cur.fetchall()
allMovieArray = []

for movie in all_movie:
    allMovieArray.append(movie[0])


# Define web url to crawl
url = 'https://www.imdb.com/movies-coming-soon/'
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')

# Search individual movie
movieArray = []
totalMovie = html_soup.select("td h4 a")
for movie in totalMovie:
    m = movie.get_text().lstrip()
    movieArray.append(m)
    
# Search category
categoryArray = []
category=html_soup.select("td p")
for cat in category:
    c = cat.get_text()
    #c = c.split('- ')[-1]
    c = c[c.find('-'):]
    c = c.replace(' ','')
    c = c.replace('\n','')
    c = c.replace('-  ','')
    c = c.replace(' | ','|')
    categoryArray.append(c)

# Search Image
imageArray = []
image=html_soup.find_all('img', class_ = 'poster shadowed')
for actual_image in image:
    imageArray.append(actual_image['src'])

# Generate insert statement
postgres_insert_query = "INSERT INTO main_movielist(date_release,id,movie_genre,movie_image_url,movie_name) VALUES (%s,%s,%s,%s,%s);"
b = 0

d = datetime.date.today()+ datetime.timedelta(days=30)

# Loop all crawled movie
while b < len(movieArray):

    # If movie found in master list, print message
    if movieArray[b] in allMovieArray:
        print('Movie exists')
    
    # Else, perform Insert statement
    else:
        print(movieArray[b])
        print('Inserting')
        max_id += 1
        print(max_id)
            
        record_to_insert = ('2022-'+'%02d' % d.month+'-01',max_id,categoryArray[b],imageArray[b],movieArray[b])
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
    b += 1

print('Done')

# Close connection
cur.close()
