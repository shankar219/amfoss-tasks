import os
import telebot
import requests
import json
import csv


# TODO: 1.1 Get your environment variables 
yourkey = os.getenv('API_KEY')
bot_id = os.getenv('BOT_KEY')

bot = telebot.TeleBot('5797006355:AAFK8EzDfoJ6NgOuSSVeFTM_0LWtIVDrPvs')

@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    bot.reply_to(
        message, 'Hello there! I am a bot that will show movie information for you and export it in a CSV file.\n\n')
    
@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nHave a good time')
    "+title+"


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/movie MOVIE_NAME\" command to get the details of a particular movie. For eg: \"/movie The Shawshank Redemption\"\n\n2.0. You can use \"/export\" command to export all the movie data in CSV format.\n\n3.0. You can use \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['movie'])
def getMovie(message):
    bot.reply_to(message, 'getting movie info..')
    messageTxt = str(message.text)
    NameList = [x.strip() for x in messageTxt.split()]
    clearMovieName = ""
    for element in NameList[1:]: #starts after the /movie command
        clearMovieName = clearMovieName + element + "+" 
    clearMovieName = clearMovieName[:-1] #without the last + sign
    api = f'http://www.omdbapi.com/?t={clearMovieName}&apikey=<API-key>' #From http://www.omdbapi.com/
    #requesting the data of the movie from the website 
    movieDict = json.loads('text') #transforming it into a dictionary
    errorKey = 'Error' 
    if errorKey in movieDict.keys(): #cheking if the movie exists and that the website and API are working
        error = movieDict.get('Error')
        bot.send_message(message.chat.id, error)
    else:
        movie = movieDict.get('Title')
        year = movieDict.get('Year')
        director = movieDict.get('Director')
        genre = movieDict.get('Genre')
        ratingInternet = movieDict.get('Ratings')
        ratingTextDict = ratingInternet[0]
        ratingInternet2 = ratingTextDict.get('Value')
        photoUrl = movieDict.get('Poster')
        textToShow = "Movie name: " + movie + "\nYear: " + str(year) + "\nDirector: " + director + "\nGenre: " + genre + "\nInternet Rating: " + ratingInternet2 + "\n"
        bot.send_message(message.chat.id, textToShow) #sending to the chat (by chad id) the data on the movie
        bot.send_photo(message.chat.id, photo=photoUrl) #sending to the chat (by chad id) the poster of the movie
    
@bot.message_handler(func=lambda message: botRunning, commands=['export'])
def getList(message):
    global botRunning
    bot.reply_to(message, 'Generating file...')
    files = {"document" :open('movies_info.csv','r')}
    resp = requests.get('https://api.telegram.org/bot5797006355:AAFK8EzDfoJ6NgOuSSVeFTM_0LWtIVDrPvs/sendDocument?chat_id=1140639286', files=files)
    bot.reply_to(message, resp)    




@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')
    
bot.infinity_polling()
