import sys
import spotipy
import spotipy.util as util

# This is the file that takes care of playing Spotify on my pi.
# I use raspotify as the api communicator with Spotify.
# At the beginning it grabs the Device_id of my pi and saves that
# as my raspotify variable which is used to make sure its actually
# connected. The sp variable is the actual client which I call to interact
# with spotify. It controls the session.


running = False
scope = 'user-read-playback-state'
token = util.prompt_for_user_token(
    '121390876',
    'user-modify-playback-state',
    client_id='8af005da65954d03a6478794a281e106',
    client_secret='d35de2392b724f64b1921e60f5e85b26',
    redirect_uri='http://localhost/')
sp = spotipy.client.Spotify(auth=token)
shuffleBoolean = False

results = sp.devices()
for device in results['devices']:
    if device['name'] == 'raspotify':
        raspotify = device
if raspotify:
    sp.shuffle(False, raspotify['id'])
else:
    print("Could not find Raspotify")

# Actual code starts here after the initial preporations

def play():
    if raspotify:
        sp.transfer_playback(raspotify['id'])
        global running
        running = True
    else:
        print("Could not find Raspotify")

def pause():
    if raspotify:
        sp.pause_playback(raspotify['id'])
        global running
        running = False
    else:
        print("Could not find Raspotify")

def next():
    if raspotify:
        sp.next_track(raspotify['id'])
    else:
        print("Could not find Raspotify")

def previous():
    if raspotify:
        sp.previous_track(raspotify['id'])
        sp.previous_track(raspotify['id'])
    else:
        print("Could not find Raspotify")

def beginning():
    if raspotify:
        sp.previous_track(raspotify['id'])
    else:
        print("Could not find Raspotify")

def top_50():
    if raspotify:
        sp.start_playback(raspotify['id'], 'spotify:user:spotifycharts:playlist:37i9dQZEVXbMDoHDwVN2tF')
        global running
        running = True
    else:
        print("Could not find Raspotify")

def playlist(name="shower"):
    if raspotify:
        playlists = sp.current_user_playlists()
        for list in playlists['items']:
            if list['name'].strip().lower() == name.strip():
                sp.start_playback(raspotify['id'], list['uri'])
                global running
                running = True
    else:
        print("Could not find Raspotify")

def shuffle():
    if raspotify:
        global shuffleBoolean
        shuffleBoolean ^= True
        sp.shuffle(shuffleBoolean, raspotify['id'])
    else:
        print("Could not find Raspotify")


def interpret(request):
    if "top 50" in request:
        top_50()
    elif "shuffle" in request:
        shuffle()
    elif "playlist" in request:
        request = request.split(" ")
        playlist(" ".join(request[request.index("playlist")+1:]))
    elif "previous" in request:
        previous()
    elif "next" in request:
        next()
    elif "pause" in request:
        pass
    elif "beginning" in request:
        beginning()
    elif "play" in request:
        play()
    else:
        return "Sorry, I could not understand your request."


# This is a basic getter that returns if spotiy is playing. It is used
# in main.py to pause when the user says the hot word.
def playing():
    global running
    return running
