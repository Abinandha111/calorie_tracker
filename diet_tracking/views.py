from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from diet_tracking.models import FoodLog
from diet_tracking.serializers import FoodLogSerializer



class FoodLogListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        qs = FoodLog.objects.filter(owner=auth_user)

        serializer_instance = FoodLogSerializer(qs,many=True)

        return Response(serializer_instance.data)

    def post(self,request):

        form_data = request.data

        auth_user = request.user

        serializer_instance = FoodLogSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=auth_user)

            return Response(serializer_instance.data)

        else:

            return Response(serializer_instance.errors)


from diet_tracking.permissions import IsOwner

class FoodLogRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        qs =    get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,qs)

        serializer_instance = FoodLogSerializer(qs)

        return Response(serializer_instance.data)


    def put(self,request,pk=None):

        instance = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = FoodLogSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(serializer_instance.data)

        else:

            return Response(serializer_instance.errors)

    def delete(self,request,pk=None):

        qs = get_object_or_404(FoodLog,id=pk)

        self.check_object_permissions(request,qs)

        qs.delete()

        return Response({"message":"deleted........"})



        
from datetime import datetime
from django.db.models import Sum

class FoodLogSummaryView(APIView):


    authentication_classes =[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user_foodlog = FoodLog.objects.filter(owner=request.user)

        response_data={
            "todays_calories":0,
            "monthly_calories":0
        }

        cur_date = datetime.today().date()

        todays_total=auth_user_foodlog.filter(
                                                created_at__date = cur_date
                                                ).values("calorie").aggregate(total=Sum("calorie")).get("total")

        #todays_total=3200

        response_data["todays_calories"]= todays_total

        return Response(response_data)

