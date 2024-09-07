import customtkinter as ctk
import tkinter as tk

# Create the main application window
app = ctk.CTk()

# Create a BooleanVar to track the state of the checkbox
checkbox_var = tk.BooleanVar()

# Function to handle checkbox state changes
def on_checkbox_toggle():
    if checkbox_var.get():
        print("Checkbox is checked")
    else:
        print("Checkbox is unchecked")

# Create a CTkCheckBox and associate it with the BooleanVar
checkbox = ctk.CTkCheckBox(
    master=app,
    text="Check me!",
    variable=checkbox_var,
    command=on_checkbox_toggle  # Call this function when the checkbox is toggled
)
checkbox.pack(pady=20)

# Run the application
app.mainloop()
