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

while input("\nWould you like to add a light? (y/n): ") == "y":
    addLightId = input("Light %i Id: " % (len(lightsToAdd) + 1))
    addLightPrimary = input("Primary (y/n): ")[0].lower()
    addLightColor = input("Color (y/n): ")[0].lower()
    lightsToAdd.append([addLightId, addLightPrimary, addLightColor])
    print("\n\nLights:\n")
    for item in lightsToAdd:
        print("ID: %s | Primary: %s | Color: %s" % (item[0], item[1], item[2]))

for item in lightsToAdd:
    primaryBool = (item[1] == "y")
    colorBool = (item[2] == "y")
    myPyLights.loadLight(lightId=item[0], primary=primaryBool, color=colorBool)

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