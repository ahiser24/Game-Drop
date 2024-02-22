<p align="center">
  <img src="https://github.com/ahiser24/Game-Drop/blob/main/assets/frame0/Screenshot.png?raw=true" alt="Logo" width="50%" height="50%"/>
</p>

###
![GitHub all releases](https://img.shields.io/github/downloads/ahiser24/game-drop/total?logo=Github)

## Overview
Game Drop is a program designed for gamers who want to share their most exciting moments with their friends and community. Many gamers record their gameplay using GeForce ShadowPlay and Radeon Adrenaline. With Game Drop, users can easily cut and share the last 30 seconds of their game recordings without the need for costly Discord Nitro subscriptions or video editing software. Game Drop is perfect for streamers, content creators, and anyone who wants to share their game moments with their friends and community. 

In short, it allows you to:
* Cut the last 30 seconds, where the action typically occurs, without needing a video editor. No one wants to see a 5 minute video.
* Shrinks the video down to under 25MB and saves local copy.
* Automatically sends the video to your favorite Discord channel upon conversion. Set it and forget it.

### How To Video
https://youtu.be/8drrtZ-qybc?si=hEAR5JGZNLRfrpTz

### Newbie Alert
This is my first real hobby project and it's been great learning to code along the way. This started out as a PowerShell program and has evolved into a Python application. I have more updates and ideas to enhance this tool coming soon, but I wanted to get it in the hands of my friends and anyone else interested as soon as possible. While there are plenty of other tools similar to this, I couldn't find any that would directly send the video to Discord when it was done. Feel free to adjust it to your liking.

### What's New
In Version 1.66, the following changes have been made:

* Simplified the process and removed output selection. Encoded videos will be stored in the same folder as the input and "_converted" will be appended to its name.
* Removed Linux options. Will try to add that in a later update.
* Optimized the code
* Included FFMPEG to make installation easier.

* Bug fixes
* **Adjusted encoding to change bitrate if the file size becomes too large.**

### Wishlist Features
* Setup a cleaner and more modern GUI
* Auto select GPU/CPU to encode.
* File size selector. 25MB, 50MB, 100MB
* Custom video length
* Choose from multiple Discord channels to send to.


## Why Game Drop?
* Easy to use.
* No need to upload a video to video websites as it's all run locally.
* Instantly share to Discord. Avoid "Your files are too powerful" messages.
* Near instant conversions (with NVIDIA or AMD GPU)

## How it works
* Users will select a video they want to share and select an output location to store the converted video.
* The user will then select an encoder being their graphics card of processor.
* If the user would like to share directly to a Discord channel they will need to specify a webhook that is linked to that channel. See: [Creating a Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more details.
* A call is made to FFMPEG to take the last 30 seconds of the video and lower the bitrate to make the file size under 8MB in size.
* The new file is then sent through a Discord webhook directly to the Discord channel so users can instantly view the video.
 

## How To Use
* **Run** "Game Drop.exe"
* **Select Video** = Select the video you want to share.
* **Select Encoder** = Choose which graphics card you have or use CPU if you don't have one.
* **Discord Webhook** = Enter the webhook for the Discord channel you want to send the video to. See: [Creating a Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more details.
* **Save** = Click this button to register the Discord Webhook.
* **Drop It** = Encode the video and send it to the Discord channel if entered.

