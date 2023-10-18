from pyrogram import Client, filters
import requests

# Initialize your Pyrogram API ID and API HASH
API_ID = "950903"
API_HASH = "69d37ae7fdf5154293b01434044c37dd"
TOKEN = "6230370760:AAFx2IL5HpXA3PEeaGVmtK2R9cYTuhO4VP0"
TMDB_API_KEY = "81cc1df77fb33a00b3b88dc5c3a26afe"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

@app.on_message(filters.command("start"))
def start(bot, update):
    bot.send_message(update.chat.id, "Welcome to the TV Show Info Bot! Send me the name of a TV show to get information.")

@app.on_message(filters.command("showinfo"))
def show_info(bot, update):
    show_name = " ".join(update.text.split()[1:])  # Extract the show name from the user's message
    response = requests.get(f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={show_name}")
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            show = data['results'][0]
            title = show['name']
            overview = show['overview']
            release_date = show['first_air_date']
            reply_text = f"Title: {title}\nOverview: {overview}\nRelease Date: {release_date}"
        else:
            reply_text = "TV show not found."
    else:
        reply_text = "An error occurred while fetching data."

    bot.send_message(update.chat.id, reply_text)

@app.on_inline_query()
def inline_query(bot, update):
    query = update.query
    response = requests.get(f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={query}")
    
    if response.status_code == 200:
        data = response.json()
        results = [
            {
                'type': 'article',
                'id': str(show['id']),
                'title': show['name'],
                'input_message_content': {
                    'message_text': f"Title: {show['name']}\nOverview: {show['overview']}\nRelease Date: {show['first_air_date']}"
                }
            }
            for show in data['results']
        ]
        bot.answer_inline_query(update.id, results)

app.run()
