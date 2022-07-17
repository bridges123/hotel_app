from django.contrib import admin

from main.models import Customer, Comfortable, Room, Review


class CustomerAdmin(admin.ModelAdmin):
    pass


class ComfortableAdmin(admin.ModelAdmin):
    pass


class RoomAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Comfortable, ComfortableAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Review, ReviewAdmin)
