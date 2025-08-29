# VIRTUAL-OCTOPAD
A hand-tracking-based virtual drum kit built with OpenCV, MediaPipe, and Pygame.
Play an octopad (8 drum pads) using your hands in front of a webcam — no physical drum kit required! 🥁✨

🚀 Features

🎥 Webcam-based hand tracking using MediaPipe

🖐️ Detects index finger position to trigger pads

🟦 2x4 Grid of 8 pads displayed on screen

🔊 Each pad plays a unique drum sound (kick, snare, hihat, toms, crash, ride, clap)

⏱️ Debounce system to prevent accidental multiple triggers

❌ Graceful error handling (missing sounds, no webcam, etc.)

🖥️ Press q to exit

📂 Project Structure

               VIRTUAL_OCTOPAD/
                │── octopad.py          # Main Python script
                │── kick.wav            # Drum sounds
                │── snare.wav
                │── hithat.wav
                │── tom01.wav
                │── tom02.wav
                │── crash.wav
                │── ride.wav
                │── clap.wav
                

🛠️ Installation

Clone this repository

    git clone https://github.com/badasscoder69/VIRTUAL-OCTOPAD.git
    cd virtual-octopad


Install dependencies
Make sure you have Python 3.8+ installed. Then run:

    pip install opencv-python mediapipe pygame


Run the project

    python octopad.py

🎮 How to Play

    Make sure your webcam is connected.
    
    Run the script → a window opens with 8 pads drawn.
    
    Use your index finger to hit different pads:
    
    Each pad = different drum sound.
    
    To exit → press q.



⚡ Requirements

    Python 3.8+
    
    OpenCV
    
    MediaPipe
    
    Pygame

📝 Future Improvements

    Add custom sound mapping (user can assign their own sounds)
    
    Multi-hand simultaneous pad hits
    
    Visual effects (glow/animations on pad hit)
    
    Recording and playback functionality
