"""biomio_backend_SCIM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from backendAPI import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^ServiceProviderConfig$', views.api_ServiceProviderConfig,
        name='scim-service-provider-config-detail'),

    url(r'^Schemas$', views.api_schemas_list,
        name='scim-schemas-detail'),
    url(r'^Schemas/(?P<pk>.+)$', views.api_schemas_detail,
        name='scim-schemas-detail'),

    url(r'^ResourceTypes$', views.api_resource_types_list,
        name='scim-resource-type-list'),
    url(r'^ResourceTypes/(?P<pk>.+)$', views.api_resource_types_detail,
        name='scim-resource-type-detail'),

    url(r'^providers/(?P<provider_id>[0-9]+)/Users$', views.ApiUsersList.as_view(),
        name='scim-users-list'),
    url(r'^providers/(?P<provider_id>[0-9]+)/Users/(?P<pk>[0-9]+)$', views.ApiUsersDetail.as_view(),
        name='scim-users-detail'),

    url(r'^providers/(?P<provider_id>[0-9]+)/BiomioResources$', views.ApiBiomioResourcesList.as_view(),
        name='scim-biomio-resources-list'),
    url(r'^providers/(?P<provider_id>[0-9]+)/BiomioResources/(?P<pk>[0-9]+)$', views.ApiBiomioResourcesDetail.as_view(),
        name='scim-biomio-resources-detail'),

    url(r'^providers/(?P<provider_id>[0-9]+)/BiomioPolicies$', views.ApiBiomioPoliciesList.as_view(),
        name='scim-biomio-policies-list'),
    url(r'^providers/(?P<provider_id>[0-9]+)/BiomioPolicies/(?P<pk>[0-9]+)$', views.ApiBiomioPoliciesDetail.as_view(),
        name='scim-biomio-policies-detail'),

    url(r'^providers/(?P<provider_id>[0-9]+)/Users/(?P<pk>[0-9]+)/BiomioDevices', views.ApiBiomioDevicesList.as_view(),
        name='scim-user-biomio-devices-list'),
    url(r'^providers/(?P<provider_id>[0-9]+)/BiomioDevices/(?P<pk>[0-9]+)$', views.ApiBiomioDevicesDetail.as_view(),
        name='scim-user-biomio-device-detail'),

    url(r'^BiomioDevices/(?P<device_id>[0-9]+)/BiomioEnrollment$', views.ApiBiomioEnrollmentDetail.as_view(),
        name='scim-biomio-enrollment'),

    url(r'^providers/(?P<provider_id>[0-9]+)/Groups$', views.ApiGroupsList.as_view(),
        name='scim-groups-list'),
    url(r'^providers/(?P<provider_id>[0-9]+)/Groups/(?P<pk>[0-9]+)$', views.ApiGroupDetail.as_view(),
        name='scim-groups-detail'),

    url(r'^generate_jwt/(?P<provider_id>[0-9]+)$', views.api_test_jwt,
        name='jwt'),

    # (?P<user_id>[0-9]+)
]
