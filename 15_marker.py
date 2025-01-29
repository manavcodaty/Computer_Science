import os
import random
import sys
import time

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
    "BIOS override in progress..."
]

# Terminal colors (ANSI escape codes)
COLORS = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"]
RESET = "\033[0m"

# Clear the terminal
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

# Stream fake hacking text
def stream_text():
    try:
        while True:
            color = random.choice(COLORS)
            print(color + random.choice(MESSAGES) + RESET)
            time.sleep(random.uniform(0.1, 0.3))
    except KeyboardInterrupt:
        print("\n\033[91m[ABORTED] Connection Terminated.\033[0m")
        sys.exit(0)

# Flashing screen effect
def flash_screen():
    try:
        while True:
            color_code = random.randint(40, 47)  # Background color codes (ANSI)
            sys.stdout.write(f"\033[{color_code}m\033[2J")  # Change background & clear screen
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        sys.stdout.write("\033[0m\033[2J")  # Reset terminal colors
        print("\n\033[91m[ABORTED] Emergency Shut Down.\033[0m")
        sys.exit(0)

# Main function
def main():
    clear_screen()
    print("\033[92mInitializing hack...\n\033[0m")
    time.sleep(3)

    # Start normal text streaming
    for _ in range(5):  # Display normal messages before flashing starts
        print("\033[92m" + random.choice(MESSAGES) + RESET)
        time.sleep(random.uniform(0.2, 0.5))

    # Enter flashing mode
    flash_screen()

# Run main function
if __name__ == "__main__":
    main()
