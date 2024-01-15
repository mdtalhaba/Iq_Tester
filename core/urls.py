from django.urls import path
from .views import home, RegistrationView, activate, UserLoginView, UserLogoutView, update_profile, quizes

urlpatterns = [
    path('', home, name='home'),
    path('category/<slug:category_slug>/', home, name='category_slug'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('register/active/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', update_profile, name='profile'),
    path('quiz/<int:quiz_id>/', quizes, name='quiz_page'),
]
