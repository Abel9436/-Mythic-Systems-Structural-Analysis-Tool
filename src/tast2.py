import customtkinter as ctk

# Create a root window
root = ctk.CTk()

# Create a button
button = ctk.CTkButton(root, text="Click Me")

# Disable the button
button.configure(state=ctk.DISABLED)

# Pack the button into the window
button.pack()

# Run the application
root.mainloop()
