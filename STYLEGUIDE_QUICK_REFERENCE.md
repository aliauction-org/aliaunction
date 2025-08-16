# AuctionVistas Quick Reference Card

## 🎨 Essential Colors

### Primary Green Palette
- **Primary**: `#10b981` - Buttons, links, highlights
- **Light**: `#34d399` - Hover states
- **Dark**: `#059669` - Active states

### Blue Accents
- **Primary Blue**: `#3a8dde` - Secondary buttons, navigation
- **Light Blue**: `#7ecbff` - Gradients, backgrounds

### Text Colors
- **Dark**: `#23284a` - Headings, primary text
- **Medium**: `#666666` - Secondary text
- **Light**: `#b0b6d6` - Muted text

### Backgrounds
- **Primary**: `#f8fafc` - Content areas
- **Success**: `#f0fff4` - Success states
- **Border**: `#e2e8f0` - Borders, dividers

## 🔤 Typography Quick Reference

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             'Helvetica Neue', Arial, sans-serif;
```

### Key Sizes
- **H1**: `2.5rem` (40px) - Bold 700
- **H2**: `2rem` (32px) - Bold 700  
- **H3**: `1.5rem` (24px) - Bold 600
- **Body**: `1rem` (16px) - Normal 400
- **Small**: `0.9rem` (14px) - Normal 400

## 🎯 Component Standards

### Primary Button
```css
background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
color: white;
padding: 0.8rem 1.5rem;
border-radius: 8px;
font-weight: 600;
```

### Card
```css
background: white;
border-radius: 12px;
box-shadow: 0 4px 15px rgba(0,0,0,0.1);
padding: 1.5rem;
```

### Form Input
```css
padding: 0.8rem;
border: 2px solid #e2e8f0;
border-radius: 8px;
font-size: 1rem;
```

## 📐 Spacing Scale
- **XS**: `0.5rem` (8px)
- **S**: `1rem` (16px)
- **M**: `1.5rem` (24px)
- **L**: `2rem` (32px)
- **XL**: `3rem` (48px)

## 🚫 Never Use
- ❌ Pink colors (`#ff4b6e`, `#ff6b8a`, `#e53e3e`)
- ❌ Pure black text
- ❌ Text smaller than 14px
- ❌ More than 3 font sizes per page

## ✅ Always Use
- ✅ Green as primary brand color
- ✅ Consistent spacing
- ✅ Proper contrast ratios (4.5:1 minimum)
- ✅ Responsive design principles

## 📱 Breakpoints
```css
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1280px) { /* Large Desktop */ }
```

### Grid System
- **Container Max Width**: `2400px`
- **Grid Gap**: `1.5rem` (24px)
- **Section Padding**: `2rem` (32px)

---

*Quick reference for maintaining consistent design across AuctionVistas* 