# AuctionVistas Style Guide

## 🎨 Brand Identity

**Platform Name**: AuctionVistas  
**Tagline**: "Discover & Bid on Unique Items"  
**Brand Promise**: Your trusted platform for discovering, bidding, and winning unique items

---

## 🎯 Color Palette

### Primary Colors
- **Primary Green**: `#10b981` (Emerald Green)
  - Used for: Primary buttons, links, highlights, success states
  - RGB: `rgb(16, 185, 129)`
  
- **Secondary Green**: `#34d399` (Light Emerald)
  - Used for: Hover states, secondary elements
  - RGB: `rgb(52, 211, 153)`
  
- **Dark Green**: `#059669` (Dark Emerald)
  - Used for: Active states, pressed buttons
  - RGB: `rgb(5, 150, 105)`

### Blue Accent Colors
- **Primary Blue**: `#3a8dde` (Ocean Blue)
  - Used for: Links, secondary buttons, navigation
  - RGB: `rgb(58, 141, 222)`
  
- **Light Blue**: `#7ecbff` (Sky Blue)
  - Used for: Gradients, backgrounds, highlights
  - RGB: `rgb(126, 203, 255)`

### Neutral Colors
- **Dark Text**: `#23284a` (Navy Blue)
  - Used for: Headings, primary text
  - RGB: `rgb(35, 40, 74)`
  
- **Medium Text**: `#666666` (Gray)
  - Used for: Secondary text, descriptions
  - RGB: `rgb(102, 102, 102)`
  
- **Light Text**: `#b0b6d6` (Light Gray)
  - Used for: Muted text, captions
  - RGB: `rgb(176, 182, 214)`

### Background Colors
- **Primary Background**: `#f8fafc` (Very Light Gray)
  - Used for: Main content areas, cards
  - RGB: `rgb(248, 250, 252)`
  
- **Secondary Background**: `#f0fff4` (Very Light Green)
  - Used for: Success states, info boxes
  - RGB: `rgb(240, 255, 244)`
  
- **Tertiary Background**: `#f8f9fa` (Light Gray)
  - Used for: Sidebars, alternate sections
  - RGB: `rgb(248, 249, 250)`
  
- **Border Gray**: `#e2e8f0` (Light Border)
  - Used for: Borders, dividers
  - RGB: `rgb(226, 232, 240)`

### Status Colors
- **Success**: `#10b981` (Green)
- **Error**: `#dc2626` (Red) - Use sparingly
- **Warning**: `#f59e0b` (Amber)
- **Info**: `#3a8dde` (Blue)

---

## 🔤 Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             'Helvetica Neue', Arial, sans-serif;
```

### Font Sizes & Weights

#### Headings
- **H1**: `2.5rem` (40px) - Bold (700)
  - Used for: Page titles, hero sections
  
- **H2**: `2rem` (32px) - Bold (700)
  - Used for: Section headers, article titles
  
- **H3**: `1.5rem` (24px) - Bold (600)
  - Used for: Subsection headers, card titles
  
- **H4**: `1.25rem` (20px) - Semi-bold (600)
  - Used for: Small headers, form labels

#### Body Text
- **Large**: `1.1rem` (17.6px) - Normal (400)
  - Used for: Important content, descriptions
  
- **Regular**: `1rem` (16px) - Normal (400)
  - Used for: Body text, paragraphs
  
- **Small**: `0.9rem` (14.4px) - Normal (400)
  - Used for: Captions, metadata, help text

#### Special Text
- **Button Text**: `1rem` (16px) - Semi-bold (600)
- **Navigation**: `1rem` (16px) - Medium (500)
- **Form Labels**: `1rem` (16px) - Semi-bold (600)

### Line Heights
- **Headings**: `1.2` (tight)
- **Body Text**: `1.6` (comfortable reading)
- **Buttons**: `1.5` (balanced)

---

## 🎨 Component Styles

### Buttons

#### Primary Button
```css
background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
color: white;
padding: 0.8rem 1.5rem;
border-radius: 8px;
font-weight: 600;
border: none;
transition: transform 0.3s ease;
```

#### Secondary Button
```css
background: #3a8dde;
color: white;
padding: 0.8rem 1.5rem;
border-radius: 8px;
font-weight: 600;
border: none;
transition: background 0.3s ease;
```

#### Ghost Button
```css
background: transparent;
color: #3a8dde;
padding: 0.8rem 1.5rem;
border-radius: 8px;
font-weight: 600;
border: 2px solid #3a8dde;
transition: all 0.3s ease;
```

### Cards
```css
background: white;
border-radius: 12px;
box-shadow: 0 4px 15px rgba(0,0,0,0.1);
padding: 1.5rem;
transition: transform 0.3s ease;
```

### Form Elements
```css
input, select, textarea {
    padding: 0.8rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #10b981;
}
```

### Badges & Tags
```css
.badge {
    background: #10b981;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}
```

---

## 📐 Layout & Spacing

### Grid System
- **Container Max Width**: `2400px`
- **Grid Gap**: `1.5rem` (24px)
- **Section Padding**: `2rem` (32px)

### Spacing Scale
- **XS**: `0.5rem` (8px) - Small gaps
- **S**: `1rem` (16px) - Standard spacing
- **M**: `1.5rem` (24px) - Component spacing
- **L**: `2rem` (32px) - Section spacing
- **XL**: `3rem` (48px) - Large sections
- **XXL**: `4rem` (64px) - Hero sections

### Breakpoints
```css
/* Mobile First */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1280px) { /* Large Desktop */ }
```

---

## 🎭 Interactive States

### Hover Effects
- **Buttons**: `transform: translateY(-2px)`
- **Cards**: `transform: translateY(-5px)`
- **Links**: Color change to `#10b981`

### Focus States
- **Form Elements**: Green border (`#10b981`)
- **Buttons**: Box shadow with green tint
- **Links**: Underline or background highlight

### Active States
- **Buttons**: `transform: translateY(0)`
- **Links**: Darker color variant

---

## 📱 Responsive Design

### Mobile (< 768px)
- Single column layouts
- Stacked navigation
- Larger touch targets (44px minimum)
- Reduced padding and margins

### Tablet (768px - 1024px)
- Two-column grids where appropriate
- Sidebar navigation
- Medium padding and margins

### Desktop (> 1024px)
- Multi-column layouts
- Horizontal navigation
- Full padding and margins
- Hover effects enabled

---

## 🎨 Page-Specific Guidelines

### Homepage
- **Hero Section**: Dark gradient background (`#23284a` to `#2b3a67`)
- **Auction Cards**: White background with shadow
- **CTA Buttons**: Green gradient with hover effects

### Auction Pages
- **Current Bid**: Large, prominent display
- **Timer**: Red or green based on urgency
- **Bid Button**: Primary green with clear hierarchy

### News/Blog Pages
- **Article Cards**: Clean white background
- **Featured Articles**: Larger cards with green accents
- **Categories**: Green badges with white text

### User Authentication
- **Form Background**: Light gray (`#f8fafc`)
- **Success Messages**: Green background (`#f0fff4`)
- **Error Messages**: Green background with red text

---

## 🚫 Design Don'ts

### Color Usage
- ❌ Never use pink colors (`#ff4b6e`, `#ff6b8a`, `#e53e3e`)
- ❌ Don't use pure black text
- ❌ Avoid high contrast red backgrounds
- ❌ Don't mix too many colors in one component

### Typography
- ❌ Don't use more than 3 font sizes on one page
- ❌ Avoid all caps for body text
- ❌ Don't use decorative fonts for UI elements
- ❌ Avoid text smaller than 14px

### Layout
- ❌ Don't center large blocks of text
- ❌ Avoid orphaned words in headings
- ❌ Don't use too many different border radius values
- ❌ Avoid inconsistent spacing

### Interactions
- ❌ Don't use red for success states
- ❌ Avoid auto-playing animations
- ❌ Don't hide important information in hover states
- ❌ Avoid complex hover effects on mobile

---

## ✅ Design Do's

### Color Usage
- ✅ Use green as the primary brand color
- ✅ Maintain consistent color hierarchy
- ✅ Use neutral backgrounds for content areas
- ✅ Apply colors with purpose and meaning

### Typography
- ✅ Use the established font hierarchy
- ✅ Maintain consistent line heights
- ✅ Use proper contrast ratios (4.5:1 minimum)
- ✅ Keep text readable and scannable

### Layout
- ✅ Use consistent spacing throughout
- ✅ Maintain visual hierarchy
- ✅ Create clear content sections
- ✅ Use whitespace effectively

### Interactions
- ✅ Provide clear feedback for all interactions
- ✅ Use consistent hover and focus states
- ✅ Ensure accessibility compliance
- ✅ Test interactions across devices

---

## 🔧 CSS Variables

For consistent implementation, use these CSS custom properties:

```css
:root {
  /* Colors */
  --color-primary: #10b981;
  --color-primary-light: #34d399;
  --color-primary-dark: #059669;
  --color-secondary: #3a8dde;
  --color-secondary-light: #7ecbff;
  --color-text-dark: #23284a;
  --color-text-medium: #666666;
  --color-text-light: #b0b6d6;
  --color-background: #f8fafc;
  --color-background-light: #f0fff4;
  --color-border: #e2e8f0;
  
  /* Typography */
  --font-size-xs: 0.8rem;
  --font-size-sm: 0.9rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.1rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 2rem;
  --font-size-4xl: 2.5rem;
  
  /* Spacing */
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;
  --spacing-2xl: 4rem;
  
  /* Border Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 18px;
  
  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 15px rgba(0,0,0,0.1);
  --shadow-lg: 0 8px 25px rgba(0,0,0,0.15);
}
```

---

## 📋 Implementation Checklist

### Before Launch
- [ ] All pink colors replaced with green
- [ ] Consistent typography hierarchy applied
- [ ] Responsive breakpoints tested
- [ ] Accessibility contrast ratios verified
- [ ] Hover and focus states implemented
- [ ] CSS variables used consistently
- [ ] Cross-browser compatibility tested
- [ ] Mobile usability verified

### Maintenance
- [ ] Regular color consistency audits
- [ ] Typography hierarchy reviews
- [ ] Responsive design testing
- [ ] Accessibility compliance checks
- [ ] Performance optimization reviews

---

*This style guide ensures consistent, professional design across all AuctionVistas pages and components. Follow these guidelines to maintain brand integrity and user experience quality.* 