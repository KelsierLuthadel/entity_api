from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from entity import views as entities
from network import views as networks

router = routers.DefaultRouter()
router.register(r'v1/ssids', entities.SSIDViewSet)
router.register(r'v1/resources', entities.ResourceViewSet)
router.register(r'v1/entities', entities.EntityViewSet)
router.register(r'v1/interfaces', entities.InterfaceViewSet)

router.register(r'v2/sites', networks.SiteView)
router.register(r'v2/networks', networks.NetworkView)
router.register(r'v2/switches', networks.SwitchView)
router.register(r'v2/wifis', networks.WiFiView)
router.register(r'v2/machines', networks.MachineView)
router.register(r'v2/interfaces', networks.InterfaceView)
router.register(r'v2/resources', networks.ResourceView)
router.register(r'v2/bluetooths', networks.BluetoothView)
router.register(r'v2/radios', networks.RadioView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # OpenAPI 3 documentation with Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
]
