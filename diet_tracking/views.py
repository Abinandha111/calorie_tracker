from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from diet_tracking.models import FoodLog
from diet_tracking.serializers import FoodLogSerializer



class FoodLogListCreateView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]

    authentication_classes = [authentication.TokenAuthentication]
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

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]

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


    # authentication_classes =[authentication.BasicAuthentication]

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user_foodlog = FoodLog.objects.filter(owner=request.user)

        response_data={
            "todays_calories":0,
            "monthly_calories":0
        }

        #todays====

        cur_date = datetime.today().date()

        todays_total=auth_user_foodlog.filter(
                                                created_at__date = cur_date
                                                ).values("calorie").aggregate(total=Sum("calorie")).get("total")

        

        #monthly =====
        cur_month = datetime.today().month
        cur_year = datetime.today().year

        monthly_total = auth_user_foodlog.filter(
            created_at__month=cur_month,
            created_at__year=cur_year
        ).values("calorie").aggregate(total=Sum("calorie")).get("total")

        #monthly summary

        monthly_summary = auth_user_foodlog.filter(
            created_at__month=cur_month,
            created_at__year=cur_year
            ).values("meal_type").annotate(total=Sum("calorie"))

        # todays summary

        todays_summary = auth_user_foodlog.filter(
            created_at__date = cur_date
        ).values("meal_type").annotate(total=Sum("calorie"))

        response_data["todays_summary"] = todays_summary

        response_data["monthly_summary"] = monthly_summary

        response_data["monthly_calories"] = monthly_total

        response_data["todays_calories"]= todays_total

        return Response(response_data)



from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework import status
from diet_tracking.services import scan_food_image

class FoodImageScanView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser] #for image 

    def post(self, request):

        food_image = request.FILES.get("food_image")

        if not food_image:
            return Response(
                {"error": "Please upload a food image"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            data = scan_food_image(food_image)

            

            serializer_instance = FoodLogSerializer(data=data)

            if serializer_instance.is_valid():

                serializer_instance.save(owner=request.user)

                return Response({
                                "message": "food image scanned successfully",
                                "data": serializer_instance.data
                            })

            else:

                return Response(serializer_instance.errors)
            
        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



