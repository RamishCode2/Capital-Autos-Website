from django.shortcuts import redirect, render
from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from brands.models import Brand
from products.models import Category, Product
from .models import HeroSlide
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import PrivacyPolicy, ReturnPolicy, FAQ, NewsletterSubscriber
from .forms import ContactForm
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ContactForm

def home(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()[:9]
    active_products = Product.objects.filter(is_active=True).select_related("brand", "category")
    homepage_products = active_products.order_by("homepage_order", "name")
    flash_products = homepage_products.filter(
        Q(is_flash_sale=True) | Q(discount_price__isnull=False)
    ).distinct()[:8]
    recommended_products = homepage_products.filter(
        Q(is_featured=True) | Q(is_best_seller=True) | Q(is_new=True)
    ).distinct()[:12]
    if not recommended_products:
        recommended_products = homepage_products[:12]

    context = {
        "brands": brands,
        "categories": categories,
        "flash_products": flash_products,
        "recommended_products": recommended_products,
        "hero_slides": HeroSlide.objects.filter(is_active=True),
    }

    return render(request, "core/home.html", context)
def about(request):
    return render(request, "about.html")

def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            enquiry = form.save()

            send_mail(

                subject=f"New Contact: {enquiry.subject}",

                message=f"""
New Contact Form Submission

Name: {enquiry.name}

Email: {enquiry.email}

Subject: {enquiry.subject}

Message:

{enquiry.message}
""",

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[settings.DEFAULT_FROM_EMAIL],

                fail_silently=True,

            )

            messages.success(
                request,
                "Thank you! Your message has been sent successfully."
            )

            return redirect("contact")

    else:

        form = ContactForm()

    return render(
        request,
        "contact.html",
        {
            "form": form
        }
    )
def privacy_policy(request):
    policy = PrivacyPolicy.objects.first()

    return render(
        request,
        "legal/privacy_policy.html",
        {
            "policy": policy
        }
    )


def returns(request):
    policy = ReturnPolicy.objects.first()

    return render(
        request,
        "legal/return.html",
        {
            "policy": policy
        }
    )


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)

    return render(
        request,
        "legal/faq.html",
        {
            "faqs": faqs
        }
    )


@require_POST
def newsletter_subscribe(request):
    try:
        email = forms.EmailField().clean(request.POST.get("email", "")).lower()
    except ValidationError:
        messages.error(request, "Enter a valid email address to subscribe.")
    else:
        subscriber, _ = NewsletterSubscriber.objects.get_or_create(email=email)
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=["is_active"])
        messages.success(request, "You are subscribed to Capital Autos updates.")

    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("home")
