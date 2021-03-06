# PyLights
PyLights allows you to easily make your philips hue light bulbs pulse to the beat of your own music.
It's as easy as...

1) Connect to the bridge using PyPHue (One line of code)
2) Connect your lights to PyLights and tell them what you want them to do (One line of code)
3) Load an mp3 or wav file into PyLights

then you're completely set and ready to run PyLights!

##### GIF Preview (Much cooler with audio)

<a href="https://imgflip.com/gif/1ov3b8"><img src="https://i.imgflip.com/1ov3b8.gif" title="made at imgflip.com"/></a>

##### Video Preview (Work In Progress)

### Quick Demo:
If you would like to quickly demo PyLights rather than use it as a tool, go a ahead and run the demo.py file. It will guide you step by step into setting up your system.

----------------------------------------
### Installation:
`pip install pylights`

### Dependencies:
* PyPHue (allows PyLights to communicate with philips hue lights)
* PyGame (Allows PyLights to play audio)
* Librosa (allows PyLights to analyze audio and find onsets, rhythm, and beats)

### Example:
To utilize PyLights you need to first use the PyPHue module to create a bridge object. This will allow PyLights to communicate with the lights.

`myHue = pyphue.PyPHue(wizard = True)`

For more information on bridge setup, check out the [PyPHue module page here](https://github.com/rdespoiu/PyPHue)
Chances are, you will only want to use the wizard option during first time setup.

Afterwards you'll need to create a PyLights object

`import pylights.pylights`

`MyPyLights = pylights.PyLights(myHue)`

You'll now need to tell PyLights what lights you have, how to use them, and what lights support colors.
You'll need to find out your light IDs, which begin at 1 and extend to how many lights you have.
It's easy to identify your lights with trial and error.

`MyPyLights.loadLight(lightId = '1', harmonic=True, percussive=True, color=True, flash=False)`

You have the option to make light '1' to react to harmonic beats, percussive beats, or both.
You may also decide whether or not you want the light to flash. The flash option is off by default, but when turned on makes lights turn off more frequently.

You will load every light you want to use this way.

Next you need to load an audio file.

`MyPyLights.loadAudio(fileName="MyFavoriteSong.mp3", songPath="Custom/Path/To/Song(Optional)", dataPath="Custom/Path/To/Data(Optional", saveAndLoad=True)`

You can set custom paths to your audio files, otherwise a data and song folder will be created inside the directory of your python program. You may also chose to turn saveAndLoad on or off. This feature saves the compiled song data to a file so the next time the song is chosen there is no compiling time. Compiling generally takes 10-20 seconds.

##### Now you're set!
All you have to do now is run it.

`MyPyLights.run()`
