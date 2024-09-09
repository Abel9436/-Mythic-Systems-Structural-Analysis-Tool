import customtkinter as ctk
import tkinter as tk

class CircularProgressBar(ctk.CTkFrame):
    def __init__(self, parent, size=100, thickness=10, speed=10, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.size = size
        self.thickness = thickness
        self.speed = speed
        self.angle = 0

        # Create a Canvas to draw the circular arc
        self.canvas = tk.Canvas(self, width=self.size, height=self.size, highlightthickness=0, bg="white")
        self.canvas.pack(expand=True, fill="both")

        # Create the arc for the spinner
        self.arc = self.canvas.create_arc(
            self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
            start=0, extent=150, style="arc", outline="#4C7766", width=self.thickness
        )

        # Start the animation
        self.animate()
        
    def animate(self):
        
        # Increment the angle and rotate the arc
        self.angle = (self.angle + self.speed) % 360
        self.canvas.itemconfig(self.arc, start=self.angle)
        # Continue the animation
        self.after(50, self.animate)


# Example usage of the CircularProgressBar in a customtkinter window
# def main():
#     root = ctk.CTk()
#     root.geometry("400x400")
#     root.title("CustomTkinter Circular Progress Indicator")

#     # Create a CircularProgressBar widget and add it to the window
#     progress = CircularProgressBar(root, size=150, thickness=15, speed=10)
#     progress.pack(expand=True)

#     root.mainloop()

# if __name__ == "__main__":
#     main()
