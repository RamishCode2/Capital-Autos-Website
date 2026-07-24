from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .forms import PasswordResetSetPasswordForm


def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")


def user_login(request):

    if request.method == "POST":

        email = request.POST["email"].strip()
        password = request.POST["password"]

        user_record = User.objects.filter(email__iexact=email).first()
        user = authenticate(request, username=user_record.username, password=password) if user_record else None

        if user is not None:

            login(request, user)
            messages.success(request, f"Welcome {user.username}!")

            return redirect("home")

        else:

            messages.error(request, "Invalid email or password.")

    return render(request, "accounts/login.html")


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"

    def form_valid(self, form):
        # The same message is shown for existing and unknown email addresses.
        messages.success(
            self.request,
            "If an account exists with this email, a password reset link has been sent.",
        )
        return super().form_valid(form)


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    form_class = PasswordResetSetPasswordForm


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


def user_logout(request):

    logout(request)
    return redirect("home")


from django.contrib.auth.decorators import login_required
from orders.models import Order


@login_required
def profile(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "orders": orders,
    }

    return render(request, "accounts/profile.html", context)
