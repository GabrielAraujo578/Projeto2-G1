#Django por padrão só autentica usando o campo username, e não email


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # O `username` pode ser substituído por `email` no backend
        email = kwargs.get('email', username)
        
        try:
            # Buscar o usuário com base no e-mail
            user = User.objects.get(email=email)
            
            # Verificar se a senha está correta
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Caso o usuário não exista
            return None