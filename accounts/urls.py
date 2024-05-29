from django.urls import path
from accounts import views

urlpatterns = [
    path(route='', view=views.Home, name='home_url'),
    path(route='main/', view=views.Main, name='main_url'),
    path(route='contact/', view=views.contactpage, name='contact_url'),
    path(route='about/', view=views.aboutpage, name='about_url'),
    path(route='signup/', view=views.signuppage, name='signup_url'),
    path(route='login/', view=views.loginpage, name='login_url'),
    path(route='profile/', view=views.profilepage, name='profile_url'),
    path(route='logout/', view=views.user_logout, name='logout_url'),
    # path(route='services/', view=Services_page, name='services_url'),
    # path(route='summerize/', view=views.text_summary, name='summerize_url'),
]

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)