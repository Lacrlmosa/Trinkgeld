import customtkinter as ctk
import qrcode
import random
from io import BytesIO
from PIL import Image, ImageTk
import pygame

links = [
    "https://youtu.be/dQw4w9WgXcQ",
    "https://app.food2050.ch/de/toni-areal/mensa/food-profile/2024-12-09-mittagsverpflegung-simply-good"
]

pygame.mixer.init()
pygame.mixer.music.load("geld_sound.mp3")



ctk.set_appearance_mode("light")

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("600x700")

        self.fullscreen = False

        self.qr_label = ctk.CTkLabel(self.root, text="")
        self.qr_label.place(relx=0.5, rely=0.6, anchor="center")

        self.countdown_label = ctk.CTkLabel(self.root, text="", font=("Helvetica", 32, "bold"), text_color="black")
        self.countdown_label.place(relx=0.5, rely=0.9, anchor="center")

        self.heart_gif = Image.open("herz.gif")
        self.heart_frames = []
        self.load_heart_frames()

        self.heart_frame_index = 0
        self.heart_label = ctk.CTkLabel(self.root, text="")
        self.heart_label.place(relx=0.5, rely=0.5, anchor="center")

        self.text_gif = Image.open("text_animation.gif")
        self.text_gif_frames = []
        self.load_text_gif_frames()

        self.text_gif_frame_index = 0
        self.text_gif_label = ctk.CTkLabel(self.root, text="")
        self.text_gif_label.place(relx=0.5, rely=0.2, anchor="center")

        self.countdown_time =5

        self.root.bind('<F11>', self.toggle_fullscreen)  
        self.root.bind('<Return>', self.start_sequence)  

        self.animate_gif()

    def load_heart_frames(self):
        try:
            while True:
                frame = self.heart_gif.copy().resize((600, 600))
                self.heart_frames.append(ImageTk.PhotoImage(frame))
                self.heart_gif.seek(self.heart_gif.tell() + 1)
        except EOFError:
            pass

    def load_text_gif_frames(self):
        try:
            while True:
                frame = self.text_gif.copy().resize((700, 500))  
                self.text_gif_frames.append(ImageTk.PhotoImage(frame))
                self.text_gif.seek(self.text_gif.tell() + 1)
        except EOFError:
            pass

    def toggle_fullscreen(self, event=None):
        """Schaltet zwischen Vollbildmodus und Fenstermodus um."""
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def start_sequence(self, event=None):
        pygame.mixer.music.play()
        self.root.after(1000, self.hide_heart)

    def hide_heart(self):
        self.heart_label.place_forget()
        self.show_qr_code()

    def show_qr_code(self):
        link = random.choice(links)
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        bio = BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        qr_image = Image.open(bio)
        ctk_image = ctk.CTkImage(qr_image, size=(500, 500))

        self.qr_label.configure(image=ctk_image)
        self.qr_label.image = ctk_image

        self.text_gif_label.place(relx=0.5, rely=0.2, anchor="center")
        self.text_gif_active = True
        self.animate_text_gif()

        self.start_countdown(5)

    def animate_text_gif(self):
        if not self.text_gif_active:
            return 
        try:
            frame = self.text_gif_frames[self.text_gif_frame_index]
            self.text_gif_frame_index = (self.text_gif_frame_index + 1) % len(self.text_gif_frames)
            self.text_gif_label.configure(image=frame)
            self.text_gif_label.image = frame

            self.text_gif_animation_id = self.root.after(200, self.animate_text_gif)
        except IndexError:
            pass

    def start_countdown(self, seconds):
        self.countdown_time = seconds
        self.countdown_label.configure(text=str(self.countdown_time))
        self.update_countdown()

    def update_countdown(self):
        if self.countdown_time > 0:
            self.countdown_time -= 1
            self.countdown_label.configure(text=str(self.countdown_time))
            self.root.after(1000, self.update_countdown)
        else:
            self.reset_sequence()

    def reset_sequence(self):
        self.qr_label.configure(image=None)
        self.qr_label.image = None
        self.text_gif_label.configure(image=None)  
        self.text_gif_label.image = None           
        self.countdown_label.configure(text="")
        self.heart_label.place(relx=0.5, rely=0.5, anchor="center")

        self.text_gif_active = False
        if self.text_gif_animation_id is not None:
            self.root.after_cancel(self.text_gif_animation_id)
            self.text_gif_animation_id = None

        self.text_gif_label.place_forget()

    def animate_gif(self):
        try:
            frame = self.heart_frames[self.heart_frame_index]
            self.heart_frame_index = (self.heart_frame_index + 1) % len(self.heart_frames)
            self.heart_label.configure(image=frame)
            self.heart_label.image = frame
            self.root.after(400, self.animate_gif)  
        except IndexError:
            pass

root = ctk.CTk()
app = QRCodeApp(root)
root.mainloop()
