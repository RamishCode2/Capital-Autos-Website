from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .forms import CustomerRegistrationForm, EmailLoginForm, PasswordResetSetPasswordForm


def register(request):

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account was created. Please sign in.")
            return redirect("login")
    else:
        form = CustomerRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = EmailLoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if not form.cleaned_data["remember_me"]:
                request.session.set_expiry(0)
            messages.success(request, f"Welcome back, {form.get_user().first_name or form.get_user().username}!")
            return redirect(request.GET.get("next") or "home")
    else:
        form = EmailLoginForm(request)
    return render(request, "accounts/login.html", {"form": form})


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
