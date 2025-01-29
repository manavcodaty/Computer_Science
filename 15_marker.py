import os
import random
import sys
import time
import tty
import termios
import subprocess

# Fake hacking messages
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

# Clear screen
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

# Hide cursor
def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

# Show cursor (for exiting)
def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

# Beep randomly
def beep():
    sys.stdout.write("\a")
    sys.stdout.flush()

# Stream fake hacking text
def stream_text(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        print(random.choice(COLORS) + random.choice(MESSAGES) + RESET)
        time.sleep(random.uniform(0.03, 0.1))  # Ultra-fast output

# Flashing effect (super fast)
def flash_screen(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        color_code = random.randint(40, 47)  # Background color
        sys.stdout.write(f"\033[{color_code}m\033[2J")
        sys.stdout.flush()
        beep()
        time.sleep(0.02)  # Extremely fast flickering

# Chaotic ultra-fast text stream
def chaotic_stream(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        print(random.choice(COLORS) + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()", k=100)) + RESET)
        beep()
        time.sleep(random.uniform(0.01, 0.03))  # Insanely fast

# Fake shutdown with glitching text
def fake_shutdown():
    clear_screen()
    time.sleep(1)
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
        tty.setraw(fd)  # Disable normal keyboard input
        hide_cursor()
        while True:
            time.sleep(1)  # Keep running indefinitely
    except KeyboardInterrupt:
        show_cursor()
        sys.stdout.write("\033[0m\033[2J")  # Reset terminal colors
        sys.exit(0)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Relaunch script in a new fullscreen terminal window
def relaunch():
    if os.name == "posix":  # macOS/Linux
        subprocess.Popen(["osascript", "-e", 'tell application "Terminal" to do script "tput civis; python3 ' + sys.argv[0] + ' && exit"'])
    sys.exit(0)

# Main function (loops forever)
def main():
    while True:
        clear_screen()
        time.sleep(3)

        # Normal hacking messages (10 sec)
        stream_text(10)

        # Flashing effect (5 sec)
        flash_screen(5)

        # Chaotic text stream (6 sec)
        chaotic_stream(6)

        # Fake shutdown
        fake_shutdown()

        # Lock the user out
        lockout()

# Start in a new fullscreen window
if len(sys.argv) == 1:
    relaunch()
else:
    main()
