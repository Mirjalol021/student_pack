import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from datetime import datetime
import random

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player - Spotify Style")
        self.root.geometry("1200x700")
        self.root.configure(bg="#121212")
        
        # Player state
        self.is_playing = False
        self.current_index = 0
        self.playlist = [
            {"title": "Midnight Dreams", "artist": "The Echoes", "duration": "4:56", "emoji": "🌙"},
            {"title": "Neon Lights", "artist": "Synthwave Dreams", "duration": "3:45", "emoji": "💡"},
            {"title": "Ocean Waves", "artist": "Coastal Vibes", "duration": "5:12", "emoji": "🌊"},
            {"title": "Urban Jungle", "artist": "City Beats", "duration": "4:03", "emoji": "🏙️"},
            {"title": "Starlight", "artist": "Night Sky", "duration": "3:28", "emoji": "⭐"},
            {"title": "Forest Echoes", "artist": "Nature Sounds", "duration": "4:30", "emoji": "🌲"},
            {"title": "Coffee Shop", "artist": "Ambient Vibes", "duration": "5:00", "emoji": "☕"},
            {"title": "Sunset Boulevard", "artist": "Evening Moods", "duration": "3:58", "emoji": "🌅"},
        ]
        
        self.shuffle_mode = False
        self.repeat_mode = 0  # 0: no repeat, 1: repeat all, 2: repeat one
        self.current_progress = 0
        self.total_duration = 296000  # 4:56 in milliseconds
        
        self.setup_ui()
        self.update_progress()
    
    def setup_ui(self):
        """Setup the UI layout"""
        # Main container
        main = tk.Frame(self.root, bg="#121212")
        main.pack(fill=tk.BOTH, expand=True)
        
        # Top Bar
        self.create_top_bar(main)
        
        # Content Area
        content = tk.Frame(main, bg="#121212")
        content.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.create_sidebar(content)
        
        # Player Area
        player = tk.Frame(content, bg="#121212")
        player.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Now Playing
        self.create_now_playing(player)
        
        # Queue
        self.create_queue(player)
        
        # Controls at bottom
        self.create_controls(self.root)
    
    def create_top_bar(self, parent):
        """Create top navigation bar"""
        top = tk.Frame(parent, bg="#1DB954", height=60)
        top.pack(fill=tk.X)
        
        label = tk.Label(top, text="♪ Music Player", font=("Helvetica", 18, "bold"),
                        bg="#1DB954", fg="#000000")
        label.pack(side=tk.LEFT, padx=20, pady=10)
    
    def create_sidebar(self, parent):
        """Create left sidebar with playlists"""
        sidebar = tk.Frame(parent, bg="#1F1F1F", width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Playlists title
        title = tk.Label(sidebar, text="PLAYLISTS", font=("Helvetica", 10, "bold"),
                        bg="#1F1F1F", fg="#FFFFFF")
        title.pack(padx=15, pady=15)
        
        playlists = [
            "Now Playing",
            "Favorites",
            "Recently Played",
            "Rock Classics",
            "Chill Vibes",
            "Party Mix",
            "Workout Mix"
        ]
        
        for playlist in playlists:
            btn = tk.Label(playlist, text=playlist, font=("Helvetica", 11),
                          bg="#1F1F1F", fg=("#1DB954" if playlist == "Now Playing" else "#FFFFFF"),
                          padx=15, pady=10, cursor="hand2")
            btn.pack(fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg="#1DB954"))
            btn.bind("<Leave>", lambda e, p=playlist, b=btn: 
                    b.config(fg="#1DB954" if p == "Now Playing" else "#FFFFFF"))
    
    def create_now_playing(self, parent):
        """Create now playing section"""
        frame = tk.Frame(parent, bg="#1F1F1F")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Album Art
        album = tk.Frame(frame, bg="#1DB954", width=250, height=250)
        album.pack(padx=20, pady=20)
        album.pack_propagate(False)
        
        emoji_label = tk.Label(album, text=self.playlist[0]["emoji"], 
                              font=("Helvetica", 80), bg="#1DB954", fg="#000000")
        emoji_label.pack(expand=True)
        
        # Song Info
        info_frame = tk.Frame(frame, bg="#1F1F1F")
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.song_title = tk.Label(info_frame, text=self.playlist[0]["title"],
                                   font=("Helvetica", 28, "bold"), bg="#1F1F1F", fg="#FFFFFF")
        self.song_title.pack(anchor=tk.W)
        
        self.artist_name = tk.Label(info_frame, text=self.playlist[0]["artist"],
                                    font=("Helvetica", 16), bg="#1F1F1F", fg="#B3B3B3")
        self.artist_name.pack(anchor=tk.W)
        
        # Progress Bar
        progress_frame = tk.Frame(frame, bg="#1F1F1F")
        progress_frame.pack(fill=tk.X, padx=20, pady=20)
        
        time_frame = tk.Frame(progress_frame, bg="#1F1F1F")
        time_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.current_time = tk.Label(time_frame, text="0:00", font=("Helvetica", 10),
                                     bg="#1F1F1F", fg="#B3B3B3")
        self.current_time.pack(side=tk.LEFT)
        
        self.duration_label = tk.Label(time_frame, text="4:56", font=("Helvetica", 10),
                                       bg="#1F1F1F", fg="#B3B3B3")
        self.duration_label.pack(side=tk.RIGHT)
        
        # Progress bar canvas
        canvas = tk.Canvas(progress_frame, bg="#404040", height=4, highlightthickness=0)
        canvas.pack(fill=tk.X, pady=5)
        self.progress_bar = canvas.create_rectangle(0, 0, 0, 4, fill="#1DB954", outline="")
        canvas.bind("<Button-1>", self.seek_progress)
    
    def create_queue(self, parent):
        """Create queue/playlist view"""
        frame = tk.Frame(parent, bg="#1F1F1F")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title = tk.Label(frame, text="QUEUE", font=("Helvetica", 12, "bold"),
                        bg="#1F1F1F", fg="#1DB954")
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Scrollable list
        list_frame = tk.Frame(frame, bg="#1F1F1F")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, bg="#1F1F1F", troughcolor="#1F1F1F")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_listbox = tk.Listbox(list_frame, bg="#282828", fg="#FFFFFF",
                                        yscrollcommand=scrollbar.set, 
                                        font=("Helvetica", 10), highlightthickness=0,
                                        selectmode=tk.SINGLE, selectbackground="#1DB954",
                                        selectforeground="#000000")
        self.queue_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.queue_listbox.bind("<Double-Button-1>", self.queue_double_click)
        scrollbar.config(command=self.queue_listbox.yview)
        
        # Populate queue
        for i, song in enumerate(self.playlist):
            display_text = f"  {song['title']} - {song['artist']}"
            self.queue_listbox.insert(tk.END, display_text)
        
        # Highlight current
        self.queue_listbox.itemconfig(0, bg="#1DB954", fg="#000000")
    
    def create_controls(self, parent):
        """Create playback controls at bottom"""
        control_frame = tk.Frame(parent, bg="#1F1F1F", height=100)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        control_frame.pack_propagate(False)
        
        buttons_frame = tk.Frame(control_frame, bg="#1F1F1F")
        buttons_frame.pack(expand=True)
        
        # Control buttons
        self.shuffle_btn = tk.Button(buttons_frame, text="🔀", font=("Helvetica", 16),
                                     bg="#282828", fg="#B3B3B3", activebackground="#1DB954",
                                     pady=10, padx=15, command=self.toggle_shuffle,
                                     highlightthickness=0, border=0)
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)
        
        self.prev_btn = tk.Button(buttons_frame, text="⏮", font=("Helvetica", 16),
                                  bg="#282828", fg="#FFFFFF", activebackground="#1DB954",
                                  pady=10, padx=15, command=self.previous_song,
                                  highlightthickness=0, border=0)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_btn = tk.Button(buttons_frame, text="▶", font=("Helvetica", 18),
                                  bg="#1DB954", fg="#000000", activebackground="#1ED760",
                                  pady=10, padx=20, command=self.toggle_play,
                                  highlightthickness=0, border=0)
        self.play_btn.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = tk.Button(buttons_frame, text="⏭", font=("Helvetica", 16),
                                  bg="#282828", fg="#FFFFFF", activebackground="#1DB954",
                                  pady=10, padx=15, command=self.next_song,
                                  highlightthickness=0, border=0)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.repeat_btn = tk.Button(buttons_frame, text="🔁", font=("Helvetica", 16),
                                    bg="#282828", fg="#B3B3B3", activebackground="#1DB954",
                                    pady=10, padx=15, command=self.toggle_repeat,
                                    highlightthickness=0, border=0)
        self.repeat_btn.pack(side=tk.LEFT, padx=5)
    
    def toggle_play(self):
        """Toggle play/pause"""
        self.is_playing = not self.is_playing
        self.play_btn.config(text="⏸" if self.is_playing else "▶")
    
    def previous_song(self):
        """Play previous song"""
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.playlist) - 1
        self.load_song()
    
    def next_song(self):
        """Play next song"""
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
        else:
            self.current_index = 0
        self.load_song()
    
    def toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.shuffle_mode = not self.shuffle_mode
        color = "#1DB954" if self.shuffle_mode else "#B3B3B3"
        self.shuffle_btn.config(fg=color)
    
    def toggle_repeat(self):
        """Cycle through repeat modes"""
        self.repeat_mode = (self.repeat_mode + 1) % 3
        colors = ["#B3B3B3", "#1DB954", "#1DB954"]
        texts = ["🔁", "🔁", "🔂"]
        self.repeat_btn.config(fg=colors[self.repeat_mode], text=texts[self.repeat_mode])
    
    def load_song(self):
        """Load and display a song"""
        song = self.playlist[self.current_index]
        self.song_title.config(text=song["title"])
        self.artist_name.config(text=song["artist"])
        self.duration_label.config(text=song["duration"])
        self.current_progress = 0
        self.current_time.config(text="0:00")
        
        # Update queue highlight
        self.queue_listbox.itemconfig(0, bg="#282828", fg="#FFFFFF")
        self.queue_listbox.itemconfig(self.current_index, bg="#1DB954", fg="#000000")
        
        if not self.is_playing:
            self.toggle_play()
    
    def seek_progress(self, event):
        """Seek in the song"""
        canvas = event.widget
        width = canvas.winfo_width()
        percent = event.x / width
        self.current_progress = int(percent * self.total_duration)
    
    def queue_double_click(self, event):
        """Handle queue item click"""
        selection = self.queue_listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.load_song()
    
    def update_progress(self):
        """Update progress bar and time"""
        if self.is_playing:
            self.current_progress += 50
            if self.current_progress >= self.total_duration:
                self.next_song()
                self.current_progress = 0
        
        # Update UI
        progress_percent = (self.current_progress / self.total_duration)
        
        # Update listbox (simulating canvas progress bar)
        seconds = self.current_progress // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        self.current_time.config(text=f"{minutes}:{seconds:02d}")
        
        self.root.after(50, self.update_progress)


if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
