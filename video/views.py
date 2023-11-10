from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Video as VideoModel
from questions.models import Question as QuestionModel
from questions.serializer import QuestionSerializer
from .serializer import VideosSerializer
from rest_framework.renderers import JSONRenderer
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .core import main
import shutil
from pytube import YouTube
from user.jwt_users import JWT_Users
import cv2
import os
from yt_dlp import YoutubeDL
import shutil


class Videos(APIView):
    def get(self, request):
        token = request.GET.get("jwt", "")
        # CHECK JWT TOKEN
        # token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)  # request.data.get('jwt')
        if not user:
            user = ""
            # return Response({"videos": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        all_videos = VideoModel.objects.all()
        videos = []

        for v in range(len(all_videos)):
            if (
                all_videos[v].public_or_private == "public"
                or all_videos[v].username == user
            ):
                serialized_video = VideosSerializer(all_videos[v])
                vid = JSONRenderer().render(serialized_video.data)
                videos.append(vid)
        return Response({"videos": videos}, status=status.HTTP_200_OK)


class Video(APIView):
    def get(self, request):
        token = request.GET.get("jwt", "")
        id = request.GET.get("id", "")
        # CHECK JWT TOKEN
        # token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            user = ""
            # return Response({"video": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        # id = json.loads(request.body.decode('utf-8'))["id"]
        video = VideoModel.objects.filter(id=id)
        if len(video) > 0:
            if video[0].public_or_private == "public" or video[0].username == user:
                serialized_video = VideosSerializer(video[0])
                return Response(
                    {"video": serialized_video.data}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"video": "PERMISSION_DENIED"}, status=status.HTTP_200_OK
                )
        else:
            return Response({"video": "NOT_FOUND"}, status=status.HTTP_200_OK)


def remove_video():
    if os.path.exists("videos/video.mp4"):
        os.remove("videos/video.mp4")
    filelist = [f for f in os.listdir("videos/frames") if f.endswith(".jpg")]
    for f in filelist:
        os.remove(os.path.join("videos/frames", f))


class QuestionAnswering(APIView):
    def post(self, request):
        # CHECK JWT TOKEN
        token = json.loads(request.body.decode("utf-8"))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            return Response({"answer": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        id = json.loads(request.body.decode("utf-8"))["id"]
        question = json.loads(request.body.decode("utf-8"))["question"]
        currentTime = json.loads(request.body.decode("utf-8"))["currentTime"]

        video = VideoModel.objects.filter(id=id)
        if len(video) == 0:
            return Response({"answer": "VIDEO_NOT_FOUND"}, status=status.HTTP_200_OK)

        remove_video()
        shutil.copy(video[0].video_path, "videos/video.mp4")
        main.create_frames("videos/video.mp4")

        if currentTime == "":
            currentTime = 0
        res = main.get_answer(question, currentTime)

        q = QuestionModel(
            video_id=id,
            time_stamp=currentTime,
            question=question,
            answer=res,
            username=user,
        )
        q.save()

        return Response({"answer": res}, status=status.HTTP_200_OK)

    def get(self, request):
        token = request.GET.get("jwt", "")
        id = request.GET.get("id", "")
        # CHECK JWT TOKEN
        # token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            user = ""
            # return Response({"questions": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        # id = json.loads(request.body.decode('utf-8'))["id"]
        questions = QuestionModel.objects.filter(video_id=id)
        questions_lst = []
        if len(questions) > 0:
            # serialized_question = QuestionSerializer(questions[0])
            for v in range(len(questions)):
                serialized_question = QuestionSerializer(questions[v])
                qid = JSONRenderer().render(serialized_question.data)
                questions_lst.append(qid)
            return Response({"questions": questions_lst}, status=status.HTTP_200_OK)
        else:
            return Response({"questions": "NOT_FOUND"}, status=status.HTTP_200_OK)


class FileUpload(APIView):
    def extract_first_frame(file_url, fname):
        # Check if the file exists
        if not os.path.isfile(file_url):
            print("File not found.")
            return

        # Extract the file's extension
        _, file_extension = os.path.splitext(file_url)

        # Open the video file
        cap = cv2.VideoCapture(file_url)

        # Check if the video can be opened
        if not cap.isOpened():
            print("Error: Couldn't open the video.")
            return

        # Read the first frame
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Couldn't read the first frame.")
            cap.release()
            return

        # Close the video file
        cap.release()

        # Create a filename for the extracted image with the same name as the video
        file_name = (
            os.path.splitext(os.path.basename(file_url))[0] + "_frame" + file_extension
        )

        # Save the first frame as an image
        cv2.imwrite(fname, frame)

        print(f"First frame extracted and saved as {file_name}")

    def post(self, request):
        # CHECK JWT TOKEN
        token = request.POST.get("jwt")
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        title = request.POST.get("title")
        public_or_private = request.POST.get("public_or_private")
        file_obj = request.FILES["file"]

        # b = VideoModel(title=file_obj.name.split(".")[0], username=user)
        b = VideoModel(title=title, username=user, public_or_private=public_or_private)
        b.save()
        VideoModel.objects.filter(id=b.id).update(video_path=f"videos/{b.id}.mp4")

        ###
        remove_video()
        path = default_storage.save(f"videos/{b.id}.mp4", ContentFile(file_obj.read()))
        ff = default_storage.open(path)
        file_url = default_storage.url(path)
        print(ff, file_url)
        ###
        FileUpload.extract_first_frame(f"videos/{b.id}.mp4", f"videos/{b.id}.png")

        return Response({"status": "success"}, status=204)


class YoutubeDownloader(APIView):
    def post(self, request):
        # CHECK JWT TOKEN
        token = json.loads(request.body.decode("utf-8"))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        youtube_url = json.loads(request.body.decode("utf-8"))["youtube_url"]
        public_or_private = json.loads(request.body.decode("utf-8"))[
            "public_or_private"
        ]

        b = VideoModel(
            title=YouTube(youtube_url).title,
            username=user,
            public_or_private=public_or_private,
        )
        b.save()
        VideoModel.objects.filter(id=b.id).update(video_path=f"videos/{b.id}.mp4")
        # youtube_video = YouTube(youtube_url).streams.filter(progressive=True, file_extension='mp4').first().download(f"videos", f"{b.id}.mp4")
        URLS = [youtube_url]
        ydl_opts = {"outtmpl": f"videos/{b.id}.mp4", "format": "mp4"}
        with YoutubeDL(ydl_opts) as ydl:
            youtube_video = ydl.download(URLS)
            print("videoooo", youtube_video)

        FileUpload.extract_first_frame(f"videos/{b.id}.mp4", f"videos/{b.id}.png")

        return Response({"status": "success"}, status=204)
