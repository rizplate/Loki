from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import SuccessStoryPerson, SuccessVideo, Snippet


class SuccessStoryPersonAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
admin.site.register(SuccessStoryPerson, SuccessStoryPersonAdmin)


class SuccessVideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(SuccessVideo, SuccessVideoAdmin)


class SnippetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Snippet, SnippetAdmin)