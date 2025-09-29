from rest_framework import serializers
from .models import Ficha
import bleach


ALLOWED_TAGS = []
ALLOWED_ATTRS = {}

def sanitize_text(s):
    if s is None:
        return s
    return bleach.clean(str(s), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__'
        read_only_fields = ('id','criado_em','atualizado_em')

    def validate_personagem(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O campo 'personagem' é obrigatório.")
        return sanitize_text(value)

    def validate_nivel(self, value):
        if value < 1:
            raise serializers.ValidationError("Nível deve ser >= 1.")
        return int(value)

    def validate(self, data):
        # Campos obrigatórios: personagem, raca, classe, nivel (jogador opcional)
        if 'personagem' not in data or not data.get('personagem', '').strip():
            raise serializers.ValidationError({'personagem': 'Obrigatório.'})
        if 'raca' in data and isinstance(data.get('raca'), str):
            data['raca'] = sanitize_text(data['raca'])
        if 'classe' in data and isinstance(data.get('classe'), str):
            data['classe'] = sanitize_text(data['classe'])
        # atributos: garantir inteiros e intervalo razoável (1..30)
        attrs = ['forca','destreza','constituicao','inteligencia','sabedoria','carisma']
        for a in attrs:
            if a in data:
                try:
                    v = int(data[a])
                except Exception:
                    raise serializers.ValidationError({a: 'Deve ser número inteiro.'})
                if not (1 <= v <= 30):
                    raise serializers.ValidationError({a: 'Deve estar entre 1 e 30.'})
                data[a] = v
        # validate pericias -> se fornecida, deve ser dict
        pericias = data.get('pericias')
        if pericias is not None and not isinstance(pericias, dict):
            raise serializers.ValidationError({'pericias':'Deve ser um objeto (dict) com perícias.'})
        # sanitize anotacoes
        if 'anotacoes' in data:
            data['anotacoes'] = sanitize_text(data['anotacoes'])
        return data
