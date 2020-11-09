# Import the libraries i'm gonna need for creating the GUI..
# ..and downloading the YouTube videos
import tkinter as tk
import tkinter.font as font
from tkinter import *
from tkinter import messagebox, filedialog
from pytube import YouTube
from moviepy.editor import *


# Creating Widgets function
def Widgets():
    # Creating the link label text
    link_label = \
        Label(win, text="YouTube link:", bg=bg_color, foreground="#ffffff", font=my_font)

    # Adjusting its place on the GUI
    link_label.grid(row=1, column=0, pady=10, padx=5)

    # The textbox where the user puts the YouTube url
    win.linkText = \
        Entry(win, width=50, textvariable=url, bg=link_text_color, font=my_font, fg=fg_link_text_color)

    # Its place on the GUI
    win.linkText.grid(row=1, column=1, pady=5, padx=5)

    # Creating the destination label
    destination_label = \
        Label(win, text="Destination:", bg=bg_color, foreground="#ffffff", font=my_font)

    # Adjusting its place on the GUI
    destination_label.grid(column=0, pady=5, padx=5)

    # Creating a clear button to clear our url if we are too lazy to hod delete
    clear_button = \
        Button(win, text="Clear", command=lambda: url.set(""), width=10, bg=button_colors, fg=fg_link_text_color, font=my_font)

    # Adjusting its place on the GUI
    clear_button.grid(row=1, column=2, pady=1, padx=1)

    # The textbox where the user puts the download path
    win.destinationText = \
        Entry(win, width=50, textvariable=download_path, bg=link_text_color, font=my_font, fg=fg_link_text_color)

    # Its place on the GUI
    win.destinationText.grid(row=2, column=1, pady=5, padx=5)

    # Creating browse button so we can browse and choose where we want to download our files
    browse_button = \
        Button(win, text="Browse", command=Browse, width=10, bg=button_colors, fg=fg_link_text_color, font=my_font)

    # Adjusting its place on the GUI
    browse_button.grid(row=2, column=2, pady=1, padx=1)

    # Declaring i variable so i don't have to type the rows every time,
    # and so i can increment it to prevent the buttons from stacking
    i = 3

    # Creating the .mp3 checkbox
    checkbox_mp3 = Checkbutton(win,
                               text=".mp3",
                               variable=chk,
                               command=lambda: print("pressed", chk.get()),
                               bg=bg_color, fg="#ffffff",
                               selectcolor=s_color,
                               activebackground=bg_color,
                               font=my_font,
                               activeforeground='white')
    checkbox_mp3.grid(row=i, column=1, pady=10)

    # Showing a message to the user that he is not able to use the resolution radio buttons
    # because he is gonna download in .mp3 format and we don't need resolutions for that
    disclaimer_check_box = \
        Label(win, text="Disclaimer: If this box is checked the resolution buttons will not work!", bg=bg_color, foreground="#fe5f5f", font=my_font)

    # Adjusting the disclaimer's button position in the GUI
    disclaimer_check_box.grid(row=i+1, column=1, pady=10)

    i += 2

    # Creating a dictionary to store all the available resolutions
    video_quality = {
        "Download in 1080p": "1080",
        "Download in 720p": "720",
        "Download in 480p": "480",
        "Download in 360p": "360",
        "Download in 240p": "240",
        "Download in 144p": "144"
    }

    # The default installing resolution will be set to 1080p
    v.set("1080")

    # Creating the radiobuttons
    for (text, value) in video_quality.items():
        rez_radio_button = Radiobutton(win,
                                       text=text,
                                       value=value,
                                       variable=v,
                                       command=lambda: print(v.get()),
                                       bg=bg_color, fg="#ffffff",
                                       selectcolor=s_color,
                                       activebackground=bg_color,
                                       font=my_font,
                                       activeforeground='white')
        rez_radio_button.grid(row=i, column=1, pady=2)
        i += 1

    # Creating Download button to download the video or the audio we want
    download_button = \
        Button(win, text="Download", command=Download, width=20, bg=button_colors, fg=fg_link_text_color, font=my_font)

    # Adjusting its position on the GUI
    download_button.grid(row=i + 1, column=1, pady=15, padx=3)


# A Browse() function is called when I press the Browse button I created earlier
def Browse():
    # Try Except if something goes wrong with the directory we choose
    try:
        # Giving the directory where we wanna download the files
        download_dir = filedialog.askdirectory(initialdir=r"C:\Users\Desktop", title="Choose a folder!")

        download_path.set(download_dir)
    except Exception as e:
        print(messagebox.showinfo("Oops, something happened!", "Invalid path!") + e)


# The Download() function is called when I press the Download button
def Download():
    # Getting the url
    yt_link = url.get()

    # A try except to tell us if we did something wrong
    try:
        # Getting the download direction from the Browse() function
        download_folder = download_path.get()

        # Checking if the user didn't entered a file directory
        # if not a messagebox pops up and asks him to choose again
        if len(str(download_folder)) <= 0:
            messagebox.showinfo("You did something wrong!", "Please choose a folder to download the file")
            return

        # Getting the YouTube video with the url we entered
        get_video = YouTube(yt_link)

        # Checking if the user checked the .mp3 box
        # if he did I convert the .mp4 to .mp3 format
        if chk.get() == 1:
            # we get the title of the video and concatenating it .mp3 at the end
            video_title = get_video.title + ".mp3"

            # picking the video streams available and downloading the first stream
            video_stream = get_video.streams.filter().first()
            downloaded_video = video_stream.download(download_folder)

            # getting the audio from the video
            video_clip = VideoFileClip(downloaded_video)
            audio_clip = video_clip.audio

            # specifying where the audio is gonna download
            final_path = download_folder + '\\' + video_title

            # downloading the new .mp3 file in this location
            audio_clip.write_audiofile(final_path)

            # closing the audio and the video so they don;t have to work on the background
            audio_clip.close()
            video_clip.close()

            # and finally removing the video file that downloaded along with the audio file
            # because i had to have the .mp4 file to convert it into .mp4
            # and now that i don't need that video file i will just delete it
            os.remove(downloaded_video)

        # if the user chose to download the video instead of the audio
        else:
            # we get all the available video streams and filter the by resolution
            # which the user picked earlier, if not the default will be 1080p
            video_stream = get_video.streams.filter(res=str(v.get() + "p")).first()

            print(video_stream)

            if str(video_stream) == "None":
                messagebox.showinfo("That's quite the bummer", "The sream you are searching for in this resolution is unavailable, please choose other resolution")
                return

            # and finally downloading the video
            video_stream.download(download_folder)

        # displaying on the screen that everything is downloaded and saved in the dir we chose
        messagebox.showinfo("Download info!", "Downloaded and saved in:\n" + download_folder)
    except Exception as e:
        messagebox.showinfo("Oops, something went wrong!", e)

# Create an Instance
win = tk.Tk()

# scoping these so i can use them everywhere

# These the variables I am gonna need to write in the variable parameter in the buttons and the checkbox
v = tk.StringVar(master=win)
chk = tk.IntVar(master=win)

# Set the title for the GUI
win.title("Youtube Downloader")

# all the colors that i'm using, atleast more important ones
bg_color = "#373737"
button_colors = "#FF7F50"
link_text_color = "#fca483"
fg_link_text_color = "#141414"
s_color = "coral"

# the font i am using
my_font = font.Font(family='Bookman Old Style', size=12, weight="bold", slant="italic")

# this picks the background color and the cursor when the GUI is shown
win.configure(bg=bg_color, cursor="plus")

# Making it with constant width and height
win.resizable(False, False)

# This is the URL of the video i want to download
# test url: https://www.youtube.com/watch?v=DLzxrzFCyOs
url = StringVar(master=win)

# And this is the path where im gonna download the file
download_path = StringVar(master=win)

# Calling the Widgets() function
Widgets()

# Start the GUI/ Create the main loop
win.mainloop()
