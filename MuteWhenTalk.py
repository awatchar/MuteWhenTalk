"""
Title: Dynamic Audio Mute Toggle
Description: This script allows users to mute and unmute their system's audio output dynamically using a specified key. 
             It leverages the 'pycaw' library for controlling the system's audio and the 'keyboard' library for capturing key presses and releases.
Usage:
    1. Run the script in a Python environment where 'keyboard' and 'pycaw' libraries are installed.
    2. When prompted, press and release the key you wish to use for muting and unmuting the audio. Keep the key pressed for a moment to set it.
    3. Once set, you can press and hold the designated key to mute the audio. Releasing the key will unmute the audio.
    4. The script will provide feedback in the console indicating the current audio state ("Audio muted." or "Audio unmuted.") each time the key is pressed or released.
    5. To stop the script, use the keyboard interrupt shortcut (usually Ctrl+C in the terminal).

Requirements:
    - Python 3.x
    - pycaw library: Install via pip with `pip install pycaw`
    - keyboard library: Install via pip with `pip install keyboard`
      Note: Running scripts that listen to keyboard events may require administrative privileges.

Author: [Your Name]
Date: YYYY-MM-DD
Version: 1.0

Note: This script is designed for educational and practical purposes, allowing users to control their audio settings directly from their keyboard.
      The author assumes no responsibility for any misuse or damage caused by this script.
"""

import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Initialize the audio controller
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# This flag will help us to mute the audio only once per key press
is_audio_muted = False

# Function to mute audio
def mute_audio():
    global is_audio_muted
    if not is_audio_muted:
        volume.SetMute(1, None)
        print("Audio muted.")
        is_audio_muted = True

# Function to unmute audio
def unmute_audio():
    global is_audio_muted
    if is_audio_muted:
        volume.SetMute(0, None)
        print("Audio unmuted.")
        is_audio_muted = False

def detect_and_bind_mute_key():
    print("Please press and release the key you want to use for muting (keep it pressed for a moment)...")
    
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        user_key = event.name
        # Ensuring the key is released before proceeding (to avoid immediate toggling)
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_UP and event.name == user_key:
                break

        print(f"The '{user_key}' key has been set as your mute/unmute toggle.")
        
        # Bind the detected key to mute on press and unmute on release
        keyboard.on_press_key(user_key, lambda _: mute_audio())
        keyboard.on_release_key(user_key, lambda _: unmute_audio())

        print(f"Press and hold the '{user_key}' key to mute, and release to unmute.")
        return user_key
    else:
        return None

def main():
    user_key = detect_and_bind_mute_key()
    if user_key:
        # Keep the script running
        keyboard.wait()

if __name__ == "__main__":
    main()
