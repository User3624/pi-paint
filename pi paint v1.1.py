import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageTk, ImageDraw

class PiPaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Paint")

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.brush_size = 5
        self.brush_color = "black"

        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), color="white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.controls = tk.Frame(root)
        self.controls.pack()

        tk.Button(self.controls, text="Change Color", command=self.pick_color).pack(side=tk.LEFT)
        tk.Button(self.controls, text="Load Pi Image", command=self.load_pi_image).pack(side=tk.LEFT)
        tk.Button(self.controls, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT)
        tk.Button(self.controls, text="Save Image", command=self.save_image).pack(side=tk.LEFT)

        self.size_slider = tk.Scale(self.controls, from_=1, to=20, orient=tk.HORIZONTAL, label="Brush Size")
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.LEFT)

        self.old_x = None
        self.old_y = None
        self.pi_image = None

    def paint(self, event):
        if self.old_x and self.old_y:
            x, y = event.x, event.y
            self.canvas.create_line(self.old_x, self.old_y, x, y, width=self.brush_size, fill=self.brush_color, capstyle=tk.ROUND)
            self.draw.line([self.old_x, self.old_y, x, y], fill=self.brush_color, width=self.brush_size)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def pick_color(self):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), color="white")
        self.draw = ImageDraw.Draw(self.image)

    def load_pi_image(self):
        try:
            img = Image.open("assets\pi.png")
            img = img.resize((300, 300))
            self.pi_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=self.pi_image)
            self.image.paste(img, (self.canvas_width // 2 - 150, self.canvas_height // 2 - 150))
        except Exception as e:
            print(f"Error loading image: {e}")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)
            print(f"Image saved to {file_path}")

root = tk.Tk()
app = PiPaintApp(root)
root.mainloop()
