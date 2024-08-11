from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/users/", include("apps.users.urls")),
    path("api/auth/", include("apps.authentication.urls")),
    path("api/customers/", include("apps.customers.urls")),
    path("api/loans/", include("apps.loans.urls")),
    path("api/payments/", include("apps.payments.urls")),
]
