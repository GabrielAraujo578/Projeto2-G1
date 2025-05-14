from django.contrib import admin
from .models import Professor, Turma, Candidato

admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(Candidato)

class TurmaAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return True