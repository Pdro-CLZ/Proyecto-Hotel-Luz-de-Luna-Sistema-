from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'fecha_registro', 'activo')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'telefono')
    list_filter = ('activo',)

