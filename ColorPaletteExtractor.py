import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # type: ignore
import colorsys
import random

class ColorPaletteExtractor:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Color Palette Extractor")
        self.master.geometry("800x900")
        self.master.configure(bg="#4169E1")  # Background color

        # Title Label
        self.title_label = tk.Label(
            self.master, text="Color Palette Extractor", font=("Arial", 18, "bold"), bg="#4169E1", fg="black"
        )
        self.title_label.pack(pady=10)

        # Image Upload Button
        self.upload_image_button = tk.Button(
            self.master, text="Upload Image", command=self.upload_image, font=("Arial", 12, "bold"), 
            bg="#8E44AD", fg="black", relief="raised", padx=10, pady=5
        )
        self.upload_image_button.pack(pady=5)

        # Image Display Label
        self.image_label = tk.Label(self.master, bg="#4169E1")
        self.image_label.pack(pady=5)

        # Color Palette Frame
        self.color_frame = tk.Frame(self.master, bg="#4169E1")
        self.color_frame.pack(pady=10)

        # Buttons for Color Combinations
        self.auto_generate_button = tk.Button(
            self.master, text="Auto-Generate Colors", command=self.auto_generate_combinations, font=("Arial", 12, "bold"),
            bg="#2ECC71", fg="black", relief="raised", padx=10, pady=5
        )
        self.auto_generate_button.pack(pady=5)

        self.gradient_galaxy_button = tk.Button(
            self.master, text="Gradient Galaxy", command=lambda: self.apply_color_scheme("gradient_galaxy"), 
            font=("Arial", 12, "bold"), bg="#2980B9", fg="black", relief="raised", padx=10, pady=5
        )
        self.gradient_galaxy_button.pack(pady=5)

        self.nature_green_button = tk.Button(
            self.master, text="Nature Green", command=lambda: self.apply_color_scheme("nature_green"), 
            font=("Arial", 12, "bold"), bg="#27AE60", fg="black", relief="raised", padx=10, pady=5
        )
        self.nature_green_button.pack(pady=5)

        self.color_swatches = []
        self.extracted_colors = []

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            self.display_image(file_path)  # Show the uploaded image
            self.extract_colors(file_path)  # Extract colors from the image

    def display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((250, 250))  # Resize for GUI
        photo = ImageTk.PhotoImage(image)
        
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep reference to avoid garbage collection

    def extract_colors(self, image_path):
        image = Image.open(image_path)
        image = image.resize((150, 150))  # Resize for faster processing
        result = image.convert('P', palette=Image.ADAPTIVE, colors=5)
        result = result.convert('RGB')
        colors = result.getcolors(150*150)
        colors.sort(reverse=True)
        
        self.extracted_colors = [color[1] for color in colors[:5]]  # Store extracted colors
        self.display_colors(self.extracted_colors)

    def display_colors(self, colors):
        for swatch in self.color_swatches:
            swatch.destroy()
        self.color_swatches = []

        for i, color in enumerate(colors):
            hex_color = "#{:02x}{:02x}{:02x}".format(*color)

            # Color Swatch
            swatch = tk.Label(self.color_frame, bg=hex_color, width=20, height=2)
            swatch.grid(row=i, column=0, pady=5)

            # RGB Label
            rgb_label = tk.Label(self.color_frame, text=f"RGB: {color}", bg="#4169E1", fg="black", font=("Arial", 10, "bold"))
            rgb_label.grid(row=i, column=1, padx=5)

            # Hex Label (Clickable)
            hex_label = tk.Label(self.color_frame, text=hex_color, bg="#4169E1", fg="black", font=("Arial", 10, "bold"), cursor="hand2")
            hex_label.grid(row=i, column=2, padx=5)
            hex_label.bind("<Button-1>", lambda e, hc=hex_color: self.copy_to_clipboard(hc))

            self.color_swatches.extend([swatch, rgb_label, hex_label])

    def copy_to_clipboard(self, hex_color):
        self.master.clipboard_clear()
        self.master.clipboard_append(hex_color)
        messagebox.showinfo("Copied!", f"Color {hex_color} copied to clipboard!")

    def auto_generate_combinations(self):
        if not self.extracted_colors:
            messagebox.showinfo("Info", "Please upload an image first.")
            return

        base_color = random.choice(self.extracted_colors)  # Pick a random base color
        h, s, v = colorsys.rgb_to_hsv(*[x/255 for x in base_color])

        # Generate a random color harmony rule
        harmony_type = random.choice(["complementary", "triadic", "analogous", "split_complementary"])
        
        if harmony_type == "complementary":
            new_colors = [(h, s, v), ((h + 0.5) % 1, s, v)]
        elif harmony_type == "triadic":
            new_colors = [(h, s, v), ((h + 0.33) % 1, s, v), ((h + 0.67) % 1, s, v)]
        elif harmony_type == "analogous":
            new_colors = [(h, s, v), ((h + 0.08) % 1, s, v), ((h - 0.08) % 1, s, v)]
        elif harmony_type == "split_complementary":
            new_colors = [(h, s, v), ((h + 0.5 - 0.1) % 1, s, v), ((h + 0.5 + 0.1) % 1, s, v)]

        generated_colors = [tuple(int(x * 255) for x in colorsys.hsv_to_rgb(*color)) for color in new_colors]
        self.display_colors(generated_colors)

    def apply_color_scheme(self, scheme):
        if scheme == "gradient_galaxy":
            colors = [(25, 25, 112), (75, 0, 130), (138, 43, 226), (255, 192, 203), (255, 20, 147)]
        elif scheme == "nature_green":
            colors = [(34, 139, 34), (0, 128, 0), (154, 205, 50), (85, 107, 47), (240, 230, 140)]
        self.display_colors(colors)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPaletteExtractor(root)
    root.mainloop()
