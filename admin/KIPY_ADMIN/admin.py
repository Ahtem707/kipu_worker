from django.contrib import admin
from django.contrib.auth.models import User, Group

from KIPY_ADMIN.models import Users, Projects, Vacancy


class UsersAdmin(admin.ModelAdmin):
    list_display = [
        'id','telegram_id', 'sername', 'tg_login', 'gender', 'phone', 'birthday', 'end_blocking', 'direction_blocking']

    list_display_links = [
        'id','telegram_id', 'sername', 'tg_login', 'gender', 'phone', 'birthday', 'end_blocking', 'direction_blocking']


class ProjectsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'description', 'type_projects', 'status', 'author', 'team', 'participants_count', 'link']
    list_display_links = [
        'id', 'title', 'description', 'type_projects', 'status', 'author', 'team', 'participants_count', 'link']


class VacancyAdmin(admin.ModelAdmin):
    list_display = [
       'id', 'title', 'description', 'type_vacancy', 'busyness', 'schedule', 'address', 'active']
    list_display_links = [
        'id', 'title', 'description', 'type_vacancy', 'busyness', 'schedule', 'address', 'active']


admin.site.register(Users, UsersAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)

