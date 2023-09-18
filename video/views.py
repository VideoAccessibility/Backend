from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Video as VideoModel
from questions.models import Question as QuestionModel
from .serializer import VideosSerializer
from rest_framework.renderers import JSONRenderer
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .core import main
import shutil
from pytube import YouTube
from user.jwt_users import JWT_Users
from descriptions.models import Description as DescriptionsModel

class Videos(APIView):

    def get(self, request):

        token = request.GET.get('jwt', '')
        # CHECK JWT TOKEN
        # token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token) #request.data.get('jwt')
        if not user:
            return Response({"videos": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        all_videos = VideoModel.objects.all()
        videos = []

        for v in range(len(all_videos)):
            serialized_video = VideosSerializer(all_videos[v])
            vid = JSONRenderer().render(serialized_video.data)
            videos.append(vid)
        return Response({"videos": videos}, status=status.HTTP_200_OK)



class Video(APIView):

    def get(self, request):

        token = request.GET.get('jwt', '')
        id = request.GET.get('id', '')
        # CHECK JWT TOKEN
        # token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            return Response({"video": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        # id = json.loads(request.body.decode('utf-8'))["id"]
        video = VideoModel.objects.filter(id=id)
        if len(video) > 0:
            serialized_video = VideosSerializer(video[0])
            return Response({"video": serialized_video.data}, status=status.HTTP_200_OK)
        else:
            return Response({"video": "NOT_FOUND"}, status=status.HTTP_200_OK)
    

def remove_video():
    if os.path.exists("videos/video.mp4"):
        os.remove("videos/video.mp4")
    filelist = [ f for f in os.listdir("videos/frames") if f.endswith(".jpg") ]
    for f in filelist:
        os.remove(os.path.join("videos/frames", f))


class QuestionAnswering(APIView):

    def post(self, request):

        # CHECK JWT TOKEN
        token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            return Response({"answer": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        id = json.loads(request.body.decode('utf-8'))["id"]
        question = json.loads(request.body.decode('utf-8'))["question"]
        currentTime = json.loads(request.body.decode('utf-8'))["currentTime"]
       
        video = VideoModel.objects.filter(id=id)
        if len(video) == 0:
            return Response({"answer": "VIDEO_NOT_FOUND"}, status=status.HTTP_200_OK)
       
        remove_video()
        shutil.copy(video[0].video_path, "videos/video.mp4")
        main.create_frames("videos/video.mp4") 

        if currentTime == '':
            currentTime = 0
        res = main.get_answer(question, currentTime)

        q = QuestionModel(video_id=id, time_stamp=currentTime, question=question, answer=res, username=user)
        q.save()

        return Response({"answer": res}, status=status.HTTP_200_OK)


class FileUpload(APIView):

    def post(self, request):   

        # CHECK JWT TOKEN
        token = request.POST.get('jwt')
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        file_obj = request.FILES['file']

        b = VideoModel(title=file_obj.name.split(".")[0], username=user)
        b.save()
        VideoModel.objects.filter(id=b.id).update(video_path=f"videos/{b.id}.mp4")

        ###
        remove_video()
        path = default_storage.save(f"videos/{b.id}.mp4", ContentFile(file_obj.read()))
        ff = default_storage.open(path)
        file_url = default_storage.url(path)
        print(ff, file_url)
        ###

        return Response({"status": "success"}, status=204)
    
import ffmpeg
import subprocess

class YoutubeDownloader(APIView):

    def post(self, request):   

        # CHECK JWT TOKEN
        token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN
        
        
        # TODO handle age-restricted
        # TODO handle wrong url/invalid url
        
        youtube_url = json.loads(request.body.decode('utf-8'))["youtube_url"]
        b = VideoModel(title=YouTube(youtube_url).title, username="TEST")
        b.save()
        youtube_video = YouTube(youtube_url).streams.filter(progressive=True, file_extension='mp4').first().download(f"/home/perl/video-description/video_accessibility/Description_generator/videos/", f"v_{b.id}.mp4")
        VideoModel.objects.filter(id=b.id).update(video_path=f"/home/perl/video-description/video_accessibility/Description_generator/videos/v_{youtube_video.split('/')[-1]}")

        duration = ffmpeg.probe(youtube_video)["streams"][1]['duration']
        frames = ffmpeg.probe(youtube_video)["streams"][1]['nb_frames']
        
        # anet_entities_test_1.json
        # {"v_test3": {"duration": 1209, "timestamps": [[0, 20], [20, 40]], "sentences": ["",""]}}
        # anet_duration_frame.csv
        # test3, 1209.00, 36228
        self.generateJSON(duration, youtube_video.split('/')[-1], frames)
        
        

        process = ["python", "/home/perl/video-description/video_accessibility/Description_generator/description_generator.py"]
        subprocess.call(process, cwd="/home/perl/video-description/video_accessibility/Description_generator/")


        with open('/home/perl/video-description/video_accessibility/Description_generator/results/anet_re_init_2023_05_09_18_14_25_0.5751435813568219/greedy_pred_test.json', 'r') as json_file:
            data = json.load(json_file)

        # Access the 'results' dictionary within the JSON data
        results = data.get('results', {})

        # Check if there are results and it's not empty
        if results:
            key = next(iter(results.keys()))
            # Access the 'v_44' dictionary within the 'results' dictionary
            result = results.get(key, [])

            # Iterate over the list of dictionaries inside 'v_44'
            for item in result:
                sentence = item.get('sentence', '')
                timestamps = item.get('timestamp', [])
                
                # Print the sentence and timestamps
                print(f"Sentence: {sentence}")
                print(f"Timestamps: {timestamps}")
                print()
                print(f"ID={b.id}")
                d = DescriptionsModel(video_id=b.id, time_stamp=f"{timestamps[0]}-{timestamps[1]}", descriptions=sentence, username="TEST")
                d.save()
        else:
            print("No results found in the JSON data.")

        # remove videos
        directory_paths = ['/home/perl/video-description/video_accessibility/Description_generator/videos',
        '/home/perl/video-description/video_accessibility/Description_generator/bbox',
        '/home/perl/video-description/video_accessibility/Description_generator/features/c3d_agent',
        '/home/perl/video-description/video_accessibility/Description_generator/features/c3d_env',
        '/home/perl/video-description/video_accessibility/Description_generator/features/lang_feature/frame_feature',
        '/home/perl/video-description/video_accessibility/Description_generator/features/lang_feature/lang_feature',
        '/home/perl/video-description/video_accessibility/Description_generator/mp4',
        '/home/perl/video-description/video_accessibility/Description_generator/rescaled',
        '/home/perl/video-description/video_accessibility/Description_generator/mid_frames',
        '/home/perl/video-description/video_accessibility/Description_generator/results/anet_re_init_2023_05_09_18_14_25_0.5751435813568219']
        
        for directory_path in directory_paths:
            try:
                # List all files in the directory
                files = os.listdir(directory_path)
                
                # Iterate through the files and remove them
                for file_name in files:
                    file_path = os.path.join(directory_path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Removed file: {file_path}")
                    if os.path.isdir(file_path):
                        os.remove(file_path)
                        print(f"Removed folder: {file_path}")

            except FileNotFoundError:
                print(f"The directory {directory_path} does not exist.")
            except PermissionError:
                print(f"Permission denied to remove files in {directory_path}.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        return Response({"status": "success"}, status=204)
          
    def generateJSON(self, duration, video_name, frames):
        # Define the JSON structure based on the input values
        json_data = {
            video_name.split('.')[0]: {
                "duration": duration,
                "timestamps": [],
                "sentences": []
            }
        }

        # Calculate timestamps based on the duration
        for start in range(0, int(float(duration)), 20):
            endtime = min(int(float(duration)), start+20)
            json_data[video_name.split('.')[0]]["timestamps"].append([start, endtime])
            json_data[video_name.split('.')[0]]["sentences"].append("")

        # Define the file path
        file_path = "/home/perl/video-description/video_accessibility/VLTinT/densevid_eval/anet_data/anet_entities_test_1.json"

        # Ensure the directory structure exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the JSON data to the file
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
            
        
        file_path = "/home/perl/video-description/video_accessibility/VLTinT/video_feature/anet_duration_frame.csv"
        # Ensure the directory structure exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the JSON data to the file
        with open(file_path, 'w') as json_file:
            json_file.write(video_name.split('.')[0][2:] + "," + duration + "," + frames)
            # json.dump(video_name.split('.')[0] + " " + duration + " " + frames, json_file)
        
        