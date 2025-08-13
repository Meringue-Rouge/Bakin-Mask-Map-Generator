import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageEnhance
import webbrowser
import numpy as np

class BakinMaskMapGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bakin Mask Map Generator")
        self.root.resizable(False, False)

        # Language setting (default: English)
        self.language = tk.StringVar(value="en")
        self.translations = {
            "en": {
                "title": "Bakin Mask Map Generator",
                "albedo_label": "Select Albedo Texture (Required):",
                "emissive_label": "Select Emissive Texture (Optional):",
                "roughness_label": "Select Roughness Texture (Optional):",
                "metallic_label": "Select Metallic Texture (Optional):",
                "specular_label": "Select Specular Texture (Optional):",
                "normal_check": "Generate Normal Map",
                "generate_button": "Generate Mask Map and Textures",
                "progress_label": "Progress:",
                "progress_start": "Starting...",
                "progress_albedo": "Copied albedo texture",
                "progress_copy": "Copied {suffix} texture",
                "progress_generate": "Generated {suffix} texture",
                "progress_normal": "Generated normal map",
                "progress_mask": "Creating mask map",
                "progress_complete": "Completed",
                "footer_notice": "This application uses Pillow and NumPy for image processing.",
                "footer_link": "Made by Meringue Rouge",
                "language_button": "日本語",
                "error_albedo_missing": "Please select a valid albedo texture.",
                "error_albedo_read": "Failed to read albedo texture: {error}",
                "error_albedo_copy": "Failed to copy albedo texture: {error}",
                "error_texture": "Failed to process {suffix} texture: {error}",
                "error_normal": "Failed to generate normal map: {error}",
                "error_mask": "Failed to generate mask map.",
                "success_message": "Textures and mask map generated in {output_dir}"
            },
            "ja": {
                "title": "Bakinマスクマップジェネレーター",
                "albedo_label": "アルベドテクスチャを選択（必須）：",
                "emissive_label": "エミッシブテクスチャを選択（任意）：",
                "roughness_label": "ラフネステクスチャを選択（任意）：",
                "metallic_label": "メタリックテクスチャを選択（任意）：",
                "specular_label": "スペキュラテクスチャを選択（任意）：",
                "normal_check": "ノーマルマップを生成",
                "generate_button": "マスクマップとテクスチャを生成",
                "progress_label": "進行状況：",
                "progress_start": "開始中...",
                "progress_albedo": "アルベドテクスチャをコピーしました",
                "progress_copy": "{suffix}テクスチャをコピーしました",
                "progress_generate": "{suffix}テクスチャを生成しました",
                "progress_normal": "ノーマルマップを生成しました",
                "progress_mask": "マスクマップを作成中",
                "progress_complete": "完了",
                "footer_notice": "このアプリケーションはPillowとNumPyを使用して画像処理を行います。",
                "footer_link": "Meringue Rouge 製作",
                "language_button": "English",
                "error_albedo_missing": "有効なアルベドテクスチャを選択してください。",
                "error_albedo_read": "アルベドテクスチャの読み込みに失敗しました：{error}",
                "error_albedo_copy": "アルベドテクスチャのコピーに失敗しました：{error}",
                "error_texture": "{suffix}テクスチャの処理に失敗しました：{error}",
                "error_normal": "ノーマルマップの生成に失敗しました：{error}",
                "error_mask": "マスクマップの生成に失敗しました。",
                "success_message": "テクスチャとマスクマップが {output_dir} に生成されました"
            }
        }

        # Variables
        self.albedo_path = tk.StringVar()
        self.emissive_path = tk.StringVar()
        self.roughness_path = tk.StringVar()
        self.metallic_path = tk.StringVar()
        self.specular_path = tk.StringVar()
        self.generate_normal = tk.BooleanVar(value=False)

        # Style
        padding_opts = {'padx': 10, 'pady': 5}

        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Language toggle button
        self.widgets = {}
        self.widgets["language_button"] = ttk.Button(
            self.main_frame,
            text=self.translations["en"]["language_button"],
            command=self.toggle_language
        )
        self.widgets["language_button"].pack(anchor="w", **padding_opts)

        # Albedo texture selection
        self.widgets["albedo_label"] = ttk.Label(self.main_frame, text=self.translations["en"]["albedo_label"])
        self.widgets["albedo_label"].pack(anchor="w", **padding_opts)
        ttk.Entry(self.main_frame, textvariable=self.albedo_path, width=50).pack(**padding_opts)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file(self.albedo_path)).pack(**padding_opts)

        # Emissive texture selection
        self.widgets["emissive_label"] = ttk.Label(self.main_frame, text=self.translations["en"]["emissive_label"])
        self.widgets["emissive_label"].pack(anchor="w", **padding_opts)
        ttk.Entry(self.main_frame, textvariable=self.emissive_path, width=50).pack(**padding_opts)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file(self.emissive_path)).pack(**padding_opts)

        # Roughness texture selection
        self.widgets["roughness_label"] = ttk.Label(self.main_frame, text=self.translations["en"]["roughness_label"])
        self.widgets["roughness_label"].pack(anchor="w", **padding_opts)
        ttk.Entry(self.main_frame, textvariable=self.roughness_path, width=50).pack(**padding_opts)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file(self.roughness_path)).pack(**padding_opts)

        # Metallic texture selection
        self.widgets["metallic_label"] = ttk.Label(self.main_frame, text=self.translations["en"]["metallic_label"])
        self.widgets["metallic_label"].pack(anchor="w", **padding_opts)
        ttk.Entry(self.main_frame, textvariable=self.metallic_path, width=50).pack(**padding_opts)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file(self.metallic_path)).pack(**padding_opts)

        # Specular texture selection
        self.widgets["specular_label"] = ttk.Label(self.main_frame, text=self.translations["en"]["specular_label"])
        self.widgets["specular_label"].pack(anchor="w", **padding_opts)
        ttk.Entry(self.main_frame, textvariable=self.specular_path, width=50).pack(**padding_opts)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file(self.specular_path)).pack(**padding_opts)

        # Normal map generation checkbox
        self.widgets["normal_check"] = ttk.Checkbutton(self.main_frame, text=self.translations["en"]["normal_check"], variable=self.generate_normal)
        self.widgets["normal_check"].pack(anchor="w", **padding_opts)

        # Generate button
        self.generate_button = ttk.Button(self.main_frame, text=self.translations["en"]["generate_button"], command=self.generate_mask_map)
        self.generate_button.pack(pady=10)

        # Progress bar and label
        self.widgets["progress_label"] = ttk.Label(self.main_frame, text=self.translations["en"]["progress_label"])
        self.widgets["progress_label"].pack(anchor="w", **padding_opts)
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(**padding_opts)
        self.progress_label = ttk.Label(self.main_frame, text="")
        self.progress_label.pack(anchor="w", **padding_opts)

        # Separator
        ttk.Separator(self.main_frame, orient="horizontal").pack(fill="x", pady=10)

        # Footer frame
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill="x", side="bottom", pady=5)

        # Left side: Creator link
        self.widgets["footer_link"] = ttk.Label(footer_frame, text=self.translations["en"]["footer_link"], foreground="blue", cursor="hand2")
        self.widgets["footer_link"].pack(side="left", padx=10)
        self.widgets["footer_link"].bind("<Button-1>", lambda e: webbrowser.open_new("https://meringue-rouge.github.io/"))

        # Right side: Placeholder for logo (optional)
        self.logo_image = None
        logo_path = os.path.join(os.path.dirname(__file__), "software_logo.png")
        if os.path.exists(logo_path):
            try:
                raw_logo = Image.open(logo_path)
                max_logo_width = 100
                aspect_ratio = raw_logo.height / raw_logo.width
                scaled_width = min(raw_logo.width, max_logo_width)
                scaled_height = int(scaled_width * aspect_ratio)
                logo_resized = raw_logo.resize((scaled_width, scaled_height), Image.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(logo_resized)
                logo_label = tk.Label(footer_frame, image=self.logo_image, cursor="hand2", borderwidth=0)
                logo_label.pack(side="right", anchor="se", padx=10, pady=5)
                logo_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://meringue-rouge.github.io/"))
                raw_logo.close()
            except Exception as e:
                print(f"Error loading logo: {e}")

        # Notice centered
        self.widgets["footer_notice"] = ttk.Label(self.main_frame, text=self.translations["en"]["footer_notice"], font=("Arial", 8))
        self.widgets["footer_notice"].pack(pady=10)

        # Update window size
        self.root.update_idletasks()
        window_width = max(450, self.main_frame.winfo_reqwidth() + 20)
        window_height = self.main_frame.winfo_reqheight() + 20
        self.root.geometry(f"{window_width}x{window_height}")

    def toggle_language(self):
        """Toggle between English and Japanese UI text."""
        new_lang = "ja" if self.language.get() == "en" else "en"
        self.language.set(new_lang)
        self.widgets["language_button"].configure(text=self.translations[new_lang]["language_button"])
        self.root.title(self.translations[new_lang]["title"])
        for key, widget in self.widgets.items():
            if key != "language_button" and "{suffix}" not in self.translations[new_lang][key]:
                widget.configure(text=self.translations[new_lang][key])
        self.root.update_idletasks()
        window_width = max(450, self.main_frame.winfo_reqwidth() + 20)
        window_height = self.main_frame.winfo_reqheight() + 20
        self.root.geometry(f"{window_width}x{window_height}")

    def browse_file(self, path_var):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.tga *.bmp")])
        if file_path:
            path_var.set(file_path)

    def generate_normal_map(self, albedo_path, output_path):
        """Generate a simple normal map from the albedo texture using Sobel edge detection."""
        try:
            albedo = Image.open(albedo_path).convert("L")
            albedo_array = np.array(albedo)
            height, width = albedo_array.shape

            sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
            sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
            
            grad_x = np.zeros_like(albedo_array, dtype=float)
            grad_y = np.zeros_like(albedo_array, dtype=float)
            
            for i in range(1, height-1):
                for j in range(1, width-1):
                    grad_x[i, j] = np.sum(albedo_array[i-1:i+2, j-1:j+2] * sobel_x)
                    grad_y[i, j] = np.sum(albedo_array[i-1:i+2, j-1:j+2] * sobel_y)
            
            grad_x = (grad_x / np.max(np.abs(grad_x)) * 127.5 + 127.5).astype(np.uint8)
            grad_y = (grad_y / np.max(np.abs(grad_y)) * 127.5 + 127.5).astype(np.uint8)
            normal_z = np.ones_like(grad_x) * 255
            
            normal_map = np.stack([grad_x, grad_y, normal_z], axis=-1)
            normal_img = Image.fromarray(normal_map, "RGB")
            normal_img.save(output_path)
            normal_img.close()
            albedo.close()
        except Exception as e:
            messagebox.showerror("Error", self.translations[self.language.get()]["error_normal"].format(error=str(e)))
            raise

    def generate_roughness_map(self, albedo_path, output_path):
        """Generate a roughness map from the albedo (inverted grayscale with contrast)."""
        try:
            albedo = Image.open(albedo_path).convert("L")
            inverted = Image.eval(albedo, lambda x: 255 - x)
            enhancer = ImageEnhance.Contrast(inverted)
            roughness = enhancer.enhance(1.5)
            roughness.save(output_path)
            albedo.close()
            inverted.close()
            roughness.close()
        except Exception as e:
            messagebox.showerror("Error", self.translations[self.language.get()]["error_texture"].format(suffix="roughness", error=str(e)))
            raise

    def generate_specular_map(self, albedo_path, output_path):
        """Generate a specular map from the albedo (grayscale with high contrast)."""
        try:
            albedo = Image.open(albedo_path).convert("L")
            enhancer = ImageEnhance.Contrast(albedo)
            specular = enhancer.enhance(2.0)
            specular.save(output_path)
            albedo.close()
            specular.close()
        except Exception as e:
            messagebox.showerror("Error", self.translations[self.language.get()]["error_texture"].format(suffix="specular", error=str(e)))
            raise

    def create_mask_map(self, emissive_path, roughness_path, metallic_path, specular_path, output_path, albedo_size):
        """Create a Bakin mask map with emissive (R), roughness (G), metallic (B), and specular (A)."""
        width, height = albedo_size
        default_img = Image.new("L", (width, height), 0)

        try:
            emissive = Image.open(emissive_path).convert("L") if emissive_path and os.path.exists(emissive_path) else default_img.copy()
            roughness = Image.open(roughness_path).convert("L") if roughness_path and os.path.exists(roughness_path) else default_img.copy()
            metallic = Image.open(metallic_path).convert("L") if metallic_path and os.path.exists(metallic_path) else default_img.copy()
            specular = Image.open(specular_path).convert("L") if specular_path and os.path.exists(specular_path) else default_img.copy()

            if emissive.size != albedo_size:
                emissive = emissive.resize(albedo_size, Image.LANCZOS)
            if roughness.size != albedo_size:
                roughness = roughness.resize(albedo_size, Image.LANCZOS)
            if metallic.size != albedo_size:
                metallic = metallic.resize(albedo_size, Image.LANCZOS)
            if specular.size != albedo_size:
                specular = specular.resize(albedo_size, Image.LANCZOS)

            mask_map = Image.new("RGBA", albedo_size)
            mask_map_array = np.array(mask_map)

            mask_map_array[..., 0] = np.array(emissive)
            mask_map_array[..., 1] = np.array(roughness)
            mask_map_array[..., 2] = np.array(metallic)
            mask_map_array[..., 3] = np.array(specular)

            mask_map = Image.fromarray(mask_map_array, "RGBA")
            mask_map.save(output_path)

            emissive.close()
            roughness.close()
            metallic.close()
            specular.close()
            mask_map.close()
            default_img.close()
        except Exception as e:
            messagebox.showerror("Error", self.translations[self.language.get()]["error_mask"])
            return False
        return True

    def generate_mask_map(self):
        albedo_path = self.albedo_path.get()
        emissive_path = self.emissive_path.get()
        roughness_path = self.roughness_path.get()
        metallic_path = self.metallic_path.get()
        specular_path = self.specular_path.get()
        generate_normal = self.generate_normal.get()

        if not albedo_path or not os.path.exists(albedo_path):
            messagebox.showerror("Error", self.translations[self.language.get()]["error_albedo_missing"])
            return

        self.generate_button["state"] = "disabled"
        self.progress["value"] = 0
        self.progress_label["text"] = self.translations[self.language.get()]["progress_start"]
        self.root.update()

        total_steps = 6 + (1 if generate_normal else 0)
        step_increment = 100.0 / total_steps
        current_step = 0

        albedo_name = Path(albedo_path).stem
        output_dir = os.path.join(os.path.dirname(albedo_path), f"{albedo_name}_bakin_textures")
        os.makedirs(output_dir, exist_ok=True)

        try:
            albedo_img = Image.open(albedo_path)
            albedo_size = albedo_img.size
            albedo_img.close()
        except Exception as e:
            messagebox.showerror("Error", self.translations[self.language.get()]["error_albedo_read"].format(error=str(e)))
            self.generate_button["state"] = "normal"
            return

        try:
            albedo_output = os.path.join(output_dir, f"{albedo_name}_albedo.png")
            Image.open(albedo_path).save(albedo_output)
            current_step += 1
            self.progress["value"] = current_step * step_increment
            self.progress_label["text"] = self.translations[self.language.get()]["progress_albedo"]
            self.root.update()
        except Exception as e:
            messagebox.showerror("Error", self.translations[self.language.get()]["error_albedo_copy"].format(error=str(e)))
            self.generate_button["state"] = "normal"
            return

        texture_configs = [
            (emissive_path, "emissive", lambda p, o: Image.new("L", albedo_size, 0).save(o)),
            (roughness_path, "roughness", self.generate_roughness_map),
            (metallic_path, "metallic", lambda p, o: Image.new("L", albedo_size, 0).save(o)),
            (specular_path, "specular", self.generate_specular_map)
        ]

        for texture_path, suffix, generate_func in texture_configs:
            output_path = os.path.join(output_dir, f"{albedo_name}_{suffix}.png")
            try:
                if texture_path and os.path.exists(texture_path):
                    img = Image.open(texture_path)
                    if img.size != albedo_size:
                        img = img.resize(albedo_size, Image.LANCZOS)
                    img.save(output_path)
                    img.close()
                    self.progress_label["text"] = self.translations[self.language.get()]["progress_copy"].format(suffix=suffix)
                else:
                    generate_func(albedo_path, output_path)
                    self.progress_label["text"] = self.translations[self.language.get()]["progress_generate"].format(suffix=suffix)
                current_step += 1
                self.progress["value"] = current_step * step_increment
                self.root.update()
            except Exception as e:
                messagebox.showerror("Error", self.translations[self.language.get()]["error_texture"].format(suffix=suffix, error=str(e)))
                self.generate_button["state"] = "normal"
                return

        if generate_normal:
            normal_output = os.path.join(output_dir, f"{albedo_name}_normal.png")
            try:
                self.generate_normal_map(albedo_path, normal_output)
                current_step += 1
                self.progress["value"] = current_step * step_increment
                self.progress_label["text"] = self.translations[self.language.get()]["progress_normal"]
                self.root.update()
            except Exception:
                self.generate_button["state"] = "normal"
                return

        mask_output = os.path.join(output_dir, f"{albedo_name}_mask.png")
        self.progress_label["text"] = self.translations[self.language.get()]["progress_mask"]
        self.root.update()
        success = self.create_mask_map(
            os.path.join(output_dir, f"{albedo_name}_emissive.png"),
            os.path.join(output_dir, f"{albedo_name}_roughness.png"),
            os.path.join(output_dir, f"{albedo_name}_metallic.png"),
            os.path.join(output_dir, f"{albedo_name}_specular.png"),
            mask_output,
            albedo_size
        )

        if success:
            current_step += 1
            self.progress["value"] = current_step * step_increment
            self.progress_label["text"] = self.translations[self.language.get()]["progress_complete"]
            self.root.update()
            messagebox.showinfo("Success", self.translations[self.language.get()]["success_message"].format(output_dir=output_dir))
            self.root.quit()
        else:
            messagebox.showerror("Error", self.translations[self.language.get()]["error_mask"])
        self.generate_button["state"] = "normal"

if __name__ == "__main__":
    root = tk.Tk()
    app = BakinMaskMapGeneratorApp(root)
    root.mainloop()