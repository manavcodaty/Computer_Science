import os
import random
import sys
import time
import tty
import termios

# List of fake hacking messages
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

# Terminal colors (ANSI escape codes)
COLORS = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"]
RESET = "\033[0m"

# Clear the terminal
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

# Hide cursor
def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

# Show cursor (for when exiting)
def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

# Stream fake hacking text
def stream_text(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        color = random.choice(COLORS)
        print(color + random.choice(MESSAGES) + RESET)
        time.sleep(random.uniform(0.1, 0.3))

# Flashing screen effect
def flash_screen(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        color_code = random.randint(40, 47)  # Background color codes (ANSI)
        sys.stdout.write(f"\033[{color_code}m\033[2J")  # Change background & clear screen
        sys.stdout.flush()
        time.sleep(0.1)

# Chaotic text stream
def chaotic_stream(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        color = random.choice(COLORS)
        text = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()", k=random.randint(20, 40)))
        print(color + text + RESET)
        time.sleep(random.uniform(0.05, 0.2))

# Fake shutdown sequence
def fake_shutdown():
    clear_screen()
    print("\033[91mSystem Error Detected...\033[0m")
    time.sleep(1)
    print("\033[91mShutting down in 3...\033[0m")
    time.sleep(1)
    print("\033[91mShutting down in 2...\033[0m")
    time.sleep(1)
    print("\033[91mShutting down in 1...\033[0m")
    time.sleep(1)
    clear_screen()
    print("\033[90mSystem Off\033[0m")
    time.sleep(2)
    clear_screen()

# Lockout mode (disable input except Ctrl+C)
def lockout():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)  # Disable normal keyboard input handling
        hide_cursor()
        while True:
            time.sleep(1)  # Keep running indefinitely
    except KeyboardInterrupt:
        show_cursor()
        sys.stdout.write("\033[0m\033[2J")  # Reset terminal colors
        print("\n\033[91m[ABORTED] Emergency Shut Down.\033[0m")
        sys.exit(0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Main function
def main():
    clear_screen()
    print("\033[92mInitializing hack...\nPress CTRL+C to abort.\033[0m")
    time.sleep(3)

    # Normal hacking messages (7 sec)
    stream_text(7)

    # Flashing effect (5 sec)
    flash_screen(5)

    # Chaotic text stream (6 sec)
    chaotic_stream(6)

    # Fake shutdown
    fake_shutdown()

    # Enter lockout mode (User can't exit except Ctrl+C)
    lockout()

# Run main function
if __name__ == "__main__":
    main()
