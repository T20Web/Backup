from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ficha
from .serializers import FichaSerializer

class FichaViewSet(viewsets.ModelViewSet):
    queryset = Ficha.objects.all().order_by('-atualizado_em')
    serializer_class = FichaSerializer

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """Retorna JSON completo da ficha (para exportar)."""
        ficha = self.get_object()
        serializer = self.get_serializer(ficha)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='import')
    def import_ficha(self, request):
        """
        Importa ou atualiza uma ficha via JSON.
        Se o body tiver 'id' e existir -> atualiza; caso contrário cria.
        Valida esquema via serializer.
        """
        data = request.data
        ficha_id = data.get('id')
        if ficha_id:
            try:
                ficha = Ficha.objects.get(id=ficha_id)
                serializer = self.get_serializer(ficha, data=data, partial=True)
            except Ficha.DoesNotExist:
                serializer = self.get_serializer(data=data)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='default')
    def default_ficha(self, request):
        """
        Retorna uma 'Ficha Padrão' (schema + preenchimento básico).
        Útil para o frontend popular ao criar nova ficha.
        """
        default = {
            "schema_version": "1.0",
            "jogador": "",
            "personagem": "Nome do Personagem",
            "raca": "",
            "origem": "",
            "classe": "",
            "nivel": 1,
            "tendencia": "",
            "divindade": "",
            "forca": 10, "destreza": 10, "constituicao": 10, "inteligencia": 10, "sabedoria": 10, "carisma": 10,
            "pv_max": 0, "pv_atual": 0, "pm_max": 0, "pm_atual": 0,
            "defesa_base": 10, "armadura": 0, "escudo": 0, "penalidade_armadura": 0, "outros_modificadores_defesa": 0,
            "pericias": {},
            "poderes": [],
            "magias": [],
            "inventario": [],
            "anotacoes": "",
            "tesouro": "",
            "carga": ""
        }
        return Response(default)
    