import os
import random
import sys
import time
import tkinter as tk
import threading
import termios
import tty

# Hacking messages
MESSAGES = [
    "ACCESS GRANTED...",
    "Brute force attack initiated...",
    "Decrypting passwords...",
    "Firewall bypassed...",
    "Injecting rootkit...",
    "Transferring 2TB of sensitive data...",
    "Self-destruct sequence initiated...",
    "Wiping all system logs...",
    "Dark web connection established...",
    "Deploying ransomware...",
    "BIOS override in progress...",
    "Zero-day exploit activated...",
    "Remote access established...",
    "Erasing master boot record...",
]

# Terminal colors
COLORS = ["red", "green", "blue", "yellow", "purple", "cyan", "white"]

# Hide cursor
def disable_cursor():
    os.system("xsetroot -cursor empty")  # Hides cursor forever

# Restore cursor on exit
def restore_cursor():
    os.system("xsetroot -cursor default")  # Restores cursor

# Play random beeping noises
def play_noise():
    while True:
        time.sleep(random.uniform(0.5, 3))
        os.system("osascript -e 'beep'")

# Create fullscreen, unclosable window
def create_window():
    root = tk.Tk()
    root.configure(bg="black")
    root.attributes("-fullscreen", True)  # Fullscreen
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing
    root.bind("<Escape>", lambda e: None)  # Block Esc key

    text = tk.Label(root, text="", font=("Courier", 20), fg="green", bg="black")
    text.pack(expand=True)

    def update_text():
        while True:
            text.config(text=random.choice(MESSAGES), fg=random.choice(COLORS))
            root.update()
            time.sleep(random.uniform(0.05, 0.2))

    threading.Thread(target=update_text, daemon=True).start()

    root.mainloop()

# Fake shutdown with glitching
def fake_shutdown():
    os.system("clear")
    time.sleep(1)
    print("\033[91mSystem Error Detected...\033[0m")
    time.sleep(1)
    print("\033[91mShutting down in 3...\033[0m")
    time.sleep(1)
    print("\033[91mShutting down in 2...\033[0m")
    time.sleep(1)
    print("\033[91mShutting down in 1...\033[0m")
    time.sleep(1)
    os.system("clear")
    print("\033[90mSystem Off\033[0m")
    time.sleep(3)
    os.system("clear")

# Fake BIOS Boot Screen
def fake_bios():
    os.system("clear")
    print("\033[94mAmerican Megatrends Inc.\033[0m")
    time.sleep(1)
    print("\033[97mCopyright (C) 2023 All Rights Reserved.\033[0m")
    time.sleep(1)
    print("\n\033[92mInitializing Boot Sequence...\033[0m")
    time.sleep(2)
    print("\033[96mLoading Kernel...\033[0m")
    time.sleep(2)
    print("\033[91mERROR: UNAUTHORIZED ACCESS DETECTED!\033[0m")
    time.sleep(1)
    print("\033[91mEntering Emergency BIOS Recovery Mode...\033[0m")
    time.sleep(2)
    print("\033[97mFlashing BIOS Firmware...\033[0m")
    time.sleep(3)
    print("\033[91mERROR: FIRMWARE CORRUPTED!\033[0m")
    time.sleep(2)
    print("\033[93mRebooting System...\033[0m")
    time.sleep(3)
    os.system("clear")

# Lock keyboard input (except Ctrl + C)
def lockout():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)  # Disable normal keyboard input
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        restore_cursor()
        os.system("clear")
        sys.exit(0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Start chaos (running in background threads)
def start_chaos():
    disable_cursor()
    threading.Thread(target=play_noise, daemon=True).start()

    while True:
        fake_shutdown()
        fake_bios()
        time.sleep(10)

# Main program loop, GUI on main thread
def main():
    # Create the window on the main thread
    threading.Thread(target=create_window, daemon=True).start()
    
    # Start the chaos in background threads
    start_chaos()

# Run the main function
if __name__ == "__main__":
    main()
