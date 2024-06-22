from django.contrib import admin
from CSM.models import Author, Author_content
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "First_name","Last_name","phone_no", "pincode", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["First_name", "Last_name", "phone_no", "pincode"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "First_name", "Last_name", "phone_no", "pincode", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(Author, UserAdmin)

class items(admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ['id', 'user', 'title', 'image_tag']
    ordering = ['id']

    
    def get_queryset(self, request):
        qs = super(items, self).get_queryset(request)
        if request.user.is_admin:
            return qs
        return qs.filter(Author=request.user)
admin.site.register(Author_content, items)
