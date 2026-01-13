import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SellerVerification
from .forms import SellerVerificationForm, OTPForm

@login_required
def start_verification(request):
    verification, created = SellerVerification.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = SellerVerificationForm(request.POST, instance=verification)
        if form.is_valid():
            verification = form.save(commit=False)
            otp = str(random.randint(100000, 999999))
            request.session["otp"] = otp  # mock OTP
            request.session["otp_user"] = request.user.id
            verification.save()
            print("DEBUG OTP:", otp)  # replace with SMS later
            return redirect("verify_otp")
    else:
        form = SellerVerificationForm(instance=verification)

    return render(request, "seller_verification/start.html", {"form": form})


@login_required
def verify_otp(request):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["otp"] == request.session.get("otp"):
                verification = request.user.seller_verification
                verification.phone_verified = True
                verification.save()
                return redirect("verification_status")
    else:
        form = OTPForm()

    return render(request, "seller_verification/otp.html", {"form": form})


@login_required
def verification_status(request):
    verification = getattr(request.user, "seller_verification", None)
    return render(
        request,
        "seller_verification/status.html",
        {"verification": verification}
    )
