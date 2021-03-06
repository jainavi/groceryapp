"""groceryapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app import views, admin_views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^contact/', views.contact, name='contact'),
	url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^password_forgot$', views.password_forgot, name='password_forgot'),
    url(r'^password_reset/([A-Za-z0-9]{128})$', views.password_reset, name='password_reset'),
    url(r'^reset_password$', views.reset_password, name='reset_password'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^order$', views.order, name='order'),
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^trackmyorder$', views.trackmyorder, name='trackmyorder'),
    url(r'^search/items/autocomplete', views.search_items, name='search_items'),
    url(r'^admin/test$', admin_views.test, name='test'),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
