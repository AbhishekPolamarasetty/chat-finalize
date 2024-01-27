from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app1.models import *
from app1.serializer import PostModelSerializer
from rest_framework import generics, status
from rest_framework.response import Response


def getpostPage(request):
    return render(request,'Post/get-post.html')
def helpPage(request):
    return render(request,'Post/help.html')
# def postPage(request):
#     return render(request,'Post/post.html')
def submit_form(request):
    return redirect('base')
# def Post(request):
#     if request.method == 'POST':
#         # Retrieve data from POST request
#         passenger_name = request.POST.get('PassengerName')
#         date_of_journey = request.POST.get('DateOfJourney')
#         gender = request.POST.get('gender')
#         flight_number = request.POST.get('FlightNumber')
#         pnr_number = request.POST.get('PNRNumber')
#         source = request.POST.get('source')  # Ensure field name consistency
#         destination = request.POST.get('destination')  # Ensure field name consistency
#         baggage_space = request.POST.get('BaggageSpace')
#         checkbox = request.POST.get('checkbox') == 'on'  # Checkbox handling

#         # Create a new instance of PostModel
#         new_passenger = PostModel(
#             passenger_name=passenger_name,
#             date_of_journey=date_of_journey,
#             gender=gender,
#             flight_number=flight_number,
#             pnr_number=pnr_number,
#             source=source,
#             destination=destination,
#             baggage_space=baggage_space,
#             is_checked=checkbox,
#         )
        
#         # Save the new instance to the database
#         new_passenger.save()

#     return render(request, 'Post/post.html', {})

# post created by me 
from django.shortcuts import render
from .models import PostModel
import random

def generate_random_5_digit_number():
    return str(random.randint(10000, 99999))


# @allowed_users(allowed_roles=['user'])
def Post(request):
    if request.method == 'POST':

        user = request.user
        # Retrieve data from POST request
        passenger_name = request.POST.get('PassengerName')
        date_of_journey = request.POST.get('DateOfJourney')
        gender = request.POST.get('gender')
        flight_number = request.POST.get('FlightNumber')
        pnr_number = request.POST.get('PNRNumber')
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        baggage_space = request.POST.get('BaggageSpace')
        checkbox = request.POST.get('checkbox') == 'on'
        baggage_number = generate_random_5_digit_number()
        # Create a new instance of PostModel
        new_passenger = PostModel(
            passenger_name=passenger_name,
            date_of_journey=date_of_journey,
            gender=gender,
            flight_number=flight_number,
            pnr_number=pnr_number,
            source=source,
            destination=destination,
            baggage_space=baggage_space,
            is_checked=checkbox,
            user=request.user,
            baggage_number=baggage_number 
        )
        
        # Save the new instance to the database
        new_passenger.save()

    # Retrieve posts for the logged-in user
    # user_posts = PostModel.objects.filter(passenger_name=request.user.username)
    user_posts = PostModel.objects.filter(user=request.user)

    return render(request, 'Post/post.html', {'user_posts': user_posts})



class PostModelAPIView(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get(self, request):
        qs = PostModel.objects.all()
        date_of_journey = self.request.query_params.get('date_of_journey', None)
        source = self.request.query_params.get('source', None)
        destination = self.request.query_params.get('destination', None)
        gender = self.request.query_params.get('gender', None)
        flight_number = self.request.query_params.get('flight_number', None)
        if date_of_journey:
            qs =qs.filter(date_of_journey=date_of_journey)

        if source:
            qs =qs.filter(source=source)

        if destination:
            qs =qs.filter(destination=destination)

        if flight_number:
            qs =qs.filter(flight_number=flight_number)
            
        # queryset = PostModel.objects.filter(date_of_journey=date_of_journey)
        serializer = PostModelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class PostModelAPIView(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get(self, request):
        qs = PostModel.objects.all()
        serializer = PostModelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostModelAPIViewID(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get_object(self,id):
        try:
            data = PostModel.objects.get(id=id)
            return data
        except PostModel.DoesNotExist:
            return None
    
    def get(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        qs = self.get_object(id)
        if qs is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        qs.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)        
        



#Chat views
    
 
# @api_view(['GET', 'POST'])
# def user_chat_list(request, user_id, other_user_id=None):
#     if request.method == 'GET':
#         # Retrieve all chatted users related to the user with ID user_id
#         user_profiles = User.objects.exclude(id=user_id).exclude(is_staff=True)
#         serializer = UserSerializer(user_profiles, many=True)
#         return Response(serializer.data)
 
#     elif request.method == 'POST':
#         sender_profile = get_object_or_404(User, id=user_id)
#         receiver_profile = get_object_or_404(User, id=other_user_id)
#         serializer = ChatMessageSerializer(data=request.data)
 
#         if serializer.is_valid():
#             # Create a new chat message
#             chat_message = serializer.save(sender=sender_profile, receiver=receiver_profile, timestamp=timezone.now())
 
#             # Update user profiles with the new chat message
#             sender_profile.chat_messages.add(chat_message)
#             receiver_profile.chat_messages.add(chat_message)
 
#             return Response(serializer.data, status=201)
 
#         return Response(serializer.errors, status=400)
 
# @api_view(['GET', 'POST'])
# def chat_messages(request, user_id, other_user_id):
#     if request.method == 'GET':
#         # Retrieve chat messages between two users
#         chat_messages = ChatMessage.objects.filter(
#             Q(sender_id=user_id, receiver_id=other_user_id) | Q(sender_id=other_user_id, receiver_id=user_id)
#         ).order_by('timestamp')
#         serializer = ChatMessageSerializer(chat_messages, many=True)
#         return Response(serializer.data)
 
#     elif request.method == 'POST':
#         sender_profile = get_object_or_404(User, id=user_id)
#         receiver_profile = get_object_or_404(User, id=other_user_id)
#         serializer = ChatMessageSerializer(data=request.data)
 
#         if serializer.is_valid():
#             # Create a new chat message
#             chat_message = serializer.save(sender=sender_profile, receiver=receiver_profile)
 
#             # Update user profiles with the new chat message
#             sender_profile.chat_messages.add(chat_message)
#             receiver_profile.chat_messages.add(chat_message)
 
#             return Response(serializer.data, status=201)
 
#         return Response(serializer.errors, status=400)
    
    # edit profile views

from django.shortcuts import render, redirect
from app1.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
@login_required
def home(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
   room = request.POST.get('room_name', '')
   username = request.POST.get('username', '')

   if Room.objects.filter(name=room).exists():
    return redirect('/app1/'+room+'/?username='+username)
   else:
    new_room = Room.objects.create(name=room)
    new_room.save()
    return redirect('/app1/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

# @login_required
# def edit_profile(request):
#     user = request.user

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('edit_profile')
#     else:
#         form = UserProfileForm(instance=user)

#     return render(request, 'Login/edit_profile_backend.html', {'form': form})

def edit_profilePage(request):
    # You can add logic here to retrieve user data if needed
    return render(request, 'Login/edit_profile.html')


def profilePage(request):
    user_posts = request.user.postmodel_set.all()
    return render(request, 'Login/profile.html', {'user_posts': user_posts})
    # return render(request, 'Login/profile.html')

def change_passwordPage(request):
    return render(request, 'Login/change.html')

def verifyPage(request):
    return render(request, 'Login/verify.html')
def chat_view(request):
    return render(request, 'post/chat.html')