import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

class ISpyAi:
    def __init__(self, root):
        self.root = root
        self.root.title("iSpyAi")

        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        self.console_frame = tk.Frame(self.root)
        self.console_frame.pack()

        self.console_label = tk.Label(self.console_frame, text="I spy...")
        self.console_label.pack(side=tk.LEFT)

        self.user_input = tk.Entry(self.console_frame)
        self.user_input.pack(side=tk.LEFT)

        self.submit_button = tk.Button(self.console_frame, text="Submit", command=self.on_submit)
        self.submit_button.pack(side=tk.LEFT)

        self.image_path = "Images/iSpyImage1.jpeg"
        self.image = self.load_image(self.image_path)

    def load_image(self, img_path):
        img = Image.open(img_path)
        img = img.resize((600, 400))
        self.img_tk = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.img_tk)
        self.img_label.image = self.img_tk
        return np.array(img)

    def on_submit(self):
        item = self.user_input.get()
        print(f"Ai is looking for: {item}")
        template_path = f"Templates/{item}.png"
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        top_left = self.find_object(self.image, template)
        h, w, _ = template.shape
        self.draw_box(self.image, top_left, w, h)

    def find_object(self, image, template):
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        return max_loc

    def draw_box(self, image, top_left, width, height):
        cv2.rectangle(image, top_left, (top_left[0] + width, top_left[1] + height), (255, 0, 0), 2)
        img_tk = ImageTk.PhotoImage(Image.fromarray(image))
        self.img_label.config(image=img_tk)
        self.img_label.image = img_tk


if __name__ == "__main__":
    root = tk.Tk()
    app = ISpyAi(root)
    root.mainloop()