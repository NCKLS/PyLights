import pyphue # Manages phillips hue lights
import time # Manages timing of notes
import librosa # Manages detection of onsets and onset strength
import pickle # Manages saving/loading of data
import os # Manages directories
import difflib # Manages matching search query to correct song
import msvcrt # Manages key input
import random # Manages random color generation
from pygame import mixer # Plays mp3 files

setIp = "192.168.1.21"
userId = "tLWZE6rPwKQbnYm-S6Gx9u5FVT8oJd9r5YYArxPL"
myHue = pyphue.PyPHue(ip = setIp, user = userId, AppName = 'PyPhue', DeviceName = 'Desktop:NickHowell1234123123', wizard = False)
print("ip: %s" % (myHue.ip))
print("user: %s" % (myHue.user))

if not os.path.exists("SongData"):
    os.makedirs("SongData")

if not os.path.exists("Songs"):
    os.makedirs("Songs")

primaryLight = '3'
secondaryLights = ['1', '2']
lastBigBeat = 0

secondaryOn = 0

while True:
    possibleFiles = os.listdir("Songs")
    closestMatch = []

    print("Song Selection...")
    for i in range(0, len(possibleFiles)):
        print("    %s" % (possibleFiles[i]))

    while len(closestMatch) < 1: # Continously ask user to input a song of choice until a song is found
        songName = input("Song Name: ")
        closestMatch = difflib.get_close_matches(songName, possibleFiles) # Returns most similar file names to song name entered

        if (len(closestMatch) > 0):
            songName = closestMatch[0] # Sets song name to the closest matching song file
            print("Playing %s" % (songName))
            break
        else:
            print("\n\nSong not found! Please try again!\n")

    if (os.path.isfile(os.path.join(os.getcwd() + "/SongData/", "%s.txt" % songName))):
        beat_times = []
        o_env = []
        with open(os.path.join(os.getcwd() + "/SongData/", "%s.txt" % songName), 'rb') as file:
            readSongData = pickle.load(file)

        for item in readSongData:
            beat_times.append(item[0])
            o_env.append(item[1])
    else:
        try:
            y, sr = librosa.load(os.path.join(os.getcwd() + "/Songs/", "%s" % songName))
            #tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            #beat_times = librosa.frames_to_time(beat_frames, sr=sr)
            o_env = librosa.onset.onset_strength(y=y, sr=sr)
            beat_times = librosa.frames_to_time(librosa.onset.onset_detect(y=y, sr=sr), sr=sr)

            writeSongData = []
            for pos, item in enumerate(beat_times):
                writeSongData.append([item, o_env[pos]])

            with open(os.path.join(os.getcwd() + "/SongData/", "%s.txt" % songName), 'wb') as file:
                pickle.dump(writeSongData, file)
        except Exception as e:
            print(e)
            exit()

    myHue.turnOn(primaryLight)
    myHue.setBrightness(primaryLight, 255)
    brightness = 255
    off = False

    starttime = time.time()

    mixer.init()
    mixer.music.load(os.path.join(os.getcwd() + "/Songs/", "%s" % songName))
    mixer.music.play()

    tick = 0
    for i in range(0, len(beat_times)):
        if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
            mixer.music.stop()
            break
        elif msvcrt.kbhit() and msvcrt.getch() == chr(32).encode():
            switch = True
            mixer.music.pause()
            while switch:
                if msvcrt.kbhit() and msvcrt.getch() == chr(32).encode():
                    switch = False
                    mixer.music.unpause()

        if (off):
            myHue.turnOn(primaryLight)
            off = False
        tick = (tick + 1) % 2

        if (tick == 1):
            brightness = 255 - int(275 - (100/(o_env[i]+0.01)))
        else:
            brightness = int(275 - (100/(o_env[i]+0.01)))

        if (brightness < 125): brightness -= 50
        else: brightness += 50

        brightness = min(brightness, 255);
        brightness = max(brightness, 0);

        if brightness == 255: #On power notes it should reach 255, and we want to light up all secondary lights on power notes
            secondaryOn = abs(beat_times[i] - lastBigBeat)
            if (secondaryOn > 1):
                lastBigBeat = beat_times[i]
                print(secondaryOn)
                for item in secondaryLights:
                    myHue.turnOn(item)
                    myHue.setBrightness(item, int(50 * secondaryOn))
            myHue.setBrightness(primaryLight, brightness)
            myHue.setHue(primaryLight, random.randint(0, 65535))
        elif brightness > 0:
            myHue.setBrightness(primaryLight, brightness)
            myHue.setHue(primaryLight, random.randint(0, 65535))
        else:
            secondaryOn = abs(beat_times[i] - lastBigBeat)
            if (secondaryOn > 1):
                lastBigBeat = beat_times[i]
                for item in secondaryLights:
                    myHue.turnOn(item)
                    myHue.setBrightness(item, int(50 * secondaryOn))
            myHue.setBrightness(primaryLight, brightness)
            myHue.setHue(primaryLight, random.randint(0, 65535))
            off = True
            myHue.turnOff(primaryLight)

        for item in secondaryLights:
            myHue.turnOff(item)

        if (i < len(beat_times) - 1):
            time.sleep(max(beat_times[i + 1] - (time.time() - starttime),0))

    print("\n\nSong Over...\n\n")
    for item in secondaryLights:
        myHue.turnOff(item)

    myHue.turnOff(primaryLight)