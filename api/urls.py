from django.urls import path, include
from home.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'person', PersonViewSet)
router.register(r'personSet', PersonViewSet, basename = 'person')

# from drf docs 
# *** This is not working, because we are overriding the variable which results in changing its functionality.
# urlpatterns = [
#     path('',include(router.urls))
# ]

# ***
# *** this variable is also redundant ***
# by sir -> wrong way
# urlpatterns = router.urls
# ***

# but sir method doesn't make much sense
urlpatterns = [
    path('',include(router.urls)), # doesn't make any sense, don't blindly follow tutorials,go with your intuition also.
    path('index/', index, name ='index'),
    path('person/', person, name = 'person'),
    path('login/',login,name = 'login'),
    # As classes usually have 's' as their end, so we can write like [persons] this for classes or [person-class-api] somethng.
    path('persons/',PersonAPI.as_view(), name = 'person-class'),
    path('register/', RegisterAPI.as_view(), name = 'register'),
    path('loginAPI/',LoginAPI.as_view(),name = 'login')
]
