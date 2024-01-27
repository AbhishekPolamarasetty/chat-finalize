from django.contrib import admin
from app1.models import PostModel
from .models import Room, Message
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id','passenger_name', 'date_of_journey', 'gender', 'flight_number', 'pnr_number', 'source', 'destination', 'baggage_space', 'is_checked')
    
admin.site.register(PostModel,PostModelAdmin)

admin.site.register(Room)
admin.site.register(Message)

