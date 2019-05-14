# HTML Detective

## Introduction
This application was based on the projects designed by Professor Sapienza from URFJ and originally all in python.
I compiled most Sapienza's proposed Python first year projects into one. Initially this was was a tkinter application, since this was the library proposed by the Prof, but I've created a new version using React Native for the front end.
Besides that, I have also modified the way I store the data, however still using Python libraries, instead of saving it as file system, I switched to database system for the backend. Code for the backend available [here](https://github.com/lnogueir/DetectiveFrontend).

## What it does:
This app is supposed to interact with the users:
Users create their own topics and respective tags, then give the app some URL, then the "detective" will analyze the url and display a result graph with the most likely results on what the website is about, based on the user topics. 
Those graphical results can then be sent via email in PNG or XLS format to the user's contact list.

## Outcomes:
Even though there might not seem to have a direct application for this app, I believe the concepts applied here can be easily extended to those applied in daily apps, and so does Professor Sapienza, since on demand libraries such as Flask restful, matplotlib, Beautiful Soup, etc. have been explored in their main functionalities.

# Some GIFs on the app's main functionalities: 

## Adding a new topic:
<a href="https://imgflip.com/gif/30t3jw"><img src="https://i.imgflip.com/30t3jw.gif" title="made at imgflip.com"/></a>

## Getting results with a url example:
<a href="https://imgflip.com/gif/30t3wc"><img src="https://i.imgflip.com/30t3wc.gif" title="made at imgflip.com"/></a>

## Emailing contacts with detective mailer:
<a href="https://imgflip.com/gif/30t4bg"><img src="https://i.imgflip.com/30t4bg.gif" title="made at imgflip.com"/></a>

## Sign in page:
<img src="assets/signin.png" width="250">

 
