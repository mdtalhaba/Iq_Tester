from django.urls import path
from .views import home, quizes, RegistrationView, activate, UserLoginView, UserLogoutView, update_profile, quiz_page

urlpatterns = [
    path('', home, name='home'),
    path('quizes/', quizes, name='quizes'),
    path('category/<slug:category_slug>/', quizes, name='category_slug_quizes'),
    path('category/<slug:category_slug>/', home, name='category_slug_home'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('register/active/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', update_profile, name='profile'),
    path('quiz/<int:quiz_id>/', quiz_page, name='quiz_page'),
]
