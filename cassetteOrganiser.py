import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

scope = "user-library-read"

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def getLength():
    while True:
        print("\nPlease enter the length of your cassette in minutes: ")
        length = input()
        if not(length.isnumeric()):
            print("Invalid - please enter only numbers\n")
        elif int(length) > 120:
            print("Invalid - Cassette cannot be longer than 120\n")
        else:
            return int(length)
        
def getPlaylist():
    while True:
        print("\nPlease enter the Spotify share URL for your playlist: ")
        playlistID = input()
        try:
            playlistID = playlistID.split("/")
            playlistCode, _ = playlistID[4].split("?")
            playlist = sp.playlist_items(playlistCode)    
            return playlist
        except:
            print("ID Not recognised - Couldn't receive data\n")
    
def chooseSongs(songData, tapeLength):
    n = len(songData)
    DP = [[0 for i in range(tapeLength+1)] for j in range(n+1)]
    
    for i in range(1, n+1):
        name, duration = songData[i-1]
        for t in range(1, tapeLength+1):
            if duration > t:
                #print("i value is " + str(i) + "| t value is " + str(t))
                DP[i][t] = DP[i-1][t]
            else:
                withoutSong = DP[i-1][t]
                withSong = DP[i-1][t - duration] + duration
                if max(withSong, withoutSong) == withSong:
                    songData = songData
                DP[i][t] = max(withoutSong, withSong)
    print("Best fit length is " + str(DP[n][tapeLength]) + "s of a possible " + str(tapeLength) + "s\n")
    
    chosenSongs = []
    t = tapeLength
    i = n
    while i > 0 and t > 0:
        if DP[i][t] != DP[i-1][t]:
            chosenSongs.append(songData[i-1])
            t -= songData[i-1][1]
        i -= 1
    
    return chosenSongs


def partitionSongs(chosenSongs, sideLength, tapeLength):
    m = len(chosenSongs)
    target = sideLength
    
    DP = [False for i in range(target+1)]
    DP[0] = True
    
    itemIDx = [-1 for i in range(target + 1)]
    prevSum = [-1 for i in range(target + 1)]
    
    #find the combination to reach the target value
    for i, (name, duration) in enumerate(chosenSongs):
        for t in range(target, duration-1, -1):
            if DP[t-duration] and not DP[t]:
                DP[t] = True
                itemIDx[t] = i
                prevSum[t] = t-duration
    
    #find the closest fill to the side length
    best_fill = None
    for t in range(target, -1, -1):
        if DP[t]:
            best_fill = t
            break
        
    if best_fill is None or best_fill == 0:
        return [], chosenSongs[:]
    
    #backtrack through found table and recover song names and durations
    side = []
    usedIndices = set()
    remaining = best_fill
    
    while remaining > 0:
        idx = itemIDx[remaining]
        if idx == -1:
            raise RuntimeError("Backtrack failed")
        side.append(chosenSongs[idx])
        usedIndices.add(idx)
        remaining = prevSum[remaining]
    
    otherSide = [chosenSongs[i] for i in range(m) if i not in usedIndices]
    
    sideALength = 0
    sideBLength = 0
    for song in side:
        sideALength += song[1]
    for song in otherSide:
        sideBLength += song[1]
    
    print("===== Side A songs =====  |  " + str(round(((sideALength/int(tapeLength/2))*100), 2)) + "% filled")
    for song in side:
        print(song[0])
    
    print("===== Side B songs =====  |  " + str(round(((sideBLength/int(tapeLength/2))*100), 2)) + "% filled")
    for song in otherSide:
        print(song[0])
    

#MAIN======================================

#tape length converted to seconds
tapeLength = getLength() * 60
playlist = getPlaylist()

songData = []
for item in playlist['items']:
    track = item['track']
    if track is None:
        continue
    #converting duration to seconds before storing
    songData.append([track['name'], int(track['duration_ms']/1000)])
    
totalLength = 0
for song in songData:
    totalLength += song[1]

if totalLength < tapeLength:
    print("\nPlaylist is shorter than the tape - filling evenly with all available...\n")
    chosenSongs = chooseSongs(songData, tapeLength)
    #if less than the full tape, split as evenly as possible to allow for tape trimming
    partitionSongs(chosenSongs, int(totalLength/2), tapeLength)
else:
    print("\nPlaylist is longer than tape - Suggesting best fitting songs...\n")
    chosenSongs = chooseSongs(songData, tapeLength)
    partitionSongs(chosenSongs, int(tapeLength/2), tapeLength)





    

    


