from rest_framework import serializers

# Serializer for Firebase email verification
class FirebaseVerifyEmailSerializer(serializers.Serializer):
    oobCode = serializers.CharField(required=False)  # Firebase's verification code
    mode = serializers.CharField(required=False)     # Should be 'verifyEmail'

from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import User
from .serializers import UserSerializer, RegisterSerializer, RequestPasswordResetSerializer, ResetPasswordSerializer, VerifyEmailSerializer
from rest_framework.views import APIView
from config.firebase_init import auth as firebase_auth
from django.core.mail import send_mail
from django.conf import settings


def send_firebase_verification_email(email, password):
    try:
        # First check if email settings are configured
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise serializers.ValidationError(
                "Email settings are not configured. Please contact the administrator."
            )

        # First, try to get the user if they already exist
        try:
            firebase_user = firebase_auth.get_user_by_email(email)
            raise serializers.ValidationError("Email already exists in Firebase")
        except firebase_auth.UserNotFoundError:
            pass  # This is good, user doesn't exist yet
        
        # Create user with email verification enabled
        firebase_user = firebase_auth.create_user(
            email=email,
            password=password,
            email_verified=False,  # Explicitly set as not verified
            disabled=False  # Make sure the account is enabled
        )
        
        try:
            # Custom email template for verification
            link_custom = firebase_auth.generate_email_verification_link(
                email
            )
            # Send the verification link using Django's email system
            send_mail(
                subject="Verify your FoodieLand account",
                message=f"Please click this link to verify your email: {link_custom}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=f"""
                    <h2>Welcome to FoodieLand!</h2>
                    <p>Please verify your email by clicking the link below:</p>
                    <a href="{link_custom}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Verify Email</a>
                    <p style="margin-top: 20px;">If you didn't create this account, you can ignore this email.</p>
                """
            )
            
            return firebase_user
            
        except Exception as email_error:
            # Log the full error for debugging
            import traceback
            print(f"Email verification error: {str(email_error)}")
            print(f"Traceback: {traceback.format_exc()}")
            
            # If email sending fails, delete the created Firebase user
            try:
                firebase_auth.delete_user(firebase_user.uid)
            except Exception as delete_error:
                print(f"Error deleting Firebase user: {str(delete_error)}")
                
            raise serializers.ValidationError(
                "Failed to send verification email. Please try again or contact support."
            )
    except Exception as e:
        if hasattr(e, 'detail'):
            raise e  # Re-raise validation errors
        raise serializers.ValidationError(f"Registration failed: {str(e)}")

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            # First create Firebase user
            firebase_user = send_firebase_verification_email(
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            # Then create Django user
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"detail": "Registration successful. Please check your email to verify your account."},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except serializers.ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "Registration failed. Please try again."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save()

# Custom TokenObtainPairView to block login for unverified users
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({
                "non_field_errors": ["Both email and password are required."]
            })

        try:
            # First check if user exists in our database
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "email": ["No account found with this email. Please register first."]
                })

            # Now verify the credentials
            data = super().validate(attrs)
            self.user = user  # Make sure user is set

            # Check Firebase verification status
            try:
                firebase_user = firebase_auth.get_user_by_email(email)
                
                # Check if Firebase has verified the email
                if not firebase_user.email_verified:
                    raise serializers.ValidationError({
                        "email": ["Please verify your email before logging in. Check your inbox for the verification link."]
                    })
                
                # If Firebase says verified but our DB doesn't, update our DB
                if not user.is_email_verified:
                    user.is_email_verified = True
                    user.save(update_fields=['is_email_verified'])

            except firebase_auth.UserNotFoundError:
                # Recreate the user in Firebase if they exist in our DB but not in Firebase
                try:
                    firebase_user = firebase_auth.create_user(
                        email=email,
                        password=password,
                        email_verified=False
                    )
                    raise serializers.ValidationError({
                        "email": ["Please verify your email. A new verification link has been sent."]
                    })
                except Exception as firebase_error:
                    print(f"Firebase error: {str(firebase_error)}")
                    raise serializers.ValidationError({
                        "non_field_errors": ["Unable to verify email status. Please try again later."]
                    })

            return data

        except serializers.ValidationError as e:
            # Re-raise validation errors with proper formatting
            if hasattr(e, 'detail'):
                if isinstance(e.detail, dict):
                    raise
                # Convert string errors to our format
                raise serializers.ValidationError({
                    "non_field_errors": [str(e.detail)]
                })
            raise serializers.ValidationError({
                "non_field_errors": ["Invalid credentials. Please try again."]
            })

class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer

class MeView(generics.RetrieveUpdateAPIView):
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		user = self.request.user
		if not user.is_email_verified:
			raise permissions.PermissionDenied("Please verify your email before accessing your profile.")
		return user


# Firebase email verification endpoint

class FirebaseVerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FirebaseVerifyEmailSerializer

    def post(self, request):
        try:
            # Get the verification code from query parameters or request body
            oob_code = request.query_params.get('oobCode')
            if not oob_code:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                oob_code = serializer.validated_data.get('token')
            
            if not oob_code:
                return Response(
                    {"error": "No verification code provided. Please use the link from your email."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify the code with Firebase
            try:
                # First check if the code is valid and is for email verification
                check_code = firebase_auth.check_action_code(oob_code)
                if check_code.operation != 'VERIFY_EMAIL':
                    return Response(
                        {"error": "Invalid verification code type"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Apply the email verification
                firebase_auth.confirm_email_verification(oob_code)
                
                # Get the email from the action code check
                email = check_code.data.get('email')
                
                # Update the Django user
                try:
                    user = User.objects.get(email=email)
                    
                    # Double check with Firebase that the email is verified
                    firebase_user = firebase_auth.get_user_by_email(email)
                    if not firebase_user.email_verified:
                        return Response(
                            {"error": "Email verification failed in Firebase"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Update Django user verification status
                    user.is_email_verified = True
                    user.email_verification_token = None  # Clear the token
                    user.save(update_fields=['is_email_verified', 'email_verification_token'])
                    
                    return Response({
                        "message": "Email successfully verified",
                        "email": email
                    })
                except User.DoesNotExist:
                    return Response(
                        {"error": f"No user found with email: {email}"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            except firebase_auth.InvalidActionCodeError:
                return Response(
                    {"error": "Invalid or expired verification code"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Check the action code
            check_action_code = firebase_auth.check_action_code(oob_code)
            if check_action_code.operation != 'VERIFY_EMAIL':
                return Response(
                    {"error": "Invalid verification code"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Apply the verification code
            firebase_auth.confirm_email_verification(oob_code)
            
            # Update Django user verification status
            email = check_action_code.data.get('email')
            try:
                user = User.objects.get(email=email)
                user.is_email_verified = True
                user.save()
                
                return Response({
                    "message": "Email successfully verified",
                    "email": email
                })
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except firebase_auth.InvalidActionCodeError:
            return Response(
                {"error": "Invalid or expired verification code"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except firebase_auth.UserNotFoundError:
            return Response(
                {"error": "User not found in Firebase"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            # Verify the Firebase token
            decoded_token = firebase_auth.verify_id_token(serializer.validated_data['token'])
            email = decoded_token['email']
            
            # Get user from Firebase
            firebase_user = firebase_auth.get_user_by_email(email)
            
            if firebase_user.email_verified:
                # Update Django user verification status
                user = User.objects.get(email=email)
                user.is_email_verified = True
                user.save()
                
                return Response({
                    "message": "Email successfully verified"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Email not verified"
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(generics.GenericAPIView):
	serializer_class = RequestPasswordResetSerializer
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response({"detail": "reset email sent"})

class ResetPasswordView(generics.GenericAPIView):
	serializer_class = ResetPasswordSerializer
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response({"detail": "password reset successful"}) 