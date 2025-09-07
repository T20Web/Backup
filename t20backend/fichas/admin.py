from django.contrib import admin
from .models import Ficha

@admin.register(Ficha)
class FichaAdmin(admin.ModelAdmin):
    list_display = ('personagem','jogador','classe','nivel','raca','criado_em')
    search_fields = ('personagem','jogador','classe','raca')
    readonly_fields = ('criado_em','atualizado_em')