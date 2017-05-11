# PyLights
PyLights aims to make it easy to have your philips hue light bulbs pulse to whatever song or audio file you want.

##### GIF Preview (Much cooler with audio)

![Preview of Lights Reacting to Audio](http://i.imgur.com/JotIP1K.gifv)

##### Video Preview (Work In Progress)
----------------------------------------
### Installation:
`pip install pylights`

### Dependencies:
* PyPhue (allows PyLights to communicate with philips hue lights)
* PyGame (Allows PyLights to play audio)
* Librosa (allows PyLights to analyze audio and find onsets, rhythm, and beats)

### Example:
To utilize PyLights you need to first use the PyPhue module to create a bridge object. This will allow PyLights to communicate with the lights.

`myHue = pyphue.PyPHue(ip = yourIp, user = yourUserId, AppName = 'PyPhue', DeviceName = 'Desktop:YourUserName', wizard = False) # Use the PyPhue module to connect to your bridge`

For more information on bridge setup, check out the PyPhue module page [here](https://github.com/rdespoiu/PyPHue)

Afterwards you'll need to create a PyLights object

`from pylights import *
MyPyLights = pylights.PyLights(myHue)`

You'll now need to tell PyLights what lights you have, how to use them, and what lights support colors.
You'll need to find out your light IDs, which begin at 1 and extend to how many lights you have.
It's easy to identify your lights with trial and error.

`MyPyLights.loadLight(lightId = '1', primary=True, color=True)`

You'll have to determine if the light is primary or not.
Primary lights react to every onset in a song while secondary lights only react to the strongest onsets.
It's also required that the color parametere is filled out. If your philips hue light supports color, set it True, otherwise False.

You will load every light you want to use this way.

Next you need to load an audio file.

`MyPyLights.loadAudio(fileName="MyFavoriteSong.mp3", songPath="Custom/Path/To/Song(Optional)", dataPath="Custom/Path/To/Data(Optional", saveAndLoad=True)`

You can set custom paths to your audio files, otherwise a data and song folder will be created inside the directory of your python program. You may also chose to turn saveAndLoad on or off. This feature saves the compiled song data to a file so the next time the song is chosen there is no compiling time. Compiling generally takes 10-20 seconds.

##### Now you're set!
All you have to do now is run it.

`MyPyLights.run()`
