from django.shortcuts import render, redirect,get_object_or_404
from .models import *
import requests
from .forms import RoomForm
from users.views import login_required,teacher_required
from django.core.exceptions import PermissionDenied

@login_required
@teacher_required
def create_room(request):
    if not request.user.is_authenticated:
        return redirect('users:signin')

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)

            room.teacher = request.user
            room.save()
            room.members.add(request.user)

            return redirect('chat:room_list')

    else:
        form = RoomForm()

    return render(request, 'create_room.html', {'form': form})

@login_required
def room_list(request):
    if not request.user.is_authenticated:
        return redirect('users:signin')

    rooms = Room.objects.all()

    city = request.GET.get("city", "Karaganda")
    api_key = "ce3c74c3c3c8bf8c6bd60759ee311985"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

    weather = None

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "desc": data["weather"][0]["description"]
            }

    except:
        weather = None

    return render(request, 'room_list.html', {
        'rooms': rooms,
        'weather': weather,
        'city': city
    })

@login_required
def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    messages = Message.objects.filter(room=room).order_by("created_at")

    return render(request, "room.html", {
        "room": room,
        "messages": messages
    })

@login_required
def delete_room(request, room_id):
    if not request.user.is_authenticated:
        return redirect('users:signin')
        
    room = get_object_or_404(Room, id=room_id)
    
    if room.teacher != request.user:
        raise PermissionDenied("Вы не можете удалить эту комнату.")
        
    if request.method == 'POST':
        room.delete()
        return redirect('chat:room_list')
        
    return redirect('chat:room_list')