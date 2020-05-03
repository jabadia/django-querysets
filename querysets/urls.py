from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('queries/', include('queries.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('queries-index'), permanent=True)),
]
