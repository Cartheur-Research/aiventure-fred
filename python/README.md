## Running this version of animals

Booting a Cartheur application on Linux at startup

In a terminal run

`sudo crontab -e`

and add somewhere in the file, here is for Cartheur Animals in python:

`@reboot sudo python /home/chip/projects/henry/animalsHenry.py &`

For the NET Framework 4 runtime

`@reboot sudo mono Cartheur.Animals.Console.exe -aeon -adult -english -theonlyone -non`

Note that the editor is vi, so `INSERT` to write to line, `ESC` to step out, : to call the command interface, `wq` to save or `q!` to exit without saving.

## Notes

The .Net version is coming soon.
