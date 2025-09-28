# TapeDivider
A python script to automatically divide a playlist to best fit onto a physical cassette tape.

Installation ====

For Windows, simply download the .exe file and _internal folder, and put them in the same file.
Then simply double click the .exe.

Alternatively .py file can be run directly, by adding your own .env file with spotify developer API codes inside.

Features ====

Can accept any tape length up to 120 minutes. 
Will automatically gather track names and length from spotify playlist. 
If the playlist is shorter than the full tape length it will aim to split them evenly between both sides (allowing for the tape to later be cut down).
If the playlist is longer than the tape it will pick the tracks that fit the time on each side the closest, i.e. on a 90 minute tape it will pick songs that fit as close to 45 mins on the dot.

Planned Features ====

Hope to add the ability to select "required" songs which the other songs will be chosen around.
Maybe even a GUI...
