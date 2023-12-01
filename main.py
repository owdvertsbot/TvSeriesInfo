from my_package.sub_module import MyClass


import requests
from pyrogram import Client, filters
from tmdbv3api import TMDb, Movie

# Your Pyrogram bot token and TMDB API key
API_ID = '950903'
API_HASH = '69d37ae7fdf5154293b01434044c37dd'
BOT_TOKEN = '6230370760:AAFx2IL5HpXA3PEeaGVmtK2R9cYTuhO4VP0'


app = Client("my_movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

tmdb = TMDb()
tmdb.api_key = '81cc1df77fb33a00b3b88dc5c3a26afe'
tmdb.language = 'en'
tmdb.debug = True


@app.on_message(filters.text & ~filters.command)
async def search_movie(client, message):
    movie_name = message.text
    movie = Movie()
    movie_results = movie.search(query=movie_name)
    await client.send_message(chat_id=message.chat.id, text=f"Found these movies: {movie_results}")


app.run()
