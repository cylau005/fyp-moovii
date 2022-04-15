from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import MovieList, RatingList, Reward_Point, PrizeList, CF_List
from register.models import Account
from .resources import MovieListResources, RatingListResources, RewardPointResources, PrizeListResources
from django.contrib import messages
from tablib import Dataset
from django.db.models import Sum
from django.views.generic.list import ListView
from .forms import RatingForm, AddMovieForm, AddRatingForm, DeleteRatingForm, MovieSearchForm, UserSearchForm, DeleteMovieForm
import string    
import random 
from django.contrib.auth.models import User
import datetime
from numpy import sqrt 
import math
# CF
import pandas as pd

# for CF related views
def movie_rating(request, id, user, user_score):  
    # print('a')
    movies = MovieList.objects.all()
    ratinglists = RatingList.objects.filter(action='Rate')

    print('Form Movie DF\n')
    # movie data frame
    m=[]
    mlist=[]
    for mv in movies:
        m=[mv.id, mv.movie_name, mv.movie_image_url]
        mlist+=[m]
    movie_DF = pd.DataFrame(mlist, columns=['movieId', 'movieName', 'movie_image_url'])

    print('Form Rating DF...\n')
    # rating data frame
    r=[]
    rlist=[]
    for rating in ratinglists:
        r=[rating.user_id.id, rating.movie_id, rating.rating_score]
        rlist+=[r]
    rating_DF = pd.DataFrame(rlist, columns=['userId', 'movieId', 'ratingScore'])
    print(rating_DF)

    chosen_MovieName = MovieList.objects.get(id=id)
    chosen_MovieName = chosen_MovieName.movie_name
    print(chosen_MovieName)
    
    print('Form User Input DF...\n')
    user_rating = [
        {'movieName': chosen_MovieName, 'ratingScore': int(user_score)}, # userId archie.carver, movieId 253
        # {'movieName': 'Braveheart (1995)', 'ratingScore': 5}, # userId archie.carver, movieId 253
        # {'movieName': 'In & Out (1997)', 'ratingScore':3}, # userId archie.carver, movieId 165
        # {'movieName': 'Toys (1992)', 'ratingScore':1}, # userId sulaiman.hopkins, movieId 208
        # {'movieName': 'Bedknobs and Broomsticks (1971)', 'ratingScore':5}, # userId sulaiman.hopkins, movieId 102
        # {'movieName': 'Star Wars: Episode IV - A New Hope (1977)', 'ratingScore':5}, 
        # {'movieName': 'Scary Movie (2000)', 'ratingScore':4}, 
    ]
    input_DF = pd.DataFrame(user_rating)
    print(input_DF)
    
    # Finding existing rating for current user
    user_Rating = RatingList.objects.filter(user_id=user)
    # chosen_MovieName = MovieList.objects.get(id=user_Rating.movie_id)
    for movie in user_Rating:
        print(movie.movie_id)
        movieName = MovieList.objects.get(id=movie.movie_id)
        print(movieName.movie_name)
        temp = pd.DataFrame({"movieName":[movieName.movie_name],
                             "ratingScore":[int(movie.rating_score)],
        })
        input_DF = input_DF.append(temp)

    print(input_DF)


    ID = movie_DF[movie_DF['movieName'].isin(input_DF['movieName'].tolist())]
    input_DF = pd.merge(ID, input_DF)

    print('Find movie name and id for Input DF...\n')
    print(input_DF)
    print()

    print('Find user who done rating on same movie...\n')
    users = rating_DF[rating_DF['movieId'].isin(input_DF['movieId'].tolist())]
    print(users)
    
    print(users.shape)
    print()

    userSubsetGroup = users.groupby(['userId'])

    print('Done GroupBy')
    
    userSubsetGroup = sorted(userSubsetGroup, key=lambda x:len(x[1]), reverse=True)    
    
    print('Done Sorted')
    print(userSubsetGroup)

    #Person correlation, where key is the user id and value is the coefficient
    pearsonCorDict = {}
    
    for name, group in userSubsetGroup:
        group = group.sort_values(by='movieId')
        input_DF = input_DF.sort_values(by='movieId')
        n = len(group)
        temp = input_DF[input_DF['movieId'].isin(group['movieId'].tolist())]
        tempRatingList = temp['ratingScore'].tolist()
        tempGroupList = group['ratingScore'].tolist()
        
        #calculating person correlation between two users, so called x and y
        Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(n)
        Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(n)
        Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(n)
        
        if Sxx != 0 and Syy != 0:
            pearsonCorDict[name] = Sxy/sqrt(Sxx*Syy)
        else:
            pearsonCorDict[name] = 0
        
        print(pearsonCorDict.items())
    

    pearsonDF = pd.DataFrame.from_dict(pearsonCorDict, orient='index')
    pearsonDF.columns = ['similarityIndex']
    pearsonDF['userId'] = pearsonDF.index
    pearsonDF.index = range(len(pearsonDF))
    
    # print(pearsonDF.head())

    topUsers = pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
    # print(topUsers.head())
    
    #rating of selected users to all movies
    topUsersRating = topUsers.merge(rating_DF, left_on='userId', right_on='userId', how='inner')
    print(topUsersRating[0:12])

    # #multiplies the similarity by the user's ratings
    topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * topUsersRating['ratingScore']
    # print(topUsersRating[0:12])

    print(topUsersRating)
    # #Applies a sum to the topUsers after grouping it up by userId
    tempTopUsersRating = topUsersRating.groupby('movieId').sum()[['similarityIndex','weightedRating']]
    tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
    print(tempTopUsersRating.head())

    # #Creates an empty dataframe
    recommendation_df = pd.DataFrame()

    #Now we take the weighted average
    recommendation_df['w.avg_score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
    print(1)
    recommendation_df['movieId'] = tempTopUsersRating.index
    print(2)
    print(recommendation_df)
    recommendation_df =  recommendation_df[recommendation_df['w.avg_score']>0]
    recommendation_df['w.avg_score'] = recommendation_df['w.avg_score'].astype(int)
    print(3)
    recommendation_df = recommendation_df.sort_values(by='w.avg_score', ascending=False)
    recommendation_df = recommendation_df.drop('movieId',1)
    print(recommendation_df)
    
    final = pd.merge(recommendation_df, movie_DF, on='movieId')
    
    final =  final[final['w.avg_score']>=3]
    print(final)

    user_Rating = RatingList.objects.filter(user_id=user)
    
    for a in user_Rating:
        final = final[final['movieId'] != a.movie_id]
        


    CF_List.objects.filter(user_id=user).delete()
    print('Old CF deleted')


    for ind in final.index:
        print(final['w.avg_score'][ind], final['movieName'][ind], final['movie_image_url'][ind])
        t = CF_List(user_id=user, movie_id=final['movieId'][ind], weighted_score=final['w.avg_score'][ind], movie_name=final['movieName'][ind], movie_image_url=final['movie_image_url'][ind])
        t.save()
    

def home(request):
    newmovies = MovieList.objects.all().order_by('-id')[:6]
    movies = MovieList.objects.filter(overall_rating__gte=5)
    genmovies = None
    if request.user.is_authenticated:
        user = request.user
        fav_genre = Account.objects.filter(user=user.id)
    
        if len(fav_genre) > 0:
            for g in fav_genre:
                gen=g.genres
                genmovies = MovieList.objects.filter(movie_genre__icontains=gen, overall_rating__gte=3)[:6]
        else:
            movies = MovieList.objects.all()[:6]

        cf_list = CF_List.objects.all()[:12]  

    else:
        cf_list = None
        
        
        
    if request.method == "POST":
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            movies_search = form.cleaned_data["movie_name"]
            movies_search_done = MovieList.objects.filter(movie_name__icontains=movies_search)
            
            if not movies_search_done:
                msg = 'No movie found'
                print(msg)
            else:
                movies = MovieList.objects.filter(movie_name__icontains=movies_search)
                msg = 'Please refer below'        
        return render(request, "main/home.html", {"movielist": movies, "newmovie":newmovies, "genmovies": genmovies, "form":form, "msg":msg})

    else:
        form = MovieSearchForm()
        movielist_form = MovieList()
    
    return render(request, "main/home.html", {"movielist": movies, "newmovie":newmovies, "genmovies": genmovies, "form":form, "cflist":cf_list})

def rating(request, id):    

    movie = MovieList.objects.get(id=id)
    genres = movie.movie_genre
    movieID = movie.id
    genresm = genres.replace('|',' | ')
    date = movie.date_release
    datem = date.year
    
    if request.user.is_authenticated:
        user = request.user
        cflist = CF_List.objects.filter(user_id=user.id, movie_id=id)
        
        if not len(cflist):
            print('No cf')
            cf_score = 'No predicted'
        else:
            for i in cflist:
                cf_score = i.weighted_score
        
        
        context= {
                'movie': movie,
                'movieyear':datem,
                'moviegenre':genresm,
                'movieID':movieID,
                'cf_score':cf_score,
                } 
    
    today = datetime.date.today()
    
    if 'actiontype' in request.POST:
        m = id
        a = request.POST['actiontype']

        rated_movie = RatingList.objects.filter(user_id=user, movie_id=id, action=a)
        num_rated_movie = len(rated_movie)

        if num_rated_movie < 1:                
            todayRateCount = RatingList.objects.filter(user_id=user, date_rating=today, action=a).count()

            if todayRateCount < 5:
                if a == "Rate":
                    s = request.POST['rating_score']
                    p = 2
                    movie_rating(request, id, user, s)

                else:
                    s = None
                    p = 3
                
                t = RatingList(user_id=user, rating_score=s, movie_id=m, action=a)
                r = Reward_Point(user_id=user, point=p)
                t.save()
                r.save()
                computeAvgRating(request, id)
                msg = a + ' successfully'
            
            else:
                msg = "You reached today limit, please try again tomorrow"
        
        else:
            if a == "Rate":
                s = request.POST['rating_score']
                rated_movie = RatingList.objects.filter(user_id=user, movie_id=id, action=a).update(rating_score=s)
                msg = a + ' successfully'
            else:
                rated_movie = RatingList.objects.filter(user_id=user, movie_id=id, action=a).update(date_rating=today)
                msg = a + ' successfully'
                    

        context= {
              'movie': movie,
              'movieyear':datem,
              'moviegenre':genresm,
              'msg':msg,
              'movieID':movieID,
              'cflist':cflist,
              }

        return render(request, "main/movie_detail.html", context)
        
    return render(request, "main/movie_detail.html", context)

def computeAvgRating(request, id):
    rated_movie_sum = RatingList.objects.filter(movie_id=id, action='Rate').aggregate(thedata=Sum('rating_score'))
    rated_movie_count = RatingList.objects.filter(movie_id=id, action='Rate').count()
    avg = rated_movie_sum['thedata'] / rated_movie_count
    roundAvg = int(math.ceil(avg))
    MovieList.objects.filter(id=id).update(overall_rating=roundAvg)
    print('Average Updated')


# default and profile views
def aboutus(response):
    return render(response, "main/aboutus.html", {})

def profile(response):
    user = response.user
    data = Reward_Point.objects.filter(user_id=user).aggregate(thedata=Sum('point'))
    prize = PrizeList.objects.all()
    reward = Reward_Point.objects.filter(user_id=user).order_by('-date_modified')
    prizeItem = PrizeList.objects.all()

    if 'prize_chosen' in response.POST:
        
        item = response.POST['prize_chosen']
        point = data['thedata']
        msg = ""

        if point is not None and point >= 1:    
            point = 0-1
            S = 30
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
            
            if item == '1':
                ran = 'MV-'+ran
                msg = 'Please do a screenshot and present it to the staff  \n\n' + ran
                
            if item == '2':
                ran = 'FD-'+ran
                msg = 'Please do a screenshot and present it to the staff  \n\n' + ran
                
            if item == '3':
                ran = 'One month subscription'
                msg = 'We will extend your subscription for one month'
                
            r = Reward_Point(user_id=user, point=point, redeem_item_id=item, code = ran)
            r.save()
            data = Reward_Point.objects.filter(user_id=user).aggregate(thedata=Sum('point'))
        
        else:
            msg = 'You do not have enough point'

        
        return render(response, "main/profile.html", {"data":data, "prize":prize, "prizeItem":prizeItem, "msg":msg, "reward":reward})
        
    else:
        error = "something wrong"

    return render(response, "main/profile.html", {"data":data, "prize":prize, "prizeItem":prizeItem, "reward":reward})

# admin views
def movie_upload(request):
    if request.method == 'POST':
        movie_resource = MovieListResources()
        dataset = Dataset()
        new_movie = request.FILES['myfile']

        if not new_movie.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'movie_upload.html')

        imported_data = dataset.load(new_movie.read(), format='xlsx')
        for data in imported_data:
            value = MovieList(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5]
            )
            value.save()
    return render(request, 'movie_upload.html')

def rating_upload(request):
    if request.method == 'POST':
        rating_resource = RatingListResources()
        dataset = Dataset()
        new_rating = request.FILES['myfile']

        if not new_rating.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'rating_upload.html')

        imported_data = dataset.load(new_rating.read(), format='xlsx')
        for data in imported_data:
            value = RatingList(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5]
            )
            value.save()
    return render(request, 'rating_upload.html')

def prize_upload(request):
    if request.method == 'POST':
        prize_resource = PrizeListResources()
        dataset = Dataset()
        new_prize = request.FILES['myfile']

        if not new_prize.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'prize_upload.html')

        imported_data = dataset.load(new_prize.read(), format='xlsx')
        for data in imported_data:
            value = RatingList(
                data[0],
                data[1],
                data[2]
            )
            value.save()
    return render(request, 'prize_upload.html')

def reward_point_upload(request):
    if request.method == 'POST':
        reward_point_resource = RewardPointResources()
        dataset = Dataset()
        new_rp = request.FILES['myfile']

        if not new_rp.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            return render(request, 'reward_point_upload.html')

        imported_data = dataset.load(new_rp.read(), format='xlsx')
        for data in imported_data:
            value = RatingList(
                data[0],
                data[1],
                data[2],
                data[3]
            )
            value.save()
    return render(request, 'reward_point_upload.html')

def movieListing(request): 
    movies = MovieList.objects.all().order_by('-id')

    if request.method == "POST":
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            movies_search = form.cleaned_data["movie_name"]
            movies_search_done = MovieList.objects.filter(movie_name__icontains=movies_search)
            
            if not movies_search_done:
                msg = 'No movie found'
                print(msg)
            else:
                movies = MovieList.objects.filter(movie_name__icontains=movies_search)
                msg = 'Please refer below'
        
        return render(request, "main/movie_listing.html", {"movielist": movies,"form":form, "msg":msg})

    else:
        form = MovieSearchForm()
        movielist_form = MovieList()

        
    return render(request, "main/movie_listing.html", {"movielist": movies,"form":form})

def movieListingAdd(request):
    movie_id = MovieList.objects.latest('id').id
    latest_id = movie_id + 1
    
    if request.method == "POST":
        form = AddMovieForm(request.POST)
        if form.is_valid():
            i = latest_id
            n = form.cleaned_data["movie_name"]
            g = form.cleaned_data["movie_genre"]
            a = form.cleaned_data["overall_rating"]
            d = form.cleaned_data["date_release"]
            u = form.cleaned_data["movie_image_url"]

            movie_check = MovieList.objects.filter(id=i)
            print(movie_check)
            if not movie_check:
                t = MovieList(id=i, movie_name=n, movie_genre=g, overall_rating=a, date_release=d, movie_image_url=u)
                msg = "Movie added"
                t.save()
            else:
                msg = "ID exists. Please try with other ID"
                
        
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/movie_listing_add.html", {"form":form, "msg":msg})
        
    else:
        form = AddMovieForm()
        add_movie_form = MovieList()
    
    return render(request, "main/movie_listing_add.html", {"form":form})

def movieListingDelete(request):
    if request.method == "POST":
        form = DeleteMovieForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["movie_name"]
            print(s)
            movie_check = MovieList.objects.filter(movie_name=s)
            
            if not movie_check:
                msg = 'Movie not exists'
            else:
                MovieList.objects.filter(movie_name=s).delete()
                msg = "Movie deleted"
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/movie_listing_delete.html", {"form":form,"msg":msg})
        
    else:
        form = DeleteMovieForm()
        delete_movie_form = MovieList()
    
    return render(request, "main/movie_listing_delete.html", {"form":form})

def rateListing(request):
    ratings = RatingList.objects.all().order_by('-id')
    return render(request, "main/rate_listing.html", {"ratelist": ratings})

def rateListingAdd(request):
    if request.method == "POST":
        form = AddRatingForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["rating_score"]
            m = form.cleaned_data["movie_id"]
            a = form.cleaned_data["action"]
            u = form.cleaned_data["user_id"]
            user_check = User.objects.filter(username=u)
            print(user_check)

            if a == "Rate":
                p = 2
            else:
                p = 3
                s = None
            
            if not user_check:
                msg = 'User not exists'
                print(msg)

            else:
                user = User.objects.get(username=u)
                t = RatingList(user_id=user, rating_score=s, movie_id=m, action=a)
                r = Reward_Point(user_id=user, point=p)
                t.save()
                r.save()

                msg = "Rating added"
                print(msg)
            
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/rate_listing_add.html", {"form":form,"msg":msg})
        
    else:
        form = AddRatingForm()
        add_movie_form = RatingList()
    
    return render(request, "main/rate_listing_add.html", {"form":form})

def rateListingDelete(request):
    if request.method == "POST":
        form = DeleteRatingForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["id"]
            print(s)
            rating_check = RatingList.objects.filter(id=s)
            
            if not rating_check:
                msg = 'Rating not exists'

            else:
                RatingList.objects.filter(id=s).delete()
                msg = "Rating deleted"
            
        else:
            msg = "Please check if you field in correctly"
            
        return render(request, "main/rate_listing_delete.html", {"form":form,"msg":msg})
        
    else:
        form = DeleteRatingForm()
        delete_movie_form = RatingList()
    
    return render(request, "main/rate_listing_delete.html", {"form":form})

def userListing(request):
    users = User.objects.all()
    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            username_search_done = User.objects.filter(username__icontains=username)
            
            if not username_search_done:
                msg = 'No user found'
                print(msg)
            else:
                users = User.objects.filter(username__icontains=username)
                msg = 'Please refer below'
        
        return render(request, "main/user_listing.html", {"userlist": users,"form":form, "msg":msg})

    else:
        form = UserSearchForm()
        user_form = User()

    return render(request, "main/user_listing.html", {"userlist": users, "form":form})

def userBlacklist(request):
    if request.method == "POST":
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            username_search_done = User.objects.filter(username=username)
            
            if not username_search_done:
                msg = 'No user found'
                print(msg)
            else:
                users = User.objects.get(username=username)
                print(users)
                users.is_active = False
                users.save()
                msg = 'User blacklisted'
        
        return render(request, "main/user_blacklist.html", {"form":form, "msg":msg})

    else:
        form = UserSearchForm()
        user_form = User()

    return render(request, "main/user_blacklist.html", {"form":form})

