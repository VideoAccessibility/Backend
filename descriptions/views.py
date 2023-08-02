from django.shortcuts import render
from .models import Description as DescriptionsModel
from .serializer import DescriptionsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import json

# Create your views here.
class Descriptions(APIView):

    def get(self, request):
        print(request.body)
        video_id = json.loads(request.body.decode('utf-8'))["video_id"]
        descriptions = DescriptionsModel.objects.filter(video_id=video_id)
        if len(descriptions) == 0:
            return Response({"descriptions": "VIDEO_NOT_FOUND"}, status=status.HTTP_200_OK)
        descriptions_lst = []
        for d in range(len(descriptions)):
            serialized_desc = DescriptionsSerializer(descriptions[d])
            vid = JSONRenderer().render(serialized_desc.data)
            descriptions_lst.append(vid)
        return Response({"descriptions": descriptions_lst}, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.body)
        video_id = json.loads(request.body.decode('utf-8'))["video_id"]
        time_stamp = json.loads(request.body.decode('utf-8'))["time_stamp"]
        descriptions = json.loads(request.body.decode('utf-8'))["descriptions"]
        
        b = DescriptionsModel(video_id=video_id, time_stamp=time_stamp, descriptions=descriptions)
        b.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)
    
    def put(self, request):
        print(request.body)
        id = json.loads(request.body.decode('utf-8'))["id"]
        modified_descriptions = json.loads(request.body.decode('utf-8'))["modified_descriptions"]
        DescriptionsModel.objects.filter(id=id).update(modified_descriptions=modified_descriptions)

        return Response({"status": "success"}, status=status.HTTP_200_OK)
