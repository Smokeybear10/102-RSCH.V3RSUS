# Website Structure Guide

Patterns distilled from D4NCE, SWIFTIFY, and thomasou.com portfolio sites.

---

## 1. Page Anatomy

Every page follows a consistent vertical hierarchy:

```
NAVBAR (fixed/sticky, persistent across routes)
  Logo + Brand + "by Thomas Ou"
  Navigation links (icon + text on desktop, icon-only on mobile)

HERO SECTION (above the fold)
  Page title (display font, large)
  Subtitle / description
  Optional CTA or featured content

CONTENT SECTIONS (scrollable)
  Section label (tiny uppercase)
  Section content (cards, tables, inputs, visualizations)
  Dividers between sections

FOOTER / CLOSING (bottom anchor)
  Tagline or attribution
  Links (GitHub, contact)
```

## 2. Navigation

- **Persistent**: Always visible (sticky top or fixed bottom)
- **Branded**: Logo on the left with tagline, links on the right
- **Active state**: Underline animation or highlight for current route/section
- **Mobile**: Icon-only nav or hamburger menu at breakpoint
- **Glassmorphism**: Semi-transparent background with `backdrop-filter: blur()`

## 3. Section Structure

Each content block follows the pattern:

```html
<section class="section">
  <div class="section-label">SECTION NAME</div>
  <div class="section-content">
    <!-- Cards, grids, tables, etc. -->
  </div>
</section>
```

- **Section labels**: `font-size: 0.6-0.7rem`, uppercase, wide letter-spacing, dim color
- **Glass cards**: `background: rgba(...)`, `border: 1px solid rgba(...)`, `backdrop-filter: blur()`
- **Consistent padding**: Cards use `1.5-2.5rem` internal padding
- **Border radius**: `12-24px` for cards, `8-10px` for inputs, `100px` for pills/buttons

## 4. Typography Hierarchy

Three font roles:

| Role        | Font Example     | Usage                              |
|-------------|------------------|------------------------------------|
| Display     | Montserrat 900   | Logo, page titles, winner names    |
| Label       | Montserrat 600   | Section labels, tags, buttons      |
| Body        | Inter 400-600    | Stats, descriptions, inputs        |

- Titles: `clamp(min, preferred, max)` for fluid scaling
- Labels: `text-transform: uppercase; letter-spacing: 0.08-0.15em`
- Values: `font-variant-numeric: tabular-nums` for aligned numbers
- Line height: `1.5-1.65` for body text

## 5. Background Atmosphere

Layer multiple effects for depth (all `position: fixed; pointer-events: none`):

| Layer | z-index | Effect                                          |
|-------|---------|------------------------------------------------|
| 0     | -1      | Animated gradient orbs (blur 100-120px)         |
| 1     | 0       | Radial gradient backdrop (animated position)    |
| 2     | 1       | Dot grid texture (32px spacing, ~6% opacity)    |
| 3     | 2       | SVG noise overlay (fractal noise, ~2.5% opacity)|

## 6. Color Strategy

- **Dark base**: `#080a10` to `#0d1117` (near-black with slight color tint)
- **Accent colors**: 1-2 saturated hues for theming (red/blue for MMA, pink for music, purple/cyan for DJ)
- **Text hierarchy**: Primary (~95% white), Muted (~45% white), Dim (~25% white)
- **Borders**: `rgba(255,255,255, 0.06-0.12)` — barely visible, just enough separation
- **Glow effects**: `box-shadow: 0 0 20-30px rgba(accent, 0.15-0.3)` on hover/focus

## 7. Animation Patterns

### Page entrance
Staggered `fadeInUp` on direct children of the page container:
```css
.container > *:nth-child(1) { animation-delay: 0.05s; }
.container > *:nth-child(2) { animation-delay: 0.12s; }
.container > *:nth-child(3) { animation-delay: 0.19s; }
```

### Scroll reveal
Elements start dimmed/translated, animate to full opacity when scrolled into view via `IntersectionObserver`.

### Micro-interactions
- Hover: `translateY(-2px)`, border brightens, subtle shadow
- Active: `translateY(0)`, shadow reduces
- Focus: Colored `box-shadow` ring matching section theme
- Transitions: `0.2-0.3s ease` for most, `0.8-1.2s cubic-bezier` for data bars

## 8. Responsive Strategy

- **Primary breakpoint**: `768px` (mobile/desktop split)
- **Fluid typography**: `clamp()` everywhere instead of media query font changes
- **Grid collapse**: Multi-column grids become single-column on mobile
- **Nav adaptation**: Text labels hide, icons remain
- **Safe areas**: `env(safe-area-inset-*)` for notched devices
- **Touch targets**: Minimum 44px interactive elements on mobile

## 9. Component Patterns

### Card
```css
background: rgba(12, 16, 26, 0.65);
border: 1px solid rgba(255, 255, 255, 0.06);
border-radius: 16-24px;
backdrop-filter: blur(20px);
padding: 1.5-2.5rem;
box-shadow: 0 24px 80px rgba(0,0,0,0.5);
```

### Stat Item
```html
<div class="stat-item">
  <span class="stat-label">LABEL</span>
  <span class="stat-value">Value</span>
</div>
```

### Comparison Row
```
Left Value | Label + Bar | Right Value
```
Bars proportional to values, brighter bar = advantage.

### Tags / Pills
```css
font-size: 0.6rem;
padding: 0.15-0.25rem 0.5rem;
border-radius: 100px;
background: rgba(accent, 0.12);
border: 1px solid rgba(accent, 0.2);
```

## 10. Data Presentation

- **Probability bars**: Dual-sided, proportional width, contrasting colors
- **Comparison tables**: Side-by-side with visual bars, advantage highlighting
- **Stat grids**: 2-column grid of label/value pairs inside cards
- **Charts**: Horizontal bar charts for categorical data (win methods, etc.)
- **Numbers**: Monospace/tabular for alignment, 1 decimal place max

## 11. Scrollbar & Selection

```css
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
::selection { background: rgba(accent, 0.3); color: #fff; }
```

## 12. File Organization

```
project/
├── static/ or app/
│   ├── index.html          # Single entry point
│   ├── style.css           # All styles (or modular CSS)
│   └── script.js           # Client logic
├── src/                    # Backend / ML code
├── data/                   # Datasets
├── docs/                   # Documentation
└── app.py / server.js      # Server entry point
```

For vanilla projects, keep it simple: one HTML, one CSS, one JS. Split CSS into sections with clear comment headers.
