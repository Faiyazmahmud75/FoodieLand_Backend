from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView, VerifyEmailView, RequestPasswordResetView, ResetPasswordView

urlpatterns = [
	path("register/", RegisterView.as_view(), name="register"),
	path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
	path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
	path("me/", MeView.as_view(), name="me"),
	path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
	path("request-password-reset/", RequestPasswordResetView.as_view(), name="request_password_reset"),
	path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
] 