"""lawyer_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from lawyer import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),

    path('login/',views.user_login,name='login'),
    path('client_signup/',views.client_signup,name='client_signup'),
    path('logout/',views.user_logout,name='logout'),

    path('view_lawyers/',views.view_lawyer,name='view_lawyers'),
    path('lawyer_register/',views.lawyer,name='lawyer_register'),
    path('filter_by_practice/',views.subarea_dependent_dropdown,name='area_dropdown'),
    path('add_practice_area/',views.add_practice_area,name='add_practice_area'),
    path('lawyer_edit_profile/',views.lawyer_edit_profile,name='lawyer_edit_profile'),
    path('state_list/',views.state_list,name='state_list'),
    path('practice_area_for_state/',views.practice_area_for_state,name='practice_area_for_state'),
    path('view_lawyer_by_state/',views.view_lawyer_by_state,name='view_lawyer_by_state'),
    path('lawyer_profile/<lid>',views.lawyer_profile,name='lawyer_profile'),
    path('review_lawyer/<lid>',views.review_lawyer,name='review_lawyer'),
    path('viewall_review_lawyer/<lid>',views.viewall_review_lawyer,name='viewall_review_lawyer'),
    path('fitler_by_subarea_rating_experience/',views.fitler_by_subarea_rating_experience,name='fitler_by_subarea_rating_experience'),
    path('send_messages/',views.send_messages,name="send_messages"),
    path('change_password/',views.change_password,name="change_password"),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
