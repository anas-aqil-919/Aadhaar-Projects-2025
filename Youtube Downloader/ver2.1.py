import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from yt_dlp import YoutubeDL
import re

# Function to download the video or playlist
# Function to download the video or playlist
def download_video():
    url = url_entry.get()
    download_path = path_entry.get()
    resolution = resolution_var.get()
    format_choice = format_var.get()
    subtitles = subtitles_var.get()
    is_playlist = playlist_var.get()

    if not url or not download_path:
        messagebox.showerror("Error", "Please provide both URL and download path.")
        return

    # Determine filename template
    if is_playlist:
        filename_template = f'{download_path}/%(playlist_index)s - %(title)s.%(ext)s'
    else:
        filename_template = f'{download_path}/%(title)s.%(ext)s'

    ydl_opts = {
        'outtmpl': filename_template,
        'merge_output_format': format_choice,
        'progress_hooks': [progress_hook],
    }

    if resolution != 'best':
        ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best'
    else:
        ydl_opts['format'] = 'best'

    if subtitles:
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitleslangs'] = ['en']

    ydl_opts['noplaylist'] = not is_playlist  # Download full playlist if checked

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to browse download path
def browse_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

# Progress Hook
def progress_hook(d):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0.0%')
        match = re.search(r'\d+\.\d+', percent_str)
        if match:
            percent = float(match.group())
            progress_bar['value'] = percent
            root.update_idletasks()
    elif d['status'] == 'finished':
        progress_bar['value'] = 100

# Main GUI
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("450x500")
root.configure(bg="#f0f4f8")

# Styling
def style_widget(widget, bg_color="#4CAF50", fg_color="white"):
    widget.configure(bg=bg_color, fg=fg_color, font=("Arial", 10, "bold"), bd=0, relief=tk.FLAT)

# Header
tk.Label(root, text="YouTube Downloader", bg="#4CAF50", fg="white", font=("Arial", 16, "bold"), pady=10).pack(fill=tk.X)

# Frame for Inputs
frame = tk.Frame(root, bg="#f0f4f8")
frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# URL Entry
tk.Label(frame, text="YouTube URL:", bg="#f0f4f8", anchor='w').pack(fill=tk.X)
url_entry = tk.Entry(frame, width=50, font=("Arial", 10), bd=2, relief=tk.GROOVE)
url_entry.pack(pady=5, fill=tk.X)

# Download Path
path_frame = tk.Frame(frame, bg="#f0f4f8")
path_frame.pack(pady=5, fill=tk.X)
path_entry = tk.Entry(path_frame, width=35, font=("Arial", 10), bd=2, relief=tk.GROOVE)
path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
browse_btn = tk.Button(path_frame, text="Browse", command=browse_path)
style_widget(browse_btn, "#007BFF")
browse_btn.pack(side=tk.LEFT, padx=5)

# Resolution Options
resolution_var = tk.StringVar(value='best')
tk.Label(frame, text="Select Resolution:", bg="#f0f4f8", anchor='w').pack(fill=tk.X)
resolutions = ['best', '1080', '720', '480', '360']
resolution_menu = tk.OptionMenu(frame, resolution_var, *resolutions)
resolution_menu.pack(pady=5, fill=tk.X)

# Format Selection
format_var = tk.StringVar(value='mp4')
tk.Label(frame, text="Select Format:", bg="#f0f4f8", anchor='w').pack(fill=tk.X)
formats = ['mp4', 'mkv', 'webm']
format_menu = tk.OptionMenu(frame, format_var, *formats)
format_menu.pack(pady=5, fill=tk.X)

# Subtitles Option
subtitles_var = tk.BooleanVar()
subtitles_check = tk.Checkbutton(frame, text="Download Subtitles", variable=subtitles_var, bg="#f0f4f8")
subtitles_check.pack(pady=5, anchor='w')

# Playlist Option
playlist_var = tk.BooleanVar()
playlist_check = tk.Checkbutton(frame, text="Download Playlist", variable=playlist_var, bg="#f0f4f8")
playlist_check.pack(pady=5, anchor='w')

# Progress Bar
progress_bar = ttk.Progressbar(frame, length=300, mode='determinate')
progress_bar.pack(pady=10, fill=tk.X)

# Download Button
download_btn = tk.Button(root, text="Download", command=download_video)
style_widget(download_btn, "#FF5722")
download_btn.pack(pady=20, padx=20, fill=tk.X)

root.mainloop()
