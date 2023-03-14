#Game Drop is used to quickly share 30 second gaming clips with friends on Discord.
#As the file also gets saved to the output folder, it can easily be shared
#with other chat programs that have <8MB size limits.



from pathlib import Path

#Tkinter requirements
from tkinter import *
from tkinter import filedialog, messagebox
from discord_webhook import DiscordWebhook
import os
import subprocess
import wmi
import time
window = Tk()


#create a WMI Object
wmi_obj = wmi.WMI()

#Query for NVIDIA card
nvidia_query = "SELECT * FROM Win32_VideoController WHERE AdapterCompatibility LIKE '%NVIDIA%'"
nvidia_result = wmi_obj.query(nvidia_query)

#Query for AMD card
amd_query = "SELECT * FROM Win32_VideoController WHERE AdapterCompatibility LIKE '%AMD%'"
amd_result = wmi_obj.query(amd_query)



#Set the Paths to be used
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


#Get the initial path to the assets and images
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#Populate the text field with the last Discord Webhook from output.txt
def populate():
    global content
    with open("output.txt", "r") as f:
        content = f.read()
        webhook_entry.insert(END, content)
        content = webhook_entry.get()
        return content

#Save the Discord webhook to the file output.txt
def update():
    global content
    content = webhook_entry.get()
    with open('output.txt', 'w') as f:
        f.write(content)
    label_process['text'] = 'Discord Webhook Updated'
    label_process.update()
    time.sleep(2)
    label_process['text'] = 'Status: Ready'
    content = webhook_entry.get()
    return content

#Define Variables
video_input = ""
video_output = ""
video_name = ""
nvidia = "h264_nvenc"
amd = "h264_amf"
cpu = "libvpx-vp9"

    


#Choose video file for input buttton
def choose_video():
    global video_input
    video_input = filedialog.askopenfilename(title = "Select video", filetypes = (("MP4 files", "*.mp4"),("All files", "*.*")))
    print(video_input)

#Choose where to save the encoded video
def choose_save_location():
    global video_output
    global video_name
    video_output = filedialog.asksaveasfilename(title = "Save video", filetypes = (("MP4 files", "*.mp4"), ("All files", "*.*")), defaultextension='.mp4')
    video_name = os.path.basename(video_output)
    print(video_output)

#Takes the encoded video file and sends it to Discord using the webhook provided.
def send_file():
    if not content:
        label_process['text'] = 'Completed'
        label_process.update()
        return
    webhook = DiscordWebhook(url=content, username='Game Drop')
#verify that the file size is smaller than 8MB (Discord limit)
    file_size = os.path.getsize(video_output)
    if file_size / 1024 > 8192:
        messagebox.showerror('Error', 'File size is too large to send')

    with open(video_output, 'rb') as f:
        webhook.add_file(file=f.read(), filename=video_name)
        response = webhook.execute()
        label_process['text'] = 'Completed'
        label_process.update()


#Call PowerShell script for FFMPEG conversion and update the status label
def run_ffmpeg():
    label_process['text'] = 'Encoding. Please wait...'
    label_process.update()
    button_dropit.config(relief='sunken')
    if not video_input or not video_output:
        messagebox.showerror('Error', 'Input and/or output files are not selected')
        button_dropit.config(relief='flat')
        label_process['text'] = 'Status: Ready'
        return
    else:
        option_selected()
        button_dropit.config(relief='flat')
        label_process['text'] = 'Status: Ready'




#Drop Down Menu actions for Encoder
def option_selected():

    global value
    value = var.get()
    if value == "NVIDIA":
        #Check if NVIDIA graphics is detected
        if not nvidia_result:
            label_process['text'] = 'NVIDIA GPU not detected'
            label_process.update()
            time.sleep(2)
            return #Stop the script
        
        # Pass 1
        subprocess.run(['ffmpeg', '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', nvidia, '-vf', 'scale=1280:720', '-an', '-b:v', '1693k', '-pass', '1', '-2pass', '-1', video_output], shell=True)
        # Pass 2
        subprocess.run(['ffmpeg', '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', nvidia, '-vf', 'scale=1280:720', '-acodec', 'copy', '-b:v', '1693k', '-pass', '2', '-2pass', '-1', '-y', video_output], shell=True)
        send_file()

    elif value == "AMD":
        #Check if AMD graphics is detected
        if not amd_result:
                label_process['text'] = 'AMD GPU not detected'
                label_process.update()
                time.sleep(2)
                return #Stop the script

        # Pass 1
        subprocess.run(['ffmpeg', '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', amd, '-vf', 'scale=1280:720', '-an', '-b:v', '1693k', '-pass', '1', '-2pass', '-1', video_output], shell=True)
        # Pass 2
        subprocess.run(['ffmpeg', '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', amd, '-vf', 'scale=1280:720', '-acodec', 'copy', '-b:v', '1693k', '-pass', '2', '-2pass', '-1', '-y', video_output], shell=True)
        send_file()

    else:
        # Pass 1
        subprocess.run(['ffmpeg', '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', cpu, '-vf', 'scale=1280:720', '-an', '-b:v', '1693k', '-pass', '1', '-2pass', '-1', video_output], shell=True)
        # Pass 2
        subprocess.run(['ffmpeg', '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', cpu, '-vf', 'scale=1280:720', '-acodec', 'copy', '-b:v', '1693k', '-pass', '2', '-2pass', '-1', '-y', video_output], shell=True)
        send_file()




#Set the Title and window position
window.title("Game Drop")
icon = PhotoImage(file=relative_to_assets("logo.png"))
window.iconphoto(False, icon)
width = 800
height = 600
x_offset = (window.winfo_screenwidth() - width) // 2
y_offset = (window.winfo_screenheight() - height) // 2
window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
window.configure(bg = "#FFFFFF")

#Set the background
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_bg = PhotoImage(
    file=relative_to_assets("bg.png"))
image_bg = canvas.create_image(
    400.0,
    300.0,
    image=image_image_bg
)

#Set the Logo
image_image_logo = PhotoImage(
    file=relative_to_assets("logo.png"))
image_logo = canvas.create_image(
    725.0,
    525.0,
    image=image_image_logo
)

image_rectangle = PhotoImage(
    file=relative_to_assets("rectangle.png"))
rectangle = canvas.create_image(
    186.0,
    246.0,
    image=image_rectangle
)

#Output button
button_image_output = PhotoImage(
    file=relative_to_assets("output.png"))
button_output = Button(
    image=button_image_output,
    borderwidth=0,
    highlightthickness=0,
    command=choose_save_location,
    relief="flat"
)
button_output.place(
    x=64.0,
    y=160.0,
    width=174.0,
    height=36.0
)


#create encoder option menu
var = StringVar(window)
var.set("NVIDIA") # default value
value = var.get()

option = OptionMenu(window, var, "NVIDIA", "AMD", "CPU")
option.pack()

def callback(*args):
    print(var.get())

var.trace("w", callback)
option.place(
    x=64.0,
    y=220.0,
    width=174.0,
    height=36.0
)


#Create the drop it button
button_image_dropit = PhotoImage(
    file=relative_to_assets("dropit.png"))
button_dropit = Button(
    image=button_image_dropit,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:run_ffmpeg(),
    relief="flat"
)
button_dropit.place(
    x=64.0,
    y=340.0,
    width=174.0,
    height=34.0
)

#Create a label with text under drop it button
global label_process
label_process = Label(window, text="Status: Ready", fg="#010101", font=("Inter Bold", 12))
label_process.place(x=100, y=380)

#Check if FFMPEG is installed
def check_ffmpeg():
    try:
        subprocess.check_output(['ffmpeg', '-version'])
        return True
    except OSError:
        return False

if not check_ffmpeg():
    label_process['text'] = 'FFMPEG not found'
else:
    label_process['text'] = 'Status: Ready'


#Create the webhook entry field
webhook_entry = Entry(window)
webhook_entry.pack()
populate()
webhook_entry.place(
    x=64.0,
    y=280.0,
    width=174.0,
    height=36.0
)

#Create the Input button
button_image_input = PhotoImage(
    file=relative_to_assets("input.png"))
button_input = Button(
    image=button_image_input,
    borderwidth=0,
    highlightthickness=0,
    command=choose_video,
    relief="flat"
)
button_input.place(
    x=64.0,
    y=100.0,
    width=174.0,
    height=36.0
)

#Text for Discord Webhook
canvas.create_text(
    104.0,
    321.0,
    anchor="nw",
    text="Discord Webhook",
    fill="#010101",
    font=("Inter Bold", 12 * -1)
)

#Text for Select Encoder
canvas.create_text(
    104.0,
    260.0,
    anchor="nw",
    text="Select Encoder",
    fill="#010101",
    font=("Inter Bold", 12 * -1)
)

#Create the Update button
button_image_update = PhotoImage(
    file=relative_to_assets("update.png"))
button_update = Button(
    image=button_image_update,
    borderwidth=0,
    highlightthickness=0,
    command=update,
    relief="flat"
)
button_update.place(
    x=248.0,
    y=283.0,
    width=66.0,
    height=30.0
)


window.resizable(False, False)
window.mainloop()
