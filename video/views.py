from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Video as VideoModel
from .serializer import VideosSerializer
from rest_framework.renderers import JSONRenderer
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .core import main
import shutil
from pytube import YouTube

class Videos(APIView):

    def get(self, request):
        print(request.body)
        all_videos = VideoModel.objects.all()
        videos = []
        for v in range(len(all_videos)):
            serialized_video = VideosSerializer(all_videos[v])
            vid = JSONRenderer().render(serialized_video.data)
            videos.append(vid)
        return Response({"videos": videos}, status=status.HTTP_200_OK)



class Video(APIView):

    def get(self, request):
        print(request.body)
        id = json.loads(request.body.decode('utf-8'))["id"]
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
        print(request.body)
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
        return Response({"answer": res}, status=status.HTTP_200_OK)


class FileUpload(APIView):

    def post(self, request):   
        file_obj = request.FILES['file']

        b = VideoModel(title=file_obj.name.split(".")[0])
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
    

class YoutubeDownloader(APIView):

    def post(self, request):   
        youtube_url = json.loads(request.body.decode('utf-8'))["youtube_url"]
        b = VideoModel(title=YouTube(youtube_url).title)
        b.save()
        youtube_video = YouTube(youtube_url).streams.filter(progressive=True, file_extension='mp4').first().download(f"videos", f"{b.id}.mp4")
        VideoModel.objects.filter(id=b.id).update(video_path=f"videos/{youtube_video.split('/')[-1]}")

        return Response({"status": "success"}, status=204)