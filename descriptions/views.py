from django.shortcuts import render
from .models import Description as DescriptionsModel
from .serializer import DescriptionsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import json
from user.jwt_users import JWT_Users
from moviepy.video.io.VideoFileClip import VideoFileClip


# Create your views here.
class Descriptions(APIView):
    def get_video_length(self, video_path):
        try:
            clip = VideoFileClip(video_path)
            length = clip.duration
            clip.close()
            return length
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get(self, request):
        token = request.GET.get("jwt", "")
        video_id = request.GET.get("video_id", "")
        # CHECK JWT TOKEN
        # token = json.loads(request.body.decode('utf-8'))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(token)
        if not user:
            user = ""
            # return Response({"descriptions": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        # video_id = json.loads(request.body.decode('utf-8'))["video_id"]
        descriptions = DescriptionsModel.objects.filter(video_id=video_id)
        if len(descriptions) == 0:
            return Response(
                {"descriptions": "VIDEO_NOT_FOUND"}, status=status.HTTP_200_OK
            )
        descriptions_lst = []
        for d in range(len(descriptions)):
            serialized_desc = DescriptionsSerializer(descriptions[d])
            vid = JSONRenderer().render(serialized_desc.data)
            descriptions_lst.append(vid)
        return Response({"descriptions": descriptions_lst}, status=status.HTTP_200_OK)

    def post(self, request):
        # CHECK JWT TOKEN
        token = json.loads(request.body.decode("utf-8"))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(request.data.get("jwt"))
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        video_id = json.loads(request.body.decode("utf-8"))["video_id"]
        time_stamp_start = json.loads(request.body.decode("utf-8"))["time_stamp_start"]
        time_stamp_end = json.loads(request.body.decode("utf-8"))["time_stamp_end"]
        descriptions = json.loads(request.body.decode("utf-8"))["descriptions"]
        ai_or_human = json.loads(request.body.decode("utf-8"))["ai_or_human"]
        group_id = str(user) + "#*#" + str(video_id)

        if time_stamp_start < 0 or time_stamp_end > self.get_video_length(
            f"videos/{video_id}.mp4"
        ):
            return Response(
                {"status": "TIME_STAMP_OUT_OF_LENGTH"}, status=status.HTTP_200_OK
            )

        descriptions = DescriptionsModel.objects.filter(video_id=video_id)
        if len(descriptions) > 0:
            for desc in descriptions:
                if (
                    time_stamp_start < desc.time_stamp_end
                    or desc.time_stamp_start < time_stamp_end
                ):
                    return Response(
                        {"status": "TIME_STAMP_OVERLAP"}, status=status.HTTP_200_OK
                    )

        b = DescriptionsModel(
            video_id=video_id,
            time_stamp_start=time_stamp_start,
            time_stamp_end=time_stamp_end,
            descriptions=descriptions,
            username=user,
            ai_or_human=ai_or_human,
            group_id=group_id,
        )
        b.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)

    def put(self, request):
        # CHECK JWT TOKEN
        token = json.loads(request.body.decode("utf-8"))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(request.data.get("jwt"))
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        id = json.loads(request.body.decode("utf-8"))["id"]
        modified_descriptions = json.loads(request.body.decode("utf-8"))[
            "modified_descriptions"
        ]
        # time_stamp = json.loads(request.body.decode('utf-8'))["time_stamp"]

        if modified_descriptions != "":
            if DescriptionsModel.objects.get(id=id).modified_descriptions:
                new_desc = (
                    DescriptionsModel.objects.get(id=id).modified_descriptions
                    + "###"
                    + DescriptionsModel.objects.get(id=id).descriptions
                    + ":::who previous descs changed:::"
                    + user
                )
            else:
                new_desc = (
                    "None"
                    + "###"
                    + DescriptionsModel.objects.get(id=id).descriptions
                    + ":::who previous descs changed:::"
                    + user
                )
            DescriptionsModel.objects.filter(id=id).update(
                modified_descriptions=new_desc
            )
            DescriptionsModel.objects.filter(id=id).update(
                descriptions=modified_descriptions
            )

        # if time_stamp != "":
        #     DescriptionsModel.objects.filter(id=id).update(time_stamp=time_stamp)

        return Response({"status": "success"}, status=status.HTTP_200_OK)

    def delete(self, request):
        # CHECK JWT TOKEN
        token = json.loads(request.body.decode("utf-8"))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(request.data.get("jwt"))
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        id = json.loads(request.body.decode("utf-8"))["id"]

        DescriptionsModel.objects.filter(id=id).delete()

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class Star(APIView):
    def post(self, request):
        # CHECK JWT TOKEN
        token = json.loads(request.body.decode("utf-8"))["jwt"]
        jwt_users1 = JWT_Users()
        jwt_users1.initialize()
        user = jwt_users1.find_user(request.data.get("jwt"))
        if not user:
            return Response({"status": "USER_NOT_LOGGED_IN"}, status=status.HTTP_200_OK)
        # CHECK JWT TOKEN

        id = json.loads(request.body.decode("utf-8"))["id"]

        group_id = DescriptionsModel.objects.filter(id=id).group_id
        star = DescriptionsModel.objects.filter(id=id).star
        for d in DescriptionsModel.objects.filter(group_id=group_id):
            d.update(star=star + 1)

        return Response({"status": "success"}, status=status.HTTP_200_OK)
