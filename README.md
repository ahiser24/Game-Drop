![Logo](https://github.com/ahiser24/Game-Drop/blob/main/assets/frame0/logo.png)

## Overview
Game Drop is a program designed for gamers who want to share their most exciting moments with their friends and community. Many gamers record their gameplay using GeForce ShadowPlay and Radeon Adrenaline. With Game Drop, users can easily cut and share the last 30 seconds of their game recordings without the need for costly Discord Nitro subscriptions or video editing software. Game Drop is perfect for streamers, content creators, and anyone who wants to share their game moments with their friends and community. 

In short, it allows you to:
* Cut the last 30 seconds of a recording without needing a video editor. No one wants to see a 5 minute video. This keeps their attention.
* Shrinks the video down to under 8MB. Now it's small enough to share with many social media and chat apps.
* Automatically sends the video to your favorite Discord channel upon conversion. Set it and forget it.

### Newbie Alert
This is my first real hobby project and it's been great learning to code along the way. I have more updates and ideas to enhance this tool coming soon, but I wanted to get it in the hands of my friends and anyone else interested as soon as possible. While there are plenty of other tools similar to this, I couldn't find any that would directly send the video to Discord when it was done.

## Why Game Drop?
* Easy to use.
* No need to upload a video to sketchy websites as it's all run local.
* Instantly share to Discord. Avoid "Your files are too powerful" messages.
* Near instant conversions (with NVIDIA or AMD GPU)

## How it works
* Python is used mostly for the User Interface with Tkinter.
* Users will select a video they want to share and an output location to store the converted video.
* The user will then select an encoder being their graphics card of processor.
* If the user would like to share directly to a Discord channel they will need to specify a webhook that is linked to that channel. See: [Creating a Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more details.
* A PowerShell script is then called using these parameters to run FFMPEG to take the last 30 seconds of the video and lower the bitrate to make it under 8MB in size.
* A PowerShell module called "[PSDsHook](https://github.com/gngrninja/PSDsHook)" allows the program to take the converted video and send it through the Discord webhook directly to the Discord channel so users can instantly view the video.

## Prerequisites - Should the user not have these; I've included scripts that will automatically install the latest PowerShell 7 and FFMPEG versions as well as set the Environmental Variables for FFMPEG.
* PowerShell 7 with loading scripts enabled.
* FFMPEG 3 or higher.
* Local admin rights to update a .txt file in the installation directory.


## How To Use
* **Run** "Game Drop.exe" as an Administrator. This ensures that the Discord Webhook can write back to the installation folder.
* **Input** = Select the video you want to share.
* **Output** = Where would you like the encoded video to be saved?
* **Select Encoder** = Choose which graphics card you have or use CPU if you don't have one.
* **Discord Webhook** = Enter the webhook for the Discord channel you want to send the video to. See: [Creating a Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more details.
* **Update** = Click this button to register the Discord Webhook.
* **Drop It** = Encode the video and send it to the Discord channel if entered.
