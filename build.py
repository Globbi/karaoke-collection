import os
import shutil
import jinja2
import json

# global variables
TARGET_DIR = os.environ.get('TARGET_DIR') or '_site'
SONG_DIR = os.environ.get('SONG_DIR') or 'songs'
LYRICS_DIR = os.environ.get('LYRICS_DIR') or 'lyrics'

def clean():
    shutil.rmtree('_site', ignore_errors=True)

def build():
    # copy static resources
    shutil.copytree('static', TARGET_DIR)
    # setup target lyrics dir
    os.makedirs(os.path.join(TARGET_DIR, LYRICS_DIR), exist_ok=True)
    # prepare templating engine
    jinja_env = jinja2.Environment(
        loader = jinja2.FileSystemLoader('templates'),
        autoescape = jinja2.select_autoescape(),
        trim_blocks = True,
        lstrip_blocks = True,
    )
    song_overview = []
    for candidate in os.scandir(SONG_DIR):
        # guard
        if candidate.is_dir() or not candidate.name.endswith('.json'):
            continue
        lyrics_html = candidate.name.replace('.json', '.html')
        # read JSON
        with open(candidate) as json_file:
            song_data = json.load(json_file)
        # store metadata for later
        song_overview.append({
            'anime': song_data['anime'],
            'artist': song_data['artist'],
            'title': song_data['title'],
            'href': LYRICS_DIR + '/' + lyrics_html,
        })
        # render lyrics
        jinja_env.get_template('lyrics/lyrics.html').stream(song_data).dump(os.path.join(TARGET_DIR, LYRICS_DIR, lyrics_html))
    # render index
    jinja_env.get_template('index.html').stream(song_overview = song_overview).dump(os.path.join(TARGET_DIR, 'index.html'))

if __name__ == '__main__':
    clean()
    build()
