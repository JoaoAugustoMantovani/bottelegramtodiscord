# Telegram to Discord Forwarder Bot
A desktop bot with a graphical user interface that monitors messages and images from a specific Telegram channel (public or private) and forwards them in real-time to a Discord channel using a Webhook.

The application is built in Python with a user-friendly Tkinter interface and can be minimized to the system tray (next to the Windows clock) to run seamlessly in the background.

### 📥 Download
You don't need to install Python to use this bot! Download the latest ready-to-use version from our Releases page.

➡️ Download the [Latest Version](https://github.com/joaoaugustomantovani/bottelegramtodiscord/releases/latest) (Windows x64)

# ⚙️ Setup Guide: How to Get the Bot Running
To use the bot, you will need to fill in a few fields in the application window. Follow this guide to get all the required information.

## 1. Telegram API Credentials (API_ID & API_HASH)
These keys act as your application's "ID card" for Telegram.

Log in to your Telegram account on the official website: [my.telegram.org](my.telegram.org).

Click on "API development tools".

Fill out the form to create a new application (the names can be anything):

App title: My Message Bot

Short name: my_msg_bot_12345 (this must be a unique name worldwide! If you get an error, try a different one).

Platform: Select Desktop.

Click "Create application".

The next page will display your credentials. Copy and save the values for api_id and api_hash. You will use these in the "Telegram API ID" and "Telegram API Hash" fields.

## 2. Channel to Monitor (Public or Private)
This tells the bot which conversation it should listen to.

For Public Channels or Groups:

Simply enter the channel's @username in the field. Example: @telegram.

For Private Channels or Groups:

Private channels don't have a @username, so we need their numeric ID. It's easy to get:

Open Telegram (Web or Desktop version).

Find the private channel or group you want to monitor.

Forward any message from that private channel to the @userinfobot.

The @userinfobot will reply with some information. The line you need is "Forwarded from", which contains the ID. The ID for private channels usually starts with -100.

Copy this full number (including the - sign) and paste it into the "Channel to Monitor" field. Example: -100123456789.

## 3. Discord Webhook URL
This URL is the "address" where the bot will send the messages.

Open Discord.

In your server, right-click on the desired text channel and go to Edit channel > Integrations.

Click on "Create Webhook".

Give the Webhook a name (e.g., "Telegram Bridge") and click the "Copy Webhook URL" button.

Paste this URL into the "URL Webhook Discord" field. Treat this URL like a password!

## 🚀 How to Use the Bot
Download and run the .exe file from the Releases page.

Fill in all the fields in the program window with the information you just gathered.

In the "Phone Number" field, enter your Telegram phone number in the international format (e.g., +15551234567).

If your Telegram account uses Two-Step Verification, fill in the "2FA Password" field. Otherwise, you can leave it blank.

Click "Save Configuration" to make the bot remember your settings.

Click "▶ Start Bot".

The first time you connect, Telegram will send a login code to your app. A pop-up window will appear in the bot for you to enter this code. After logging in, the bot will start working in the background.

Running in the Background
To minimize the bot, just click the "X" on the window. It will disappear from the taskbar and an icon will appear in the system tray (next to the clock).

To reopen the window, right-click the icon in the system tray and select "Show".

To close the program completely, right-click the icon and select "Exit".
