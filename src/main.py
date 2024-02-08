import random
import time
import pygame
import os
from pydub import AudioSegment
from pydub.playback import play

pygame.init()

AUDIO_DIR = "../audio"

def apply_random_effect(sound):
    effect_type = random.choice(["QSB", "QRN", "QRM"])
    if effect_type == "QSB":
        fade_length = random.randint(500, 2000)  # Fade length in milliseconds (0.5 - 2 seconds)
        sound = sound.fade_out(fade_length)
    elif effect_type == "QRN":
        noise_level = random.randint(-30, -10)  # Noise level in decibels (10 - 30 dB)
        noise = AudioSegment.silent(duration=len(sound))
        noise = noise.overlay(AudioSegment.from_file(os.path.join(AUDIO_DIR, "qrn.mp3")).apply_gain(noise_level))
        sound = sound.overlay(noise)
    elif effect_type == "QRM":
        noise_level = random.randint(-20, 0)  # Noise level in decibels (0 - 20 dB)
        noise = AudioSegment.silent(duration=len(sound))
        noise = noise.overlay(AudioSegment.from_file(os.path.join(AUDIO_DIR, "qrm.mp3")).apply_gain(noise_level))
        sound = sound.overlay(noise)
    return sound

def play_sound(file_name):
    sound = AudioSegment.from_file(os.path.join(AUDIO_DIR, file_name))
    sound = apply_random_effect(sound)
    play(sound)  # Wait until the sound finishes playing

def generate_numbers(length):
    return [str(random.randint(0, 9)) for _ in range(length)]

def read_numbers(numbers):
    for number in numbers:
        play_sound(f"{number}.mp3")
        time.sleep(0.5)  # Delay for 0.5 seconds between numbers

def play_transmission_sound():
    play_sound("transmission.mp3")

def play_after_transmission_sound():
    play_sound("after_transmission.mp3")

try:
    while True:
        play_transmission_sound()
        number_sequence = generate_numbers(random.randint(5, 10))
        print("Transmitting numbers:", " ".join(number_sequence))
        read_numbers(number_sequence)
        play_after_transmission_sound()
        time.sleep(5)
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")
    pygame.quit()
