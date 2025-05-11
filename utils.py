
import tkinter as tk

class HoverButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = self["background"]
        self.hover_bg = "#637d9c"
        self.active_bg = "black"
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def on_enter(self, e):
        self["background"] = self.hover_bg
    
    def on_leave(self, e):
        self["background"] = self.default_bg
    
    def on_press(self, e):
        self["background"] = self.active_bg
    
    def on_release(self, e):
        self["background"] = self.hover_bg
