from pathlib import Path

import customtkinter as ctk
from customtkinter import filedialog
from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable

# Colors used in the program
red = "#8c1f1f"
dark_red = "#631a1a"
light_red = "#d14343"
grey = "#949a9f"
dark_grey = "#353639"
green = "#57c96c"

# Customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Main app
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Youtube video downloader")
        self.resizable(False, False)
        self.filename = "output"

        # Select directory
        def selectdir():
            self.filename = filedialog.askdirectory(
                initialdir=Path(__file__).parent.resolve()
            )
            self.selectdir.configure(text=self.filename)

        # Download video
        def download(val):
            yturl = self.urlentry.get()
            try:
                match val:
                    case 1:
                        video = YouTube(yturl, on_progress_callback=on_progress)
                        stream = video.streams.get_highest_resolution()
                        stream.download(output_path=self.filename)
                        self.status.configure(
                            text=f"{video.title} downloaded", text_color=green
                        )
                    case 2:
                        video = YouTube(yturl, on_progress_callback=on_progress)
                        stream = video.streams.get_lowest_resolution()
                        stream.download(output_path=self.filename)
                        self.status.configure(
                            text=f"{video.title} downloaded", text_color=green
                        )
                    case 3:
                        video = YouTube(yturl, on_progress_callback=on_progress)
                        stream = video.streams.get_audio_only()
                        stream.download(output_path=self.filename)
                        self.status.configure(
                            text=f"{video.title} downloaded", text_color=green
                        )
                    case _:
                        self.status.configure(
                            text="Error - Select an quality option",
                            text_color=light_red,
                        )
            except VideoUnavailable:
                self.status.configure(
                    text="Error - Video unavailable", text_color=light_red
                )

        # Download progress
        def on_progress(stream, chunk, bytes_remaining):

            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            perc_of_completion = bytes_downloaded / total_size * 100
            per = str(int(perc_of_completion))

            self.percentage.configure(text=f"{per}%")
            self.percentage.update()

            self.progressbar.set(float((perc_of_completion) / 100))

        # Main frame
        self.frame = ctk.CTkFrame(self, width=560, height=320, corner_radius=10)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title = ctk.CTkLabel(
            self.frame,
            text="youtube video downloader",
            width=365,
            height=28,
            font=("Inter", 28, "bold"),
            text_color=grey,
        )
        self.title.grid(row=0, column=0, columnspan=3, pady=(40, 0), padx=97)

        # Output folder
        self.selectdir = ctk.CTkLabel(
            self.frame,
            text="select the output folder",
            font=("Inter", 16),
            width=195,
            height=18,
            text_color=light_red,
        )
        self.selectdir.bind("<Button-1>", lambda e: (selectdir()))
        self.selectdir.grid(row=1, column=0, columnspan=3, pady=(14, 0))

        # Video url entry
        self.urlentry = ctk.CTkEntry(
            self.frame,
            width=460,
            height=35,
            font=("Inter", 20),
            corner_radius=3,
            placeholder_text="video url",
            text_color=grey,
            bg_color=dark_grey,
            border_color=grey,
        )
        self.urlentry.grid(row=2, column=0, columnspan=3, pady=(3, 0), padx=50)

        # Quality selector
        self.radio_var = ctk.IntVar(value=0)

        self.radio1 = ctk.CTkRadioButton(
            self.frame,
            text="High Quality",
            radiobutton_height=25,
            radiobutton_width=25,
            font=("Inter", 18),
            variable=self.radio_var,
            value=1,
            fg_color=red,
            hover_color=dark_red,
            text_color=grey,
        )
        self.radio2 = ctk.CTkRadioButton(
            self.frame,
            text="Low Quality",
            radiobutton_height=25,
            radiobutton_width=25,
            font=("Inter", 18),
            variable=self.radio_var,
            value=2,
            fg_color=red,
            hover_color=dark_red,
            text_color=grey,
        )
        self.radio3 = ctk.CTkRadioButton(
            self.frame,
            text="Audio Only",
            radiobutton_height=25,
            radiobutton_width=25,
            font=("Inter", 18),
            variable=self.radio_var,
            value=3,
            fg_color=red,
            hover_color=dark_red,
            text_color=grey,
        )

        self.radio1.grid(row=3, column=0, pady=(28, 0), padx=(50, 0))
        self.radio2.grid(row=3, column=1, pady=(28, 0), padx=(0, 0))
        self.radio3.grid(row=3, column=2, pady=(28, 0), padx=(0, 50))

        # Download button
        self.downloadbtn = ctk.CTkButton(
            self.frame,
            text="download",
            width=250,
            height=50,
            font=("Inter", 24, "bold"),
            corner_radius=10,
            fg_color=red,
            hover_color=dark_red,
            command=lambda: download(self.radio_var.get()),
        )
        self.downloadbtn.grid(row=4, column=0, columnspan=3, pady=(28, 0), padx=(150))

        # Percentage text
        self.percentage = ctk.CTkLabel(
            self.frame,
            text="",
            font=("Inter", 14),
            width=100,
            height=11,
            text_color=grey,
        )
        self.percentage.grid(row=5, column=0, columnspan=3, pady=(15, 3))

        # Progress bar
        self.progressbar = ctk.CTkProgressBar(
            self.frame, width=460, height=15, corner_radius=5, progress_color=red
        )
        self.progressbar.set(0)
        self.progressbar.grid(row=6, column=0, columnspan=3)

        # Status text
        self.status = ctk.CTkLabel(
            self.frame,
            text="",
            font=("Inter", 14),
            width=100,
            height=11,
            wraplength=400,
        )
        self.status.grid(row=7, column=0, columnspan=3, pady=(3, 30))


app = App()

# App loop
if __name__ == "__main__":
    app.mainloop()
