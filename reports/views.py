from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from auctions.models import Auction
from users.models import User
from .forms import ReportForm
from .models import Report

@login_required
def report_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.report_type = Report.REPORT_AUCTION
            report.auction = auction
            report.save()
            return redirect("auction_detail", auction_id=auction.id)
    else:
        form = ReportForm()

    return render(request, "reports/report_form.html", {
        "form": form,
        "target": auction.title
    })


@login_required
def report_user(request, user_id):
    reported_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.report_type = Report.REPORT_USER
            report.reported_user = reported_user
            report.save()
            return redirect("profile", user_id=reported_user.id)
    else:
        form = ReportForm()

    return render(request, "reports/report_form.html", {
        "form": form,
        "target": reported_user.username
    })
