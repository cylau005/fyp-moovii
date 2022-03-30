import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import pandas as pd
import psycopg2
from selenium.webdriver.common.by import By
import datetime
import schedule


from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def crawling():
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


    # Locate driver
    ##browser = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")
    S = Service("chromedriver.exe")
    browser = webdriver.Chrome(service=S)
    # Define web url to crawl
    url = 'https://www.imdb.com/movies-coming-soon/'

    # Activate driver
    browser.get(url)

    # Search individual movie
    movieDate=browser.find_elements(By.XPATH,'//h4[@class="l_group"]/a')

    # Search individual movie
    totalMovie=browser.find_elements(By.XPATH,'//td[@class="overview-top"]/h4/a')

    # Search category
    category=browser.find_elements(By.XPATH,'//td[@class="overview-top"]/p[@class="cert-runtime-genre"]')


    imageArray = []
    # Search Image
    image=browser.find_elements(By.XPATH,'//img[contains(@class,"shadowed")]')
    for actual_image in image:
        imageArray.append(actual_image.get_attribute('src'))

        
    # While loop add the finding to arrays
    i = 0
    movieArray = []
    categoryArray = []
    c = []
    while i < len(totalMovie):
        
        movieArray.append(totalMovie[i].text)
        categoryArray.append(category[i].text)
        
        # Remove unwanted text
        if "-" in categoryArray[i]:
            categoryArray[i] = categoryArray[i][categoryArray[i].find('-'):]
            categoryArray[i] = categoryArray[i].replace('-   ','')
            categoryArray[i] = categoryArray[i].replace(' | ','|')
            categoryArray[i] = categoryArray[i].replace(' | ','|')
            
        i += 1

    browser.quit()

    postgres_insert_query = "INSERT INTO main_movielist(date_release,id,movie_genre,movie_image_url,movie_name) VALUES (%s,%s,%s,%s,%s);"
    b = 0

    d = datetime.date.today()+ datetime.timedelta(days=30)

    while b < len(movieArray):
        if movieArray[b]in allMovieArray:
            print('Movie exists')
        else:
            print(movieArray[b])
            print('Inserting')
            max_id += 1
            print(max_id)
                
            record_to_insert = ('2022-'+'%02d' % d.month+'-01',max_id,categoryArray[b],imageArray[b],movieArray[b])
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
        b += 1

    print('inserted')


    cur.close()

# @sched.scheduled_job('cron', day_of_week='mon-sun', hour=12)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()


