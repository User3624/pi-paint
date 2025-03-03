import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from tkinter import Menu
from PIL import Image, ImageTk, ImageDraw

class PiPaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Paint")

        # Create a menu bar
        self.menu_bar = Menu(root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save Image", command=self.save_image)  # Save Image added here
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # About Menu
        self.about_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="About Pi Paint", command=self.show_about)

        # Canvas setup (300x300 to fit Pi image)
        self.canvas_size = 300
        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Brush settings
        self.brush_size = 5
        self.brush_color = "black"
        self.is_eraser = False

        # Image creation for saving
        self.base_image = Image.new("RGB", (self.canvas_size, self.canvas_size), color="white")
        self.drawing_image = Image.new("RGBA", (self.canvas_size, self.canvas_size), color=(255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.drawing_image)

        # Bind mouse events for drawing
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Controls on the right
        self.controls = tk.Frame(root)
        self.controls.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Button(self.controls, text="Change Color", command=self.pick_color).pack(side=tk.TOP, fill=tk.X, pady=5)
        tk.Button(self.controls, text="Load Pi Image", command=self.load_pi_image).pack(side=tk.TOP, fill=tk.X, pady=5)
        tk.Button(self.controls, text="Clear", command=self.clear_canvas).pack(side=tk.TOP, fill=tk.X, pady=5)
        tk.Button(self.controls, text="Eraser", command=self.toggle_eraser).pack(side=tk.TOP, fill=tk.X, pady=5)
        tk.Button(self.controls, text="Pencil", command=self.toggle_pencil).pack(side=tk.TOP, fill=tk.X, pady=5)

        self.size_slider = tk.Scale(self.controls, from_=1, to=20, orient=tk.HORIZONTAL, label="Brush Size", command=self.update_brush_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Drawing variables
        self.old_x = None
        self.old_y = None
        self.pi_image = None

    def update_brush_size(self, event=None):
        self.brush_size = self.size_slider.get()

    def paint(self, event):
        if self.old_x and self.old_y:
            x, y = event.x, event.y
            if self.is_eraser:
                self.canvas.create_line(self.old_x, self.old_y, x, y, width=self.brush_size, fill="white", capstyle=tk.ROUND)
                self.draw.line([self.old_x, self.old_y, x, y], fill=(255, 255, 255, 0), width=self.brush_size)
            else:
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
        self.base_image = Image.new("RGB", (self.canvas_size, self.canvas_size), color="white")
        self.drawing_image = Image.new("RGBA", (self.canvas_size, self.canvas_size), color=(255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.drawing_image)

    def load_pi_image(self):
        try:
            img = Image.open("assets/pi.png")
            img = img.resize((self.canvas_size, self.canvas_size))  # Ensure the image fits the canvas
            self.pi_image = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            # Center the Pi image on the canvas
            self.canvas.create_image(self.canvas_size // 2, self.canvas_size // 2, image=self.pi_image)

            self.base_image.paste(img, (0, 0))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")

    def toggle_eraser(self):
        self.is_eraser = True

    def toggle_pencil(self):
        self.is_eraser = False

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                # Composite only the drawing on the Pi image, not the full canvas
                final_image = Image.alpha_composite(self.base_image.convert("RGBA"), self.drawing_image.convert("RGBA"))

                # Convert to RGB before saving if needed and ensure it's 300x300
                final_image = final_image.convert("RGB")
                final_image = final_image.resize((self.canvas_size, self.canvas_size))  # Ensure it's 300x300

                final_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving image: {e}")

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                img = Image.open(file_path)
                img = img.resize((self.canvas_size, self.canvas_size))
                self.pi_image = ImageTk.PhotoImage(img)

                self.canvas.delete("all")
                self.canvas.create_image(self.canvas_size // 2, self.canvas_size // 2, image=self.pi_image)

                self.base_image.paste(img, (0, 0))
            except Exception as e:
                messagebox.showerror("Error", f"Error opening image: {e}")

    def show_about(self):
        messagebox.showinfo("About", "Pi Paint - A simple drawing app with Pi symbol\nCreated by User3624")

# Run the App
root = tk.Tk()
app = PiPaintApp(root)
root.mainloop()
