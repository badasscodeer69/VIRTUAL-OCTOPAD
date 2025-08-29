import cv2
import mediapipe as mp
import pygame
import sys
import time
import os

def main():
    print(f"[{time.strftime('%H:%M:%S')}] Starting Virtual Octopad...")

    # Initialize pygame for sound
    try:
        pygame.mixer.init()
        print(f"[{time.strftime('%H:%M:%S')}] Pygame mixer initialized.")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Warning: Failed to initialize pygame mixer: {e}. Continuing without sound.")

    # Load drum sounds (optional, with fallback)
    sound_files = [
        "kick.wav", "snare.wav", "hithat.wav", "tom01.wav",
        "tom02.wav", "crash.wav", "ride.wav", "clap.wav"
    ]
    sounds = []
    for sound_file in sound_files:
        if not os.path.exists(sound_file):
            print(f"[{time.strftime('%H:%M:%S')}] Warning: Sound file '{sound_file}' not found. Using silent placeholder.")
            sounds.append(None)
        else:
            try:
                sounds.append(pygame.mixer.Sound(sound_file))
                print(f"[{time.strftime('%H:%M:%S')}] Loaded sound: {sound_file}")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Warning: Error loading sound '{sound_file}': {e}. Using silent placeholder.")
                sounds.append(None)

    # Initialize MediaPipe Hands
    try:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        mp_draw = mp.solutions.drawing_utils
        print(f"[{time.strftime('%H:%M:%S')}] MediaPipe Hands initialized.")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error initializing MediaPipe: {e}")
        time.sleep(2)
        sys.exit(1)

    # Try webcam indices 0 and 1
    cap = None
    for index in [0, 1]:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"[{time.strftime('%H:%M:%S')}] Webcam opened with index {index}.")
            break
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Failed to open webcam with index {index}.")
    if not cap or not cap.isOpened():
        print(f"[{time.strftime('%H:%M:%S')}] Error: No webcam available. Tried indices 0 and 1.")
        time.sleep(2)
        sys.exit(1)

    # Get frame dimensions
    ret, frame = cap.read()
    if not ret or frame is None:
        print(f"[{time.strftime('%H:%M:%S')}] Error: Failed to capture initial frame.")
        cap.release()
        time.sleep(2)
        sys.exit(1)
    height, width = frame.shape[:2]
    print(f"[{time.strftime('%H:%M:%S')}] Frame dimensions: {width}x{height}")

    # Define 8 pads in a 2x4 grid with 80% size to reduce overlap
    pad_width = int(width // 4 * 0.8)
    pad_height = int(height // 2 * 0.8)
    pad_margin_x = int(width // 4 * 0.1)  # 10% margin between pads
    pad_margin_y = int(height // 2 * 0.1)
    pads = [
        ((i % 4) * (pad_width + pad_margin_x) + pad_margin_x, (i // 4) * (pad_height + pad_margin_y) + pad_margin_y, pad_width, pad_height)
        for i in range(8)
    ]
    last_triggered = [0] * 8
    debounce_time = 0.3  # Increased for better control

    print(f"[{time.strftime('%H:%M:%S')}] Entering main loop. Press 'q' to exit. Use index finger to trigger pads.")
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"[{time.strftime('%H:%M:%S')}] Error: Failed to capture frame in loop.")
                break

            # Flip frame and convert to RGB
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process frame with MediaPipe
            try:
                results = hands.process(rgb_frame)
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Error processing frame with MediaPipe: {e}")
                continue

            # Draw pads
            for i, (x, y, w, h) in enumerate(pads):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, f"Pad {i+1}", (x + 10, y + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Track index finger only and allow one pad per hand
            if results.multi_hand_landmarks:
                for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    # Use index finger tip (landmark 8)
                    idx = 8
                    x = int(hand_landmarks.landmark[idx].x * width)
                    y = int(hand_landmarks.landmark[idx].y * height)
                    cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                    # Check for pad hit, stop after first hit per hand
                    current_time = time.time()
                    for i, (px, py, pw, ph) in enumerate(pads):
                        if (px <= x <= px + pw and py <= y <= py + ph and
                                current_time - last_triggered[i] > debounce_time):
                            if sounds[i]:
                                sounds[i].play()
                                print(f"[{time.strftime('%H:%M:%S')}] Hand {hand_idx+1} triggered Pad {i+1}")
                            last_triggered[i] = current_time
                            cv2.rectangle(frame, (px, py), (px + pw, py + h),
                                          (0, 255, 255), -1)
                            break  # Only one pad per hand per frame

            # Display frame
            cv2.imshow('Virtual Octopad', frame)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(f"[{time.strftime('%H:%M:%S')}] User pressed 'q'. Exiting.")
                break

    except KeyboardInterrupt:
        print(f"[{time.strftime('%H:%M:%S')}] Program interrupted by user.")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Unexpected error in main loop: {e}")
    finally:
        if cap:
            cap.release()
        cv2.destroyAllWindows()
        hands.close()
        pygame.mixer.quit()
        print(f"[{time.strftime('%H:%M:%S')}] Resources released successfully.")
        time.sleep(2)

if __name__ == "__main__":
    main()