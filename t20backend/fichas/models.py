from django.db import models
# Se for usar SQLite/Django 3.1+, use models.JSONField diretamente:
# from django.db import models

class Ficha(models.Model):
    # Metadados
    schema_version = models.CharField(max_length=10, default='1.0')  # versão do JSON/schema

    # Identificação
    jogador = models.CharField(max_length=120, blank=True)
    personagem = models.CharField(max_length=120)
    raca = models.CharField(max_length=80, blank=True)
    origem = models.CharField(max_length=80, blank=True)
    classe = models.CharField(max_length=80, blank=True)
    nivel = models.PositiveIntegerField(default=1)
    divindade = models.CharField(max_length=120, blank=True)
    tendencia = models.CharField(max_length=40, blank=True)

    # Atributos (Campos explícitos para facilitar cálculos)
    forca = models.IntegerField(default=10)
    destreza = models.IntegerField(default=10)
    constituicao = models.IntegerField(default=10)
    inteligencia = models.IntegerField(default=10)
    sabedoria = models.IntegerField(default=10)
    carisma = models.IntegerField(default=10)

    # Vida / Mana
    pv_max = models.IntegerField(default=0)
    pv_atual = models.IntegerField(default=0)
    pm_max = models.IntegerField(default=0)
    pm_atual = models.IntegerField(default=0)

    # Defesa e armadura
    defesa_base = models.IntegerField(default=10)
    armadura = models.IntegerField(default=0)
    escudo = models.IntegerField(default=0)
    penalidade_armadura = models.IntegerField(default=0)
    outros_modificadores_defesa = models.IntegerField(default=0)

    # Perícias, habilidades, magias, inventário, anotações: armazenar como JSON
    pericias = models.JSONField(default=dict, blank=True)  # dict com cada perícia: { "Atletismo": {...} }
    poderes = models.JSONField(default=list, blank=True)   # lista de poderes/habilidades
    magias = models.JSONField(default=list, blank=True)    # lista de magias/slots
    inventario = models.JSONField(default=list, blank=True) # lista de items {nome, qtd, peso, obs}
    anotações = models.TextField(blank=True)

    tesouro = models.CharField(max_length=100, blank=True)
    carga = models.CharField(max_length=100, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.personagem} (Nível {self.nivel})"
