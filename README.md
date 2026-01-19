# AuctionVistas: Online Auction System

## Overview
AuctionVistas is a full-featured online auction platform built with Django, designed for real-time, secure, and user-friendly bidding, payments, and management. It supports manual payment flows, in-app and email notifications, reviews, and a robust admin dashboard. The platform features a modern, responsive design with comprehensive marketplace functionality and advanced features like **anti-sniping**, **real-time WebSocket updates**, **bulk uploads**, and **rate limiting**.

---
## 🗂 COMPLETE PROJECT STRUCTURE

```text
aliaunction/
│
├── manage.py
├── db.sqlite3
├── README.md
├── requirements.txt
│
├── aliaunction/                 # Main project configuration
├── auctions/                    # Core auction system & Bulk Upload
├── auction_discovery/           # Discover & explore auctions
├── auction_status/              # Real-time status utils
├── auction_close/               # Anti-sniping & auction closing
├── auction_workflow/            # Auction state management
├── auction_ws/                  # WebSocket real-time updates
├── bid_protection/              # Bid validation & Rate limiting
├── commission/                  # Commission calculations
├── contact/                     # Contact forms
├── dashboard/                   # User dashboards
├── deposits/                    # Deposit management
├── disputes/                    # Dispute management
├── escrow/                      # Escrow & transaction tracking
├── marketplace/                 # Marketplace pages
├── news/                        # News articles
├── newsletter/                  # Newsletter subscriptions
├── notifications/               # In-app notifications
├── payments/                    # Payments & invoices
├── reports/                     # User & auction reporting
├── reserve_price/               # Reserve price logic
├── reviews/                     # Buyer & seller ratings
├── seller_verification/         # Seller verification
├── shipping/                    # Shipping & delivery
├── users/                       # User accounts & profiles
├── watchlist/                   # Watchlist functionality
├── static/                      # Static files (CSS, JS, images)
└── templates/                   # Global templates
```

## 🚀 Key Features

### 🔨 Core Auction & Bidding
- **Auction Status**: *Upcoming / Live / Ended* with real-time countdowns.
- **Anti-Sniping**: Auctions automatically extend by X minutes if a bid is placed in the last Y minutes (configurable per auction).
- **Real-Time Updates**: WebSocket-powered live bid updates without page refresh.
- **3-Column Auction Layout**: Image/Description | Bidding | Bid History for optimal UX.
- **Bid Protection**:
  - Negative bid validation
  - Seller cannot bid on own auction
  - Bids blocked before start & after end
  - **Rate Limiting**: Limits bids (10/min) and logins (5/min) to prevent abuse.
- **Reserve Price**: Hidden reserve prices with status indicators ("Met" / "Not Met").
- **Bulk Upload**: Admin/Sellers can upload multiple auctions via CSV.

### 🏪 Marketplace Enhanced
- **Categories**: Browse auctions by categories (Electronics, Art, Vehicles, etc.)
- **Advanced Search**: Filter by price range, live status, and category.
- **Price Filtering**: Min/Max price filters on search.
- **Featured Auctions**: Highlighted auctions on the homepage.
- **Watchlist**: Users can watch items and get "Ending Soon" notifications.
- **Auction Discovery**: Explore trending and recommended auctions.

### 💳 Payments & Commission
- **Winner Checkout**: Seamless flow for winning bidders.
- **Payment Options**: UPI, Bank Transfer, COD, QR Code.
- **Commission System**:
  - *10% commission from Seller*
  - *3% commission from Buyer*
- **Payment Proof Upload**: Users upload payment screenshots for verification.
- **Escrow Flow**: `Pending Payment` → `Paid` → `Shipped` → `Delivered` → `Completed`.

### 🧾 Invoice & Receipts
- Automatic generation of detailed invoices.
- **PDF Download**: Support for downloading payment receipts (via WeasyPrint).

### ⭐ User System & Dashboard
- **Clean Dashboard**: Stats cards for My Bids, My Auctions, Watchlist, Payments, and Disputes.
- **Reputation System**: Buyer ↔ Seller ratings (1–5 stars) after completed transactions.
- **Notifications**: Email & In-app alerts for outbid, won, paid, shipped events.
- **Report System**: Users can report auctions or other users.
- **Dispute Management**: Raise and track disputes on transactions.

---

## 🛠 Tech Stack

- **Backend**: Django 6.0, Python 3.12
- **Database**: SQLite (Dev) / PostgreSQL compatible
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Real-Time**: Django Channels (WebSockets)
- **PDF Generation**: WeasyPrint

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Dimanjan/aliaunction.git
cd aliaunction
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# If WeasyPrint has issues on macOS: brew install weasyprint
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Seed Test Data (Recommended)
This command populates the database with realistic test data:
```bash
python manage.py seed_data
```
Creates:
- **Admin**: `admin` / `admin123`
- **Sellers**: `seller1`, `seller2`, `seller3` / `password123`
- **Buyers**: `buyer1`, `buyer2`, `buyer3`, `buyer4` / `password123`
- 8 Categories, 10 Auctions, 27 Bids, 12 Watchlist entries

### 7. Run Server
```bash
python manage.py runserver 8001
```

### 8. Access Application
| Page | URL |
|------|-----|
| Homepage | http://localhost:8001/ |
| Admin | http://localhost:8001/admin/ |
| Marketplace | http://localhost:8001/marketplace/live-auctions/ |
| Dashboard | http://localhost:8001/dashboard/ |
| Auctions | http://localhost:8001/auctions/ |
| Discover | http://localhost:8001/discover/ |

---

## 🔒 Security Features
- **CSRF & XSS Protection**: Native Django security.
- **Rate Limiting**: Custom decorators for sensitive actions.
- **Input Validation**: Extensive model and form validation.
- **Secure File Uploads**: Validated image uploads.

---

## 📋 Recent Updates

**Version 2.2 - Jan 19, 2026**
- Redesigned auction detail page with 3-column layout
- Fixed template namespacing for reports and disputes apps
- Removed animations from dashboard for cleaner UX
- Fixed create auction form syntax errors
- Code formatting and cleanup

**Version 2.1 - Jan 2026**
- Added: Anti-Sniping, Rate Limiting, Bulk Upload, Watchlist Notifications, Escrow Services.

