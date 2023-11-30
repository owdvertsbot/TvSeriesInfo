import requests
from pyrogram import Client, filters
from tmdbv3api import TMDb, Movie

# Your Pyrogram bot token and TMDB API key
API_ID = '950903'
API_HASH = '69d37ae7fdf5154293b01434044c37dd'
BOT_TOKEN = '6230370760:AAFx2IL5HpXA3PEeaGVmtK2R9cYTuhO4VP0'
TMDB_API_KEY = '81cc1df77fb33a00b3b88dc5c3a26afe'

# Initialize the TMDB API
TMDb().api_key = TMDB_API_KEY
TMDb().language = 'en'

# Initialize the Pyrogram bot
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Welcome to the TV Show Information bot!")

@app.on_message(filters.command("info"))
def get_tv_show_info(client, message):
    if len(message.text.split()) < 2:
        client.send_message(chat_id=message.chat.id, text="Please provide the name of the TV show you want to know about.")
    else:
        tv_show_name = message.text.split()[1]
        try:
            search_results = TMDb().search_tv_show(tv_show_name)
            if search_results['total_results'] > 0:
                first_result = search_results['results'][0]
                tv_show = TMDb().tv_show(first_result['id'])
                message = f"{tv_show['name']} ({tv_show['first_air_date']}) - {tv_show['overview']}"
                client.send_message(chat_id=message.chat.id, text=message)
            else:
                client.send_message(chat_id=message.chat.id, text="No results found for your query.")
        except requests.exceptions.RequestException as e:
            client.send_message(chat_id=message.chat.id, text=f"Error: {str(e)}")

app.run()