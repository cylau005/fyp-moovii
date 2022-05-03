from urllib import request
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import MovieList, RatingList, Reward_Point, PrizeList, CF_List, Interact_List
from .resources import MovieListResources, RatingListResources, RewardPointResources, PrizeListResources
from .forms import RatingForm, AddMovieForm, AddRatingForm, DeleteRatingForm, MovieSearchForm, UserSearchForm, DeleteMovieForm
from register.models import Account
from tablib import Dataset
import string    
import random 
import datetime
from numpy import sqrt 
import math
import pandas as pd

# CF Approach - Pearson Correlation
def cf_approach(request, id, user, user_score):  
    
    # CF take similar user who has the similar birthday Year (+5 or -5) as well
    dob = Account.objects.get(user=user.id)
    myyear = dob.dob.year

    sameBirth = Account.objects.filter(dob__year__range=[myyear-5, myyear+5])
    sameBirthId = []
    for i in sameBirth:
        sameBirthId.append(i.id)

    # Get all the movie
    movies = MovieList.objects.all()

    # Get all the rating related Rate action
    ratinglists = RatingList.objects.filter(user_id__in=sameBirthId, action='Rate')
    

    # Form master movie list dataframe
    m=[]
    mlist=[]
    for mv in movies:
        m=[mv.id, mv.movie_name, mv.movie_image_url]
        mlist+=[m]
    movie_DF = pd.DataFrame(mlist, columns=['movieId', 'movieName', 'movie_image_url'])

    # Form rating list dataframe
    r=[]
    rlist=[]
    for rating in ratinglists:
        r=[rating.user_id.id, rating.movie_id, rating.rating_score]
        rlist+=[r]
    rating_DF = pd.DataFrame(rlist, columns=['userId', 'movieId', 'ratingScore'])
    
    # Get movieID and movieName based on user rated
    chosen_MovieName = MovieList.objects.get(id=id)
    chosen_MovieName = chosen_MovieName.movie_name

    # Form dataframe based on what user has rated
    user_rating = [
        {'movieName': chosen_MovieName, 'ratingScore': int(user_score)}, 
    ]
    input_DF = pd.DataFrame(user_rating)
    
    # Finding all the movies has rated by the user
    user_Rating = RatingList.objects.filter(user_id=user, action='Rate')
    
    # Append all the movies has rated by the user into dataframe
    for movie in user_Rating:
        print(movie.movie_id)
        movieName = MovieList.objects.get(id=movie.movie_id)
        print(movieName.movie_name)
        temp = pd.DataFrame({"movieName":[movieName.movie_name],
                             "ratingScore":[int(movie.rating_score)],
        })
        input_DF = input_DF.append(temp)

    # Filter the master movie list based on user's rated movies. and Merge the table together
    ID = movie_DF[movie_DF['movieName'].isin(input_DF['movieName'].tolist())]
    input_DF = pd.merge(ID, input_DF)

    print('Merged movie list.\n')
    print(input_DF)

    # Find all users who done rating on same movie
    users = rating_DF[rating_DF['movieId'].isin(input_DF['movieId'].tolist())]
    print(users)
    
    # Group by to userId avoid duplicate
    userSubsetGroup = users.groupby(['userId'])

    # Sort the user based on most common movie
    userSubsetGroup = sorted(userSubsetGroup, key=lambda x:len(x[1]), reverse=True)    
    print(userSubsetGroup)
    
    print(len(userSubsetGroup))
    if len(userSubsetGroup) > 0:
    
        # Pearson correlation approach
        PCDict = {}
        
        for name, group in userSubsetGroup:
            group = group.sort_values(by='movieId')
            input_DF = input_DF.sort_values(by='movieId')
            n = len(group)
            temp = input_DF[input_DF['movieId'].isin(group['movieId'].tolist())]
            tempInputDFList = temp['ratingScore'].tolist()
            tempGroupList = group['ratingScore'].tolist()
            
            # Calculating pearson correlation between two users, so called userX and userY
            userX = sum([i**2 for i in tempInputDFList]) - pow(sum(tempInputDFList), 2) / float(n)
            userY = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList), 2) / float(n)
            userXY = sum( i*j for i, j in zip(tempInputDFList, tempGroupList)) - sum(tempInputDFList) * sum(tempGroupList) / float(n)
            
            # Avoid 0
            if userX != 0 and userY != 0:
                PCDict[name] = userXY / sqrt(userX * userY)
            else:
                PCDict[name] = 0
        
        pearsonDF = pd.DataFrame.from_dict(PCDict, orient='index')

        # Forming similarity index
        pearsonDF.columns = ['similarityIndex']
        pearsonDF['userId'] = pearsonDF.index
        pearsonDF.index = range(len(pearsonDF))
        
        topUsers = pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
        
        # Merging the table between all top user and master rating list by inner join
        topUsersRating = topUsers.merge(rating_DF, left_on='userId', right_on='userId', how='inner')
        print(topUsersRating[0:12])
        

        # Calculate similarity index
        topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * topUsersRating['ratingScore']
        print('Top User Rating:')
        print(topUsersRating)

        # Sum similarityIndex and WeightedRating
        tempTopUsersRating = topUsersRating.groupby('movieId').sum()[['similarityIndex','weightedRating']]
        tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
        print(tempTopUsersRating.head())

        # Creates new dataframe
        recommendation_df = pd.DataFrame()

        # Compute weighted average score
        recommendation_df['w.avg_score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
        recommendation_df['movieId'] = tempTopUsersRating.index
        
        # Filter weighted average score greater than 0 and make it integer
        recommendation_df =  recommendation_df[recommendation_df['w.avg_score']>0]
        recommendation_df['w.avg_score'] = recommendation_df['w.avg_score'].astype(int)
        recommendation_df = recommendation_df.sort_values(by='w.avg_score', ascending=False)
        recommendation_df = recommendation_df.drop('movieId',1)
        print(recommendation_df)
        
        # Merged recommendation dataframe and master movie list to get neccessary data
        # Do not include the movie which has just done rated
        final = pd.merge(recommendation_df, movie_DF, on='movieId')
        final = final[final['movieId'] != id]
        
        # Only recommend the movie if weighed average score is equal or greater than 3
        final =  final[final['w.avg_score']>=3]

        # Get all the rating done by the user
        user_Rating = RatingList.objects.filter(user_id=user, action='Rate')
        
        # Filter rated movie from the final dataframe so it won't recommend same movie to user
        for a in user_Rating:
            final = final[final['movieId'] != a.movie_id]

        # Remove rated movie from the final dataframe so it won't recommend same movie to user
        CF_List.objects.filter(user_id=user).delete()
        print('Old CF deleted')

        # Save final recommended movie list into CF_List model
        for ind in final.index:
            print(final['w.avg_score'][ind], final['movieName'][ind], final['movie_image_url'][ind])
            t = CF_List(user_id=user, movie_id=final['movieId'][ind], weighted_score=final['w.avg_score'][ind], movie_name=final['movieName'][ind], movie_image_url=final['movie_image_url'][ind])
            t.save()
    
# Function for homepage
def home(request):
    
    # Get top 6 new movies
    newmovies = MovieList.objects.all().order_by('-id')[:6]

    # Get movie which has max rating
    movies = MovieList.objects.filter(overall_rating__gte=5).order_by('?')
    
    # Custom variable
    genmovies = None
    intMovie = None
    select_genre_done = None
    msg = ''

    # If is registered viewer
    if request.user.is_authenticated:

        user = request.user

        # Get register viewer's favourite genre
        fav_genre = Account.objects.filter(user=user.id)

        # Get similar genre movies based on your last visit of the movie detail page
        intMovie = Interact_List.objects.filter(user_id=user).order_by('?')[:6]

        # If favourite genre found, filter 6 movies that related to the genre 
        # and overall rating is equal or greater than 3
        if len(fav_genre) > 0:
            for g in fav_genre:
                gen=g.genres
                genmovies = MovieList.objects.filter(movie_genre__icontains=gen, overall_rating__gte=3).order_by('?')[:6]
        
        # Else, get all movies
        else:
            movies = MovieList.objects.all().order_by('?')

        # Get 12 movies from CF List
        cf_list = CF_List.objects.filter(user_id=user).order_by('?')[:12]  

    # Else, no CF List
    else:
        cf_list = None
    
    # Individual Movies after Genre filter selected
    genre_list = ''
    movie = MovieList.objects.values_list("movie_genre", flat=True).distinct()
    for i in movie:
        genre_list = genre_list + '|' + i
    split_genre = genre_list.split('|')
    split_genre = list(dict.fromkeys(split_genre))
    split_genre = list(filter(None, split_genre))

    # Form for movie search and genre filter
    if request.method == "POST":
        # Movie search function
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

        if 'movie_genre' in request.POST:
            select_genre = request.POST['movie_genre']
            select_genre_done = MovieList.objects.filter(movie_genre__icontains=select_genre).order_by('?')
            movies = select_genre_done 
    else:
        form = MovieSearchForm()
        movielist_form = MovieList()
    
    context = {"movielist": movies, 
                "newmovie":newmovies, 
                "genmovies": genmovies, 
                "form":form, 
                "cflist":cf_list, 
                "msg":msg,
                "intMovie":intMovie,
                "split_genre":split_genre,
    }
    
    return render(request, "main/home.html", context)

# Function for Rating 
def rating(request, id):    
    
    # Get movie detail for the selected movie
    movie = MovieList.objects.get(id=id)
    genres = movie.movie_genre
    movieID = movie.id
    genresm = genres.replace('|',' | ')

    # Get individual genre for the selected movie
    split_genre = genres.split('|')
    split_genre = list(dict.fromkeys(split_genre))
    split_genre = list(filter(None, split_genre))

    # Set variable
    date = movie.date_release
    datem = date.year
    cf_score = ''
    cflist = ''
    msg = ''
    today = datetime.date.today()
    openShare = 'none'

    # If user is a registered viewer, get the predicted rating for that user and movie if available
    # If user is a registered viewer, everytime user visit the movie detail page in the website, 
    #                                 it should show relevant movies next time
    if request.user.is_authenticated:
        user = request.user

        # Getting all movie from Pearson Correlation approach
        cflist = CF_List.objects.filter(user_id=user.id, movie_id=id)

        # Create a list in order to exclude CF Movie from Interact Movie list
        cflistMovie = []
        for i in cflist:
            cflistMovie.append(i.movie_id)
        

        # Getting all high rated movies that related to the movie genre you have visited
        intMovie = MovieList.objects.filter(movie_genre__in=split_genre, overall_rating__gte=3). \
                    exclude(id__in=cflistMovie).order_by('?')[:6]
        
        # Delete the current relevant movie you might like
        Interact_List.objects.filter(user_id=user).delete()

        # Insert latest relevant movies that you visited in the last movie detail page
        for i in intMovie:
            intMovie_Save = Interact_List(user_id=user, movie_id=i.id, 
                                    movie_name=i.movie_name, movie_image_url = i.movie_image_url)
            intMovie_Save.save()
        
        if not len(cflist):
            cf_score = 'No predicted'
        else:
            cf_score = cflist.values_list('weighted_score', flat=True)[0]
            print(cf_score)
        

        
    # Rating form
    if 'actiontype' in request.POST:
        m = id
        a = request.POST['actiontype']
        
        # Get number of rating or sharing done by the user to particular movie
        rated_movie = RatingList.objects.filter(user_id=user, movie_id=id, action=a)
        num_rated_movie = len(rated_movie)
        
        # If no record found, add new record
        if num_rated_movie < 1:             
            
            # Check how many rating or sharing done by the user on the same day   
            todayRateCount = RatingList.objects.filter(user_id=user, date_rating=today, action=a).count()

            # If less than 5 time, add new record
            if todayRateCount < 5:
                
                # If is rating, earn 2 reward point
                if a == "Rate":

                    # If got star and user press on Rate button
                    if 'rating_score' in request.POST:
                        s = request.POST['rating_score']
                        p = 2

                        
                        cf_approach(request, m, user, s)
                    
                    # If no star selected and user press on Rate button, prompt message 
                    else:
                        msg = 'Please select a star'

                # If is sharing, earn 3 reward point
                else:
                    openShare = 'block'
                    s = None
                    p = 3
                
                # If is rating or sharing, add record and compute movie rating average
                if a == "Share" or (a == "Rate" and 'rating_score' in request.POST):
                    t = RatingList(user_id=user, rating_score=s, movie_id=m, action=a)
                    r = Reward_Point(user_id=user, point=p)
                    t.save()
                    r.save()
                    computeAvgRating(request, id)
                    msg = a + ' successfully'

                
            # Else, print error message
            else:
                msg = "You reached today limit, please try again tomorrow"
        
        # Else, update record, and no new reward point earn
        else:
            if a == "Rate":
                if 'rating_score' in request.POST:
                    s = request.POST['rating_score']
                    rated_movie = RatingList.objects.filter(user_id=user, movie_id=id, action=a).update(rating_score=s)
                    msg = a + ' successfully'
                else:
                    msg = 'Please select a star'
            else:
                openShare = 'block'
                rated_movie = RatingList.objects.filter(user_id=user, movie_id=id, action=a).update(date_rating=today)
                msg = a + ' successfully'

    context= {
            'movie': movie,
            'movieyear':datem,
            'moviegenre':genresm,
            'msg':msg,
            'movieID':movieID,
            'cflist':cflist,
            'cf_score':cf_score,
            'openShare':openShare,
            }
        
    return render(request, "main/movie_detail.html", context)

# Compute average score for the movie
def computeAvgRating(request, id):
    
    # Sum all the rating from the RatingList model for particular movie
    rated_movie_sum = RatingList.objects.filter(movie_id=id, action='Rate').aggregate(thedata=Sum('rating_score'))

    # Count number of record all the rating from the RatingList model for particular movie
    rated_movie_count = RatingList.objects.filter(movie_id=id, action='Rate').count()

    # Count average
    avg = rated_movie_sum['thedata'] / rated_movie_count

    # Round up
    roundAvg = int(math.ceil(avg))

    # Update model
    MovieList.objects.filter(id=id).update(overall_rating=roundAvg)
    print('Average Updated')


# Function for About Us page
def aboutus(response):
    return render(response, "main/aboutus.html", {})

# Function for Profile page
def profile(response):
    
    # Find the userID and sum all the reward point available for the user
    user = response.user
    data = Reward_Point.objects.filter(user_id=user).aggregate(thedata=Sum('point'))

    # Get all prizes
    prize = PrizeList.objects.all()

    # Get all reward point history
    reward = Reward_Point.objects.filter(user_id=user).order_by('-id')
    
    # Custom variable
    msg = ''

    # Form for prize redeem
    if 'prize_chosen' in response.POST:
        
        item = response.POST['prize_chosen']
        point = data['thedata']
        msg = ""
        
        # Get required point for the selected prize
        chosenPrizeID = PrizeList.objects.get(pk=item)
        rp_PrizeItem = PrizeList.objects.filter(pk=item).values_list('require_points', flat=True)[0]
        
        # If available point for user and available point is greater than prize's required point
        if point is not None and point >= rp_PrizeItem:    
            
            # Redeem prize and deduct point
            point = 0-rp_PrizeItem

            # Generate redemption code with a prefix and 30 digits random alphanumeric
            S = 30
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
            
            # If is Movie Voucher
            if item == '1':
                ran = 'MV-'+ran
                msg = 'Please do a screenshot and present it to the staff  \n\n' + ran
            
            # If is Cinema Food Voucher
            if item == '2':
                ran = 'FD-'+ran
                msg = 'Please do a screenshot and present it to the staff  \n\n' + ran
                
            # If is one month subscription
            if item == '3':
                ran = 'One month subscription'
                msg = 'We will extend your subscription for one month'
            
            r = Reward_Point(user_id=user, point=point, redeem_item_id=chosenPrizeID, code = ran)
            r.save()
            data = Reward_Point.objects.filter(user_id=user).aggregate(thedata=Sum('point'))
        
        # Else, if not enough point, print message
        else:
            msg = 'You do not have enough point'
        
    else:
        error = "something wrong"

    context = {"data":data, 
                "prize":prize,  
                "reward":reward,
                "msg": msg
    }

    return render(response, "main/profile.html", context)


# Function for MovieList(Admin) page
def movieListing(request): 

    # Get all movie and sort descending
    movies = MovieList.objects.all().order_by('-id')
    msg = ''

    # Search movie
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

    else:
        form = MovieSearchForm()
        movielist_form = MovieList()

    context = {"movielist": movies,
                "form":form,
                "msg":msg
    }
        
    return render(request, "main/movie_listing.html", context)

# Function for admin to add movie manually in frontend
def movieListingAdd(request):

    # Get maxID + 1
    movie_id = MovieList.objects.latest('id').id
    latest_id = movie_id + 1
    msg = ''

    # Get required information from the form
    if request.method == "POST":
        form = AddMovieForm(request.POST)
        if form.is_valid():
            i = latest_id
            n = form.cleaned_data["movie_name"]
            g = form.cleaned_data["movie_genre"]
            a = form.cleaned_data["overall_rating"]
            d = form.cleaned_data["date_release"]
            u = form.cleaned_data["movie_image_url"]

            # If no existing movie found , add new record
            movie_check = MovieList.objects.filter(id=i)
            movie_name_check = MovieList.objects.filter(movie_name=n)
            print(movie_check)
            if not movie_check or not movie_name_check:
                t = MovieList(id=i, movie_name=n, movie_genre=g, overall_rating=a, date_release=d, movie_image_url=u)
                msg = "Movie added"
                t.save()
            else:
                msg = "Movie exists. Please try with other movie name"
                
        else:
            msg = "Please check if you fill in correctly"
            
    else:
        form = AddMovieForm()
        add_movie_form = MovieList()
    
    context = {"form":form, 
                "msg":msg
    }
    
    return render(request, "main/movie_listing_add.html", context)

# Function for admin to delete movie manually in frontend
def movieListingDelete(request):
    msg = ''

    # Form
    if request.method == "POST":
        form = DeleteMovieForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["movie_name"]
            print(s)
            movie_check = MovieList.objects.filter(movie_name=s)
            
            # If no movie name found, then print message
            if not movie_check:
                msg = 'Movie not exists'

            # If movie name found, then delete movie
            else:
                MovieList.objects.filter(movie_name=s).delete()
                msg = "Movie deleted"
        else:
            msg = "Please check if you fill in correctly"
                    
    else:
        form = DeleteMovieForm()
        delete_movie_form = MovieList()
    
    context = {"form":form, 
                "msg":msg
    }

    return render(request, "main/movie_listing_delete.html", context)

# Function for RatingList(Admin) page
def rateListing(request):
    ratings = RatingList.objects.all().order_by('-id')
    context = {"ratelist": ratings
    }
    return render(request, "main/rate_listing.html", context)

# Function for admin to add rating on behalf of customer manually
def rateListingAdd(request):
    msg = ''

    # Get required data from the form
    if request.method == "POST":
        form = AddRatingForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["rating_score"]
            m = form.cleaned_data["movie_id"]
            u = form.cleaned_data["user_id"]

            user_check = User.objects.filter(username=u)
            print(user_check)

            # Prefixed as Rate action and earn 2 points
            # Because admin do not has access to customer's social media
            a = "Rate"
            p = 2
            
            # If user not found, print message
            if not user_check:
                msg = 'User not exists'
                print(msg)

            # Else, add record
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

# Function for admin to delete rating based on rating ID
def rateListingDelete(request):
    msg = ''
    if request.method == "POST":
        form = DeleteRatingForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data["id"]
            print(s)
            rating_check = RatingList.objects.filter(id=s)
            
            # If ratingID not found, print message
            if not rating_check:
                msg = 'Rating not exists'
            
            # Else, delete record
            else:
                RatingList.objects.filter(id=s).delete()
                msg = "Rating deleted"
            
        else:
            msg = "Please check if you field in correctly"
                    
    else:
        form = DeleteRatingForm()
        delete_movie_form = RatingList()
    
    context = {"form":form, 
                "msg":msg
    }

    return render(request, "main/rate_listing_delete.html", context)

# Function for UserListing(Admin) page
def userListing(request):
    
    msg = ''
    users = User.objects.all()

    # Form for search User function by username
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

    else:
        form = UserSearchForm()
        user_form = User()

    context = {"userlist": users,
                "form":form, 
                "msg":msg
    }

    return render(request, "main/user_listing.html", context)

# Function for blacklist user from frontend
def userBlacklist(request):
    msg = ''
    if request.method == "POST":
        form = UserSearchForm(request.POST)

        # Blacklist based on username
        if form.is_valid():
            username = form.cleaned_data["username"]
            username_search_done = User.objects.filter(username=username)
            
            # If no user found, print message
            if not username_search_done:
                msg = 'No user found'
                print(msg)
            
            # Else, update user as inactive
            else:
                users = User.objects.get(username=username)
                print(users)
                users.is_active = False
                users.save()
                msg = 'User blacklisted'
    else:
        form = UserSearchForm()
        user_form = User()

    context = {"form":form, 
                "msg":msg
    }

    return render(request, "main/user_blacklist.html", context)


# Function for backend admin to upload movie
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

# Function for backend admin to upload rating
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

# Function for backend admin to upload prize
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

# Function for backend admin to upload reward point
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
