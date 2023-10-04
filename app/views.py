from django.shortcuts import render, HttpResponse
from .models import Student
from .serializers import UserSerializer,StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.contrib.auth import authenticate, login
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


# from .models import User
# from .serializers import UserSerializer

# Create your views here.


    
   

 
class RegisterUser(APIView):

    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            # token_obj,created=Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)  # Create a refresh token
            access_token = refresh.access_token 
            return Response({'status':400,'token': str(access_token)})
        else:
            
            return Response({'status':200,'message':'error data'})
        
class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
        
            login(request, user)
            #token_obj, created = Token.objects.get_or_create(user=user) --- for simple token auth
            refresh = RefreshToken.for_user(user)  # Create a refresh token for jwt auth
            access_token = refresh.access_token 
            return Response({'status': 200,'token':str(access_token)})
        else:
            return Response({'status': 400, 'message': 'Invalid credentials','token': str(token)})




from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated     
            
        

class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.IsAdminUser]------>when you want to show data to admin or for simple user, using super,active class
    
    
    def post(self,request):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':200,'message':'data saved'})
        else:
            return Response({'status':403})
      
    def get(self,request):
        studnet_obj=Student.objects.all()
        serializer = StudentSerializer(studnet_obj,many = True)
       
        return Response({'data':serializer.data})
            
    
    def put(self,request,id): #complete data update
        try:
            student_obj=Student.objects.get(id=id)           
            serializer=StudentSerializer(student_obj,data=request.data,partial=True)
            if serializer.is_valid():
        
                serializer.save()
                return Response({'status':200,'data':serializer.data})
            else:
                return Response({'status':400,'data':'invalid data'})
                
        except Exception as e:
           return Response({'message':'error, thorw a exception'+ str(e)})
       
       
    def patch(self,request,id):
        student_obj=Student.objects.get(id=id)
        serializer=StudentSerializer(instance=student_obj,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status':400,'data':serializer.data})
        else:
            return Response({'status':200,'data':'invalid data'})
        
    def delete(self,request,id):
        student_obj=Student.objects.get(id=id)
        student_obj.delete()
   
        return Response({'status': 400, 'message': f' id {id} deleted'})

            
        
        
        
        
        
            