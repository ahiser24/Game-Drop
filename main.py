# Game Drop is used to quickly share 30 second gaming clips with friends on Discord.
# A local copy is saved to the inputs folder



from pathlib import Path

#Tkinter requirements
from tkinter import *
from tkinter import filedialog, messagebox
from discord_webhook import DiscordWebhook
import os
import subprocess
import wmi
import time
import json

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

# Populate the text field with the last Discord Webhook from output.json
def populate():
    global content
    try:
        with open("output.json", "r") as f:
            data = json.load(f)
            content = data.get("webhook_url", "")
    except FileNotFoundError:
        content = ""

    webhook_entry.insert(END, content)
    return content

# Save the Discord webhook to the file output.json
def update():
    global content
    content = webhook_entry.get()
    data = {"webhook_url": content}
    with open('output.json', 'w') as f:
        json.dump(data, f)
    
    label_process['text'] = 'Discord Webhook Updated'
    label_process.update()
    time.sleep(2)
    label_process['text'] = 'Status: Ready'
    return content

#Define Variables
video_input = ""
save_location = ""
video_name = ""
nvidia = "h264_nvenc"
amd = "h264_amf"
cpu = "libvpx-vp9"


#Choose video file for input buttton
def choose_video():
    global video_input
    video_input = filedialog.askopenfilename(title = "Select video", filetypes = (("MP4 files", "*.mp4"),("All files", "*.*")))
    determine_save_location
    print(video_input)

#Set the save location to the same folder as the video input
def determine_save_location():
    global save_location, video_name  # Indicate these are global

    if video_input:
        original_dir = os.path.dirname(video_input)
        default_filename = os.path.basename(video_input).split('.')[0] + "_converted.mp4"
        save_location = os.path.join(original_dir, default_filename)
        video_name = os.path.basename(save_location)

    else:
        # Since there's no choice possible, handle this situation directly
        messagebox.showerror('Error', 'Please select an input video first.')

# Takes the encoded video file and sends it to Discord using the webhook provided.
def send_file():
    global content, save_location

    if not content:
        label_process['text'] = 'Completed'
        label_process.update()
        return

    file_size = os.path.getsize(save_location)
    
    #Check if file is under 25MB limit
    if file_size / 1024 > 25600:
        label_process['text'] = 'Adjusting encoding...'
        label_process.update()

        # Retry with a lower bitrate
        subprocess.run([ffmpeg_path, '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', nvidia, '-vf', 'scale=1920:1080', '-an', '-b:v', '5000k', '-pass', '1', '-2pass', '1', save_location], shell=True)
        subprocess.run([ffmpeg_path, '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input, '-c:v', nvidia, '-vf', 'scale=1920:1080', '-acodec', 'copy', '-b:v', '5000k', '-pass', '2', '-2pass', '1', '-y', save_location], shell=True)
        
        file_size = os.path.getsize(save_location)

        if file_size / 1024 > 25600:
            # If adjusted encoding fails, don't send.
            messagebox.showerror('Error', 'Adjusted file size is still too large to send')
            label_process['text'] = 'Adjustment failed'
        else:
            # Successfully adjusted encoding
            with open(save_location, 'rb') as f:
                webhook = DiscordWebhook(url=content, username='Game Drop')
                webhook.add_file(file=f.read(), filename=video_name)
                response = webhook.execute()
                label_process['text'] = 'Completed'

    else:
        # File size is within the limit, send as is
        with open(save_location, 'rb') as f:
            webhook = DiscordWebhook(url=content, username='Game Drop')
            webhook.add_file(file=f.read(), filename=video_name)
            response = webhook.execute()
            label_process['text'] = 'Completed'



# Call PowerShell script for FFMPEG conversion and update the status label
def run_ffmpeg():
    #Declare a global variable for the ffmpeg path
    global ffmpeg_path
    label_process['text'] = 'Encoding. Please wait...'
    label_process.update()
    button_dropit.config(relief='sunken')
    if not video_input:
        messagebox.showerror('Error', 'No Video file selected')
        button_dropit.config(relief='flat')
        label_process['text'] = 'Status: Ready'
        return
    else:
        ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Bin', 'FFMPEG', 'ffmpeg.exe')  # Add this line
        determine_save_location()
        option_selected(save_location)
        button_dropit.config(relief='flat')
        label_process['text'] = 'Status: Ready'


# Drop Down Menu actions for Encoder
def option_selected(save_location):
    global value, video_input, video_name, content, ffmpeg_path

    value = var.get()
    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Bin', 'FFMPEG', 'ffmpeg.exe')

    gpu_checks = {
        "NVIDIA": (nvidia_result, "NVIDIA GPU not detected", nvidia, nvidia),
        "AMD": (amd_result, "AMD GPU not detected", amd, amd),
        "CPU": (None, None, cpu, cpu)
    }

    gpu_check, gpu_not_detected_msg, pass_1_encoder, pass_2_encoder = gpu_checks.get(value, (None, None, None, None))

    if gpu_check is not None and not gpu_check:
        label_process['text'] = gpu_not_detected_msg
        label_process.update()
        time.sleep(2)
        return  # Stop the script

    # Pass 1
    subprocess.run([ffmpeg_path, '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input,
                    '-c:v', pass_1_encoder, '-vf', 'scale=1920:1080', '-an', '-b:v', '6000k', '-pass', '1', '-2pass', '-1', save_location], shell=True)
    # Pass 2
    subprocess.run([ffmpeg_path, '-y', '-loglevel', '0', '-nostats', '-sseof', '-30', '-i', video_input,
                    '-c:v', pass_2_encoder, '-vf', 'scale=1920:1080', '-acodec', 'copy', '-b:v', '6000k', '-pass', '2', '-2pass', '-1', '-y', save_location], shell=True)
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
    y=202.0,
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

# Check if FFMPEG is installed
def check_ffmpeg():
    global ffmpeg_path

    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Bin', 'FFMPEG', 'ffmpeg.exe')

    try:
        subprocess.check_output([ffmpeg_path, '-version'])
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
    y=142.0,
    width=174.0,
    height=36.0
)

#Text for Discord Webhook
canvas.create_text(
    100.0,
    317.0,
    anchor="nw",
    text="Discord Webhook",
    fill="#010101",
    font=("Inter", 10, "bold")
)

#Text for Select Encoder
canvas.create_text(
    100.0,
    238.0,
    anchor="nw",
    text="Select Encoder",
    fill="#010101",
    font=("Inter", 10, "bold")
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
