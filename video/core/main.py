from datetime import timedelta
import cv2
import numpy as np
import os
from PIL import Image
from transformers import pipeline


SAVING_FRAMES_PER_SECOND = 10
FINAL_SAVING_FRAMES_PER_SECOND = 10

# vqa_pipeline = pipeline("visual-question-answering")

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")
 

def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


# def main(video_file):
#     frames_counter = 0
#     filename, _ = os.path.splitext(video_file)
#     filename += ""
#     # make a folder by the name of the video file
#     # if not os.path.isdir(filename):
#     #     os.mkdir(filename)
#     # read the video file    
#     cap = cv2.VideoCapture(video_file)
#     # get the FPS of the video
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
#     saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
#     FINAL_SAVING_FRAMES_PER_SECOND = saving_frames_per_second
#     # get the list of duration spots to save
#     saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
#     # start the loop
#     count = 0
#     while True:
#         is_read, frame = cap.read()
#         if not is_read:
#             # break out of the loop if there are no frames to read
#             break
#         # get the duration by dividing the frame count by the FPS
#         frame_duration = count / fps
#         try:
#             # get the earliest duration to save
#             closest_duration = saving_frames_durations[0]
#         except IndexError:
#             # the list is empty, all duration frames were saved
#             break
#         if frame_duration >= closest_duration:
#             # if closest duration is less than or equals the frame duration, 
#             # then save the frame
#             frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
#             cv2.imwrite(os.path.join(os.getcwd(), f"videos/frames/{frames_counter}.jpg"), frame) 
#             frames_counter += 1
#             # drop the duration spot from the list, since this duration spot is already saved
#             try:
#                 saving_frames_durations.pop(0)
#             except IndexError:
#                 pass
#         # increment the frame count
#         count += 1
        

# def create_frames(video_path):
#     main("videos/video.mp4")


# def get_answer(question, currentTime):
#     ##
#     cap = cv2.VideoCapture("videos/video.mp4")
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     FINAL_SAVING_FRAMES_PER_SECOND = min(fps, SAVING_FRAMES_PER_SECOND)
#     print("saving_frames_per_second", FINAL_SAVING_FRAMES_PER_SECOND)
#     start_frame = (currentTime-5)*FINAL_SAVING_FRAMES_PER_SECOND
#     end_frame = (currentTime)*FINAL_SAVING_FRAMES_PER_SECOND
#     print("time", currentTime, start_frame, end_frame)
#     ##
#     max_score = 0
#     best_answer = "Nothing has found"
#     print(os.getcwd())
#     for file in os.listdir("videos/frames"):
#         file_num = int(file.replace(".jpg", ""))
#         if file_num < start_frame:
#             continue
#         if file_num > end_frame:
#             continue
#         image =  Image.open(os.path.join(os.getcwd(), f"videos/frames/{file}")) 
#         res = vqa_pipeline(image, question, top_k=1)[0]
#         print(file, res)

#         if max_score < res["score"] * (file_num - start_frame) * (file_num - start_frame):
#             best_answer = res["answer"]
#             max_score = res["score"] * (file_num - start_frame) * (file_num - start_frame)

#     print(max_score, best_answer)
#     return best_answer
