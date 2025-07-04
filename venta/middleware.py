from django.shortcuts import redirect

from django.urls import reverse
from django.contrib.auth import get_user

class AuthenticationMiddleware:
    """
    Verificar que el usuario este autenticado antes de
    acceder a cualquier url del sistema
    """
    def __init__(self, get_response):
        self.get_response = get_response
        #URLS que no requieren verificación de autentificación
        self.public_urls =[
            '/',
            '/admin/login',
            '/logout',
        ]

    def __call__(self, request):
        #verificar si el url actual esta en la lista publica
        if self.is_public_url(request.path):
            response = self.get_response(request)
            return response
        #Si el usuatio no esta autenticado, redirigirlo al login
        if not request.user.is_authenticated:
            return redirect('login')
        
        response = self.get_response(request)
        return response
    
    def is_public_url(self, path):
        """
        Si la url es pública, no requiere autenticación
        """
        if path in self.public_urls:
            return True
        
        return False