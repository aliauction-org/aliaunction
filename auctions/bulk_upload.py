"""
Bulk upload functionality for auctions via CSV.
"""
import csv
import io
from decimal import Decimal, InvalidOperation
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Auction, Category
from auction_workflow.models import AuctionWorkflow
from reserve_price.models import ReservePrice


def parse_datetime(date_string):
    """Parse various datetime formats."""
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M',
        '%d/%m/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M',
    ]
    for fmt in formats:
        try:
            return timezone.make_aware(datetime.strptime(date_string.strip(), fmt))
        except ValueError:
            continue
    return None


def validate_row(row, row_num, categories):
    """Validate a single CSV row."""
    errors = []
    
    # Required fields
    required = ['title', 'description', 'starting_price', 'end_time']
    for field in required:
        if not row.get(field, '').strip():
            errors.append(f"Row {row_num}: Missing required field '{field}'")
    
    # Validate starting_price
    try:
        price = Decimal(row.get('starting_price', '0'))
        if price <= 0:
            errors.append(f"Row {row_num}: Starting price must be greater than 0")
    except (InvalidOperation, ValueError):
        errors.append(f"Row {row_num}: Invalid starting price format")
    
    # Validate end_time
    end_time = parse_datetime(row.get('end_time', ''))
    if not end_time:
        errors.append(f"Row {row_num}: Invalid end_time format. Use YYYY-MM-DD HH:MM:SS")
    elif end_time <= timezone.now():
        errors.append(f"Row {row_num}: End time must be in the future")
    
    # Validate reserve_price if provided
    reserve = row.get('reserve_price', '').strip()
    if reserve:
        try:
            reserve_decimal = Decimal(reserve)
            if reserve_decimal <= 0:
                errors.append(f"Row {row_num}: Reserve price must be greater than 0")
        except (InvalidOperation, ValueError):
            errors.append(f"Row {row_num}: Invalid reserve price format")
    
    # Validate category if provided
    category_name = row.get('category', '').strip()
    if category_name and category_name not in categories:
        errors.append(f"Row {row_num}: Unknown category '{category_name}'")
    
    return errors


@login_required
def bulk_upload_auctions(request):
    """Handle CSV upload for bulk auction creation."""
    # Get available categories for template
    categories = {c.name: c for c in Category.objects.filter(is_active=True)}
    
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file:
            messages.error(request, 'Please select a CSV file to upload.')
            return redirect('bulk_upload_auctions')
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File must be a CSV file.')
            return redirect('bulk_upload_auctions')
        
        try:
            # Read CSV
            decoded = csv_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            
            # Validate all rows first
            rows = list(reader)
            all_errors = []
            
            for i, row in enumerate(rows, start=2):  # Start at 2 (after header)
                errors = validate_row(row, i, categories)
                all_errors.extend(errors)
            
            if all_errors:
                for error in all_errors[:10]:  # Show first 10 errors
                    messages.error(request, error)
                if len(all_errors) > 10:
                    messages.error(request, f'...and {len(all_errors) - 10} more errors')
                return redirect('bulk_upload_auctions')
            
            # Create auctions
            created_count = 0
            for row in rows:
                auction = Auction.objects.create(
                    title=row['title'].strip(),
                    description=row['description'].strip(),
                    starting_price=Decimal(row['starting_price']),
                    current_price=Decimal(row['starting_price']),
                    end_time=parse_datetime(row['end_time']),
                    owner=request.user,
                    is_active=True,
                    category=categories.get(row.get('category', '').strip()),
                )
                
                # Create workflow entry (starts as DRAFT)
                AuctionWorkflow.objects.create(
                    auction=auction,
                    status='DRAFT'
                )
                
                # Create reserve price if provided
                reserve = row.get('reserve_price', '').strip()
                if reserve:
                    ReservePrice.objects.create(
                        auction=auction,
                        amount=Decimal(reserve),
                        seller_only=True
                    )
                
                created_count += 1
            
            messages.success(request, f'Successfully created {created_count} auctions as drafts.')
            return redirect('my_auctions')
            
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            return redirect('bulk_upload_auctions')
    
    return render(request, 'auctions/bulk_upload.html', {
        'categories': categories.keys()
    })


@login_required
def download_csv_template(request):
    """Provide a sample CSV template for bulk upload."""
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="auction_template.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['title', 'description', 'starting_price', 'end_time', 'category', 'reserve_price'])
    writer.writerow([
        'Sample Auction Title',
        'This is a detailed description of the item being auctioned.',
        '1000.00',
        '2025-12-31 18:00:00',
        'Electronics',
        '1500.00'
    ])
    
    return response
