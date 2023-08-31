from django.shortcuts import render
from rest_framework.views import APIView
from .models import Student
from .serializer import Studentserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class StudentDetails(APIView):
    queryset = Student.objects.all()   # for djangomodelpermission and djangomodelpermissionoranonreadonly, because it need to know which model should the check permisssion ,which is through the queryset or get_queryset() 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,format=None):
        stu = Student.objects.all()
        serializer = Studentserializer(stu,many = True)
        return Response(serializer.data)


    def post (self,request,format = None):
        serializer = Studentserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({'msg':'Data Created ...'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class StudentUpdates(APIView):
    queryset = Student.objects.all()   # for djangomodelpermission and djangomodelpermissionoranonreadonly, because it need to know which model should the check permisssion ,which is through the queryset or get_queryset() 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
   
    
    def get(self,request,pk=None,format=None):
        id = pk 
        if id is not None:
            stu =Student.objects.get(pk=id)
            serializer = Studentserializer(stu)
            return Response(serializer.data)
    
    def put(self,request,pk=None,format=None):
        id = pk
        if id is not None:
            stu = Student.objects.get(pk=id)
            serializer = Studentserializer(stu,data=request.data)
            if serializer.is_valid():
                serializer.save()
                res = {"msg":"Data Updated Completely"}
                data = JSONRenderer().render(res)
                return HttpResponse(data,content_type='application/json')
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self,request,pk=None,format = None):
        id = pk
        if id is not None:
            stu = Student.objects.get(pk=id)
            serializer = Studentserializer(stu,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Data Updated Partially...'})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self,request,pk=None,format=None):
        
        id= pk 
        if id is not None:
            stu = Student.objects.get(pk=id)
            stu.delete()
            return Response({'msg':'Data deleted succesfully....'})
        return Response({'msg':'Select A student...'})