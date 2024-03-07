import openai
import cv2
import base64
from openai import OpenAI

API_KEY = "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" #"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"
openai.api_key = API_KEY

def create_descriptions(video_path):
    video = cv2.VideoCapture(video_path)
    
    base64Frames = []
    seconds_per_frame = 1  # Assuming 1 second per frame, adjust according to your video's frame rate
    
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
    
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append((base64.b64encode(buffer).decode("utf-8"), round(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)))
    
    video.release()
    print(len(base64Frames), "frames read.")
    
    frame_count = 0
    frames = []
    while frame_count < len(base64Frames):
        if frame_count % 300 == 0:
            frames.append(base64Frames[frame_count])
        frame_count += 1
    
    # Create batches of 10 frames
    batch_size = 10
    frame_batches = [frames[i:i + batch_size] for i in range(0, len(frames), batch_size)]
    
    descriptions = []
    seconds_list = []
    
    for batch in frame_batches:
        PROMPT_MESSAGES = [
            {
                "role": "user",
                "content": [
                    "These are frames from a video. Generate Audio descriptions for the scene. Focus on providing meaningful details for a blind user. Generate complete audio description. Include information about on-screen text, characters, setting, and relevant details to enhance the overall experience for a blind user. As these descriptions will be spoken for the second of the video they describe, I want the descriptions to sound as if they are part of a continuous narrative rather than segmented into distinct frames or images. Return each description in a new line",
                    *map(lambda x: {"image": x[0], "resize": 768}, batch),
                ],
            },
        ]
        params = {
            "model": "gpt-4-vision-preview",
            "messages": PROMPT_MESSAGES,
            "max_tokens": 1000,
        }
    
        result = openai.chat.completions.create(**params)
        description_content = result.choices[0].message.content
        descriptions.append(description_content)
    
        # Extract seconds from the batch
        seconds_list.extend([frame[1] for frame in batch])
    
    # Split each description into sentences
    result = [sentence.strip() for description in descriptions for sentence in description.split('\n') if sentence]
    
    # Output the result and seconds_list
    print("Descriptions:", result)
    print("Seconds List:", seconds_list)
    return (result, seconds_list)
    
def ask_question(video_path, question, current_moment):
    video = cv2.VideoCapture(video_path)
    
    base64Frames = []
    seconds_per_frame = 1  # Assuming 1 second per frame, adjust according to your video's frame rate
    
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
    
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append((base64.b64encode(buffer).decode("utf-8"), round(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)))
    
    video.release()
    print(len(base64Frames), "frames read.")
    
    frame_count = 0
    frames = []
    while frame_count < len(base64Frames):
        if frame_count % 300 == 0:
            frames.append(base64Frames[frame_count])
        frame_count += 1
    
    # Create batches of 10 frames
    batch_size = 10
    frame_batches = [frames[i:i + batch_size] for i in range(0, len(frames), batch_size)]
    
    answer = []
    seconds_list = []
    
    for batch in frame_batches:
        PROMPT_MESSAGES = [
            {
                "role": "user",
                "content": [
                    f"These are frames from a video. Please answer to the question short, consice and to the point about the video. Focus on providing meaningful details for a blind user (without mentioning the frame number). Now, the blind user stopped the video on frame number {current_moment} to ask the question. Question: {question}",
                    *map(lambda x: {"image": x[0], "resize": 768}, batch),
                ],
            },
        ]
        params = {
            "model": "gpt-4-vision-preview",
            "messages": PROMPT_MESSAGES,
            "max_tokens": 1000,
        }
    
        result = openai.chat.completions.create(**params)
        description_content = result.choices[0].message.content
        answer.append(description_content)
    
    # Output the answer
    print("Answer:", answer[0])
    return answer[0]