Pearson Correlation Rating
Due to live database size, we are unable to import too much data from MovieLens into the system.
Hence, the Pearson Correlation (CF) performance might be a bit weak.

Things to take note before start Pearson Correalation (CF) testing,
1. For testing purpose, please sign up your account with DOB from Year 2017 to 2027
2. Please sign up your account with Gender Male
(The reason is because our database testing data, DOB for all users are DOB Year 2022 and Gender Male)

To perform Pearson Correlation (CF) testing,
1. Please sign up an account
2. Activate your account from mailbox
3. Login to your account
4. Click into the movie detail page
5. Select stars
6. Press on Rate button
7. Go back to home page
8. If you yet to see recommnded movie with Predicted Score in Recommended For You, repeat step 4 to step 7 for multiple times



Automation IMDB Movies Crawling
Files related: 
    1. mysite/main/clock.py
    2. mysite/main/imdbCrawl.py

Automation:
    1. Once a day
As Heroku server will go to Idle session if there is no user interact in the website.
Hence, the crawling might not run if the server is in Idle session. 
For testing purpose, we can set the automation crawling from once 1 day to every 2 minutes.
