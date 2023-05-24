from moviepy.editor import VideoFileClip
import time
import cv2
import numpy as np
import os
import pygame
from pydub import AudioSegment
from pydub.playback import play




video_path = ""
video_res_x = 0
video_res_y = 0
video_fps = 0
video_duration = 0
video_frames = 0

time_to_frame = 0
frame_count = 0
clear = lambda: os.system('cls')

framex = 0
framey = 0



def options():
    print("\nPlease insert video path:")
    print("Ex. [C:/Users/User/Desktop/video.mp4] or [./video.mp4]")
    path = input("> ")

    print("\nSelect the resolution (The higher the resolution, the lower the fps)")
    print("0 > 64 x 48 (extemely low)")
    print("1 > 128 x 72 (low)")
    print("2 > 192 x 108 (default)")
    print("3 > 256 x 144 (high)")
    print("4 > 384 x 216 (extremely high)")
    res = input("> ")
    if res == "0":
        x = 64
        y = 48
    elif res == "1":
        x = 128
        y = 72
    elif res == "3":
        x = 256
        y = 144
    elif res == "4":
        x = 384
        y = 216
    else:
        x = 192
        y = 108

    return path, x, y


def get_data(file):
    video = VideoFileClip(file)
    fps = video.fps
    duration = video.duration
    frames = round(fps * duration)
    video.close()
    return round(fps,2), duration, frames

def show_properties():
    print("\n///// PROPERTIES /////")
    print(f"FPS: {video_fps}")
    print(f"Duration: {video_duration}s")
    print(f"Total frames: {video_frames}")
    print("//////////////////////\n")

def show_ascii_frame(video_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Can't open the video")
        return
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    if not ret:
        print("Can't read the frame")
        return
    
    cap.release()
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (framex, framey))  # Adjust the frame size
    
   
    ascii_chars = " .,'`^_~!;:=-+*@80oO@&%$#@"
    
    ascii_frame = ""
    for row in frame:
        for pixel in row:
            ascii_frame += ascii_chars[pixel // 10]*2  # 256 / 10 = 25.6 -> There are 26 chars in the palette
        ascii_frame += '\n'
    
    print(ascii_frame)
    

def howtouse():
    print("+----------------- HOW TO USE ----------------+")
    print("| Use the mouse-wheel to adjust the font size |")
    print("|  and resize the window to enjoy your video  |")
    print("+---------------------------------------------+\n")

def play_audio():
    audio_path = "temp_audio.wav"  # Nombre del archivo de audio temporal
    
    if os.path.exists(audio_path):
        os.remove(audio_path)

    video = VideoFileClip(video_path)
    audio = video.audio
    
    audio.write_audiofile(audio_path)  # Guarda el archivo de audio temporal

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()



video_path, framex, framey = options()
print(f"{framex}x{framey}")

video_fps, video_duration, video_frames = get_data(video_path)
time_to_frame = 1 / video_fps
show_properties()
howtouse()
play_video = input("Play? [Y/n] > ")
if (play_video != "n" and play_video != "N"):
    play_audio()
    frame_sum = 0
    delta = 0
    delta_init = time.time()
    while frame_count < video_frames:
        frame_sum += delta/time_to_frame
        frame_count = round(frame_sum)


        delta = time.time() - delta_init
        delta_init = time.time()
        
        #print(f"Frame {frame_count}") #Debug
        #print(f"Delta {delta}")
        #print(f"Time {time_to_frame}")
        show_ascii_frame(video_path,frame_count)
        

        time.sleep(time_to_frame)
else:
    exit()