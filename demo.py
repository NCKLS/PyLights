import pylights.pylights
import pyphue # Manages phillips hue lights
import os # Manages directories
import difflib # Manages matching search query to correct song

myHue = pyphue.PyPHue(wizard = True)

if not os.path.exists("Songs"):
    os.mkdir("Songs");

possibleFiles = os.listdir("Songs")
closestMatch = []
lightsToAdd = [] # A list of lights to be loaded

myPyLights = pylights.PyLights(myHue)
if input("(Press enter to begin)") == "skip":
    lightsToAdd = [['1', 'n', 'y', 'n', 'y'], ['2', 'n', 'y', 'n', 'y'], ['3', 'y', 'n', 'y', 'n']]
else:
    while input("\nWould you like to add a light? (y/n): ") == "y":
        addLightId = input("Light %i Id: " % (len(lightsToAdd) + 1))
        addLightHarmonic = input("Harmonic (y/n): ")[0].lower()
        addLightPercussive = input("Percussive (y/n): ")[0].lower()
        addLightColor = input("Color (y/n): ")[0].lower()
        addLightFlash = input("Flash (y/n): ")[0].lower()
        lightsToAdd.append([addLightId, addLightHarmonic, addLightPercussive, addLightColor, addLightFlash])
        print("\n\nLights:\n")
        for item in lightsToAdd:
            print("ID: %s | Harmonic: %s | Percussive: %s | Color: %s | Flash: %s" % (item[0], item[1], item[2], item[3], item[4]))


for item in lightsToAdd:
    harmonicBool = (item[1] == "y")
    percussiveBool = (item[2] == "y")
    colorBool = (item[3] == "y")
    flashBool = (item[4] == "y")
    myPyLights.loadLight(lightId=item[0], harmonic=harmonicBool, percussive=percussiveBool, color=colorBool, flash=flashBool)

while True:
    closestMatch = ""
    print("Song Selection...")
    for i in range(0, len(possibleFiles)): # Prints list of songs available in the Songs file directory
        print("    %s" % (possibleFiles[i]))

    while len(closestMatch) < 1:  # Continously ask user to input a song of choice until a song is found
        songName = input("Song Name: ")
        closestMatch = difflib.get_close_matches(songName,
                                                 possibleFiles)  # Returns most similar file names to song name entered

        if (len(closestMatch) > 0):
            songName = closestMatch[0]  # Sets song name to the closest matching song file
            print("Playing %s" % (songName))
            myPyLights.loadAudio(fileName = songName) # Once a song has been selected, load the song into the pylights object
            break
        else:
            print("\n\nSong not found! Please try again!\n")

    myPyLights.run()