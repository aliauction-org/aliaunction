# AuctionVistas: Online Auction System

## Overview
AuctionVistas is a full-featured online auction platform built with Django, designed for real-time, secure, and user-friendly bidding, payments, and management. It supports manual payment flows, in-app and email notifications, reviews, and a robust admin dashboard.

---

## Features Implemented

- **User Authentication & Profile**: Signup, login, password reset, profile page, bid/purchase history.
- **Auction Listing & Bidding**: Create auctions, upload images, real-time bidding (AJAX polling), Indian currency formatting.
- **Manual Payment Integration**: Platform and user payment profiles (bank, UPI, QR), payment proof uploads, admin/seller verification.
- **Notifications**: In-app (real-time, AJAX) and email notifications for outbid, auction won, auction ended, etc.
- **Newsletter Signup**: Users can subscribe to auction updates via the newsletter form in the footer. Emails are securely stored and manageable via the Django admin.
- **Ratings & Reviews**: Users can rate and review auctions after bidding.
- **Admin Dashboard**: Approve/block/end auctions, manage commissions, verify payments, view all data.
- **Contact Us Page**: Simple contact form, messages stored for admin review.
- **Minimalist Frontend**: Clean, modern, responsive UI with global CSS, no unnecessary effects.

---

## Tech Stack & Choices

- **Django**: Robust, secure, batteries-included backend framework.
- **HTML/CSS/JS**: Simple, maintainable frontend with custom CSS for a minimal look.
- **SQLite (default)**: Easy local development; can switch to MySQL/Postgres for production.
- **AJAX Polling**: Real-time updates for bidding and notifications with minimal setup.
- **Django Admin**: Powerful, customizable admin interface for rapid management.
- **Manual Payment Flow**: No API integration; supports Indian payment methods and proof uploads for flexibility and trust.

**Why these choices?**
- Django provides security, scalability, and rapid development.
- Manual payment flow is more flexible for Indian payment systems and easier to verify for both parties.
- AJAX polling is simple and reliable for real-time needs without extra infrastructure.
- Minimalist frontend ensures usability and fast load times.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Dimanjan/aliaunction.git
cd aliaunction
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# If requirements.txt is missing, install manually:
pip install django pillow
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

### 7. Access the App
- Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for the user site
- Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) for the admin dashboard

### 8. (Optional) Configure Media and Static Files
- Ensure `MEDIA_ROOT` and `STATIC_ROOT` are set in `settings.py` for production
- Collect static files: `python manage.py collectstatic`

---

## How Each Feature Can Be Improved in the Future

- **Real-Time Bidding**: Upgrade from AJAX polling to Django Channels (WebSockets) for instant updates and scalability.
- **Payments**: Integrate with payment APIs (Stripe, Razorpay, PayPal) for automated, secure transactions and instant verification.
- **Notifications**: Add web push notifications or mobile app support for true real-time, even when users are offline.
- **Admin Dashboard**: Build a custom dashboard UI for a more user-friendly, branded experience.
- **Proxy Bidding**: Implement automatic bidding up to a user’s max bid.
- **Refunds**: Automate refund processing and add user/admin workflows for disputes.
- **Security**: Add 2FA, rate limiting, and audit logs for enhanced security.
- **Testing & CI/CD**: Add automated tests and continuous integration for reliability.
- **Internationalization**: Add support for multiple languages and currencies.

---

## License
MIT (or specify your license)

---

## Contact
For support, use the Contact Us page in the app or open an issue on GitHub.

## Newsletter Setup & Management

AuctionVistas includes a built-in newsletter signup system:

- Users can subscribe to auction updates using the form in the footer of every page.
- Subscribed emails are stored in the database (`NewsletterSubscriber` model).
- Admins can view and manage subscribers in the Django admin panel.
- You can export emails for use in third-party services (Mailchimp, Brevo, etc.).

To enable or customize newsletter features (e.g., double opt-in, welcome emails, or unsubscribe), see the `newsletter` app code or contact the maintainer.

