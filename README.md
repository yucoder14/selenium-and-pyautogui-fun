WHY?
====

Instead of searching for students and right clicking on students' head shot to
save the images, now you can run this script to automatically crawl head shots,
albeit the script may break because GUI scripting is fragile by nature. 

~Instead of spending time to learn about why I was not getting the image I 
wished from just curl'ing the image `src`, I defaulted to GUI option because 
it's more fun that way.~

The reason why I was not getting the correct images was because when I was using
requests, it wasn't using my session cookies. It appears that Carleton does not 
allow strangers to download photos of students. Now, there's no need to be 
flimsy about messing with the computer. 

Prerequisites
=============

Assumes that you are running the script on macOS environment because there's 
no need to make this script cross platform, considering its very niche usage. 

~You need to give the Terminal Accessibility rights in system preferences before
running this script. Go to System Preferences > Privacy & Security > 
Accessibility. If Terminal is already present among the list, toggle the switch.
If not present, press the plus button and find Terminal.app.~

You also need to have Chrome.

The script depends on two (three?) libraries: 

```
selenium
pytautogui
```

I think `getpass` should be installed with base python, but, if not, you need
that too.

It is highly recommended that you use a python venv to run this script.

Key Assumption
==============

Assumes that students you are trying to search for has single first and single
last name. If that is not the case, the script will try to search the individual
only using the last name.

Usage
=====

```
python3 crawl_images.py -i student_names.txt -o output_directory
```

When the script prompts you for username and password, enter your Carleton
username and password.

Caveats
=======

~When the script is running, you CANNOT touch the machine where the script is 
running. Otherwise, everything will break. GUI scripting is very fragile, so
please tend it with extra care. If you get unlucky and a pop-up pops up, 
try to recover as fast as you can. If not, kill the script. If you re-run the
script, it will continue from where you previously failed.~

This script is bound to fail sometime in the future if the College decides 
to revamp the student directory, modify any of the id's of html elements, 
or decide to rework how pages are linked. 

It's also very possible that DUO might no longer be a thing. So feel free to 
use the script as long as it works. If it breaks, then, well, you should build 
the next one. It's fun. Or vibe code it. Whatever works for you.
