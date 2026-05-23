import tkinter as tk

class WireframeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Low-Fidelity Mobile Wireframer")
        self.root.geometry("450x650")
        self.root.configure(bg="#e0e0e0")

        # Application State
        self.current_tool = "box"  
        self.start_x = None
        self.start_y = None
        self.preview_id = None

        # Setup UI Components
        self.create_toolbar()
        self.create_canvas()
        self.create_statusbar()
        self.draw_default_template()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg="#222222", padx=5, pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        lbl = tk.Label(toolbar, text="Tools:", fg="white", bg="#222222", font=("Arial", 11, "bold"))
        lbl.pack(side=tk.LEFT, padx=5)

        tools = [("Image Box", "box"), ("Button", "button"), ("Text", "line"), ("Clear All", "clear")]
        for text, tool_id in tools:
            if tool_id == "clear":
                btn = tk.Button(toolbar, text=text, command=self.clear_canvas, bg="#ff3333", fg="white", font=("Arial", 9))
            else:
                btn = tk.Button(toolbar, text=text, command=lambda t=tool_id: self.set_tool(t), font=("Arial", 9))
            btn.pack(side=tk.LEFT, padx=3)

    def create_canvas(self):
        frame = tk.Frame(self.root, bg="#e0e0e0")
        frame.pack(expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(frame, width=320, height=500, bg="white", highlightbackground="#000000", highlightthickness=4)
        self.canvas.pack(pady=15, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def create_statusbar(self):
        self.status = tk.Label(self.root, text="Tool: Image Box | Click and drag INSIDE the white box to draw.", bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=5, pady=3, font=("Arial", 9))
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def set_tool(self, tool):
        self.current_tool = tool
        self.status.config(text=f"Tool: {tool.capitalize()} | Click and drag INSIDE the white box to draw.")

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_default_template(self):
        self.draw_box(10, 10, 310, 120)
        self.canvas.create_oval(20, 140, 80, 200, fill="#cccccc", outline="#999999", width=2)
        self.draw_line(100, 155, 280)
        self.draw_line(100, 175, 220)
        self.draw_button(10, 230, 310, 270)

    def draw_box(self, x1, y1, x2, y2):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f0f0f0", outline="#999999", width=2)
        self.canvas.create_line(x1, y1, x2, y2, fill="#cccccc")
        self.canvas.create_line(x1, y2, x2, y1, fill="#cccccc")

    def draw_button(self, x1, y1, x2, y2):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#dddddd", outline="#666666", width=1)
        self.canvas.create_text((x1 + x2)/2, (y1 + y2)/2, text="Action Button Element", fill="#333333", font=("Arial", 9, "bold"))

    def draw_line(self, x1, y1, x2):
        self.canvas.create_line(x1, y1, x2, y1, fill="#999999", width=6)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.current_tool in ["box", "button"]:
            self.preview_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="#333333", dash=(2, 2))
        elif self.current_tool == "line":
            self.preview_id = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill="#333333", dash=(2, 2))

    def on_drag(self, event):
        if self.preview_id:
            self.canvas.coords(self.preview_id, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        if self.preview_id:
            self.canvas.delete(self.preview_id)
        end_x, end_y = event.x, event.y
        if abs(end_x - self.start_x) < 5 and abs(end_y - self.start_y) < 5:
            return
        if self.current_tool == "box":
            self.draw_box(self.start_x, self.start_y, end_x, end_y)
        elif self.current_tool == "button":
            self.draw_button(self.start_x, self.start_y, end_x, end_y)
        elif self.current_tool == "line":
            self.draw_line(self.start_x, self.start_y, end_x)

if __name__ == "__main__":
    root = tk.Tk()
    app = WireframeApp(root)
    root.mainloop()
