# Design Guidelines

## Design Philosophy: The 2026 Pivot

Two dominant styles are converting well—choose based on audience:

### 1. Modern/Polished (Agentic)
**Best for:** Enterprise SaaS, Fintech, B2B, Security products

- 3D renders, glassmorphism
- Complex gradients (mesh gradients)
- Sans-serif geometric fonts
- Perfect whitespace
- Dark mode with neon accents
- Signals: competence, scale, technology

### 2. Human/Authentic (Raw)
**Best for:** Creator economy, Micro-SaaS, Coaching, DTC brands

- Hand-drawn elements (arrows, underlines)
- Organic shapes, anti-grid layouts
- Serif fonts for warmth
- Real photos (not stock)
- Document/Notion-like aesthetic
- Signals: authenticity, trust, personality

### 3. Hybrid (Recommended Default)
**Best of both worlds:**

- Clean infrastructure (fast loading, clear hierarchy)
- Human elements layered on top (handwritten annotations, real photos)
- Serif headlines + Sans-serif body text
- Minimal but warm color palette

---

## Color Psychology by Product Type

| Product Category | Primary Colors | Accent | Psychology |
|-----------------|----------------|--------|------------|
| SaaS/Tech | Deep blue, Charcoal | Electric blue, Lime | Trust, Innovation |
| Finance | Navy, Forest green | Gold | Security, Growth |
| Health/Wellness | Sage green, Lavender | Warm coral | Calm, Care |
| Creative Tools | Purple, Teal | Magenta, Orange | Creativity, Energy |
| Education | Teal, Deep orange | Yellow | Knowledge, Clarity |
| E-commerce | Warm neutrals | Red/Orange for CTA | Action, Urgency |

### 2026 Trending Palettes

1. **"Naturaleza Destilada"** (Earthy)
   - Verdant green, Terracotta, Warm beige
   - Use for: Wellness, Eco-tech, Lifestyle

2. **"Lavanda Digital"** (Soft Pop)
   - Light purple, Soft teal, Sunny yellow
   - Use for: Gen-Z products, Creative tools

3. **"Modo Oscuro Evolucionado"**
   - Charcoal #121212 (not pure black)
   - Neon accents (lime, electric blue, magenta)
   - Use for: Developer tools, Analytics, B2B SaaS

---

## CTA Button Colors

**Rule:** CTA color must be used ONLY for CTAs. High contrast against background.

| Background | Optimal CTA Color |
|-----------|------------------|
| White | Orange, Green, Blue |
| Dark | Lime, Coral, Electric blue |
| Blue-based | Orange, Yellow |
| Green-based | Purple, Red-orange |

**Key stat:** Changing CTA to high-contrast color increases conversions by 21%.

---

## Typography

### Avoid (Generic AI-slop fonts):
- Inter
- Roboto
- Arial
- System fonts

### Recommended Pairings:

**Modern/Tech:**
- Headlines: Graphik, Sohne, Satoshi
- Body: Inter (only as body), DM Sans

**Human/Warm:**
- Headlines: Fraunces, Playfair Display, Crimson Pro
- Body: Source Serif Pro, Lora

**Bold/Creative:**
- Headlines: Space Grotesk, Clash Display
- Body: General Sans, Plus Jakarta Sans

### Typography Specs:

| Element | Desktop | Mobile | Weight |
|---------|---------|--------|--------|
| H1 | 48-60px | 32-40px | 700-900 |
| H2 | 32-40px | 24-32px | 600-700 |
| H3 | 24-28px | 20-24px | 600 |
| Body | 16-18px | 16px | 400-500 |
| CTA | 16-18px | 16px | 600-700 |

**Letter spacing for headlines:** -0.4px to -1px (tighter is more impactful)

---

## Layout Patterns

### Hero Section Layouts

1. **Split Screen (Recommended for SaaS)**
   - Left: Copy + CTA
   - Right: Product demo/screenshot
   - 50/50 or 55/45 split

2. **Centered (Minimal)**
   - Centered headline + CTA
   - Full-width product image below
   - Best for simple products

3. **Video Hero**
   - Background video (muted, looping)
   - Overlay with headline + CTA
   - Best for storytelling brands

### Content Section Patterns

1. **Bento Grid**
   - Best for: Features, integrations
   - Modular boxes of varying sizes
   - ⚠️ Make truly responsive (not just stacked)

2. **Alternating Columns (Z-Pattern)**
   - Best for: Narrative flow, step-by-step
   - Text left, image right (alternate)
   - Controls reading pace

3. **Card Grid**
   - Best for: Pricing, team, testimonials
   - Equal-sized cards
   - 3 columns desktop, 1 column mobile

---

## Mobile-First Design Rules

1. **Thumb Zone Priority**
   - CTAs in bottom 1/3 of screen
   - Navigation at bottom (not top)
   - Key actions accessible with one hand

2. **Touch Targets**
   - Minimum 48px × 48px
   - 8px minimum spacing between targets

3. **Sticky Elements**
   - Sticky CTA bar at bottom (12-32% conversion lift)
   - Show only after first scroll
   - Include price/offer summary

4. **Content Adaptation**
   - Reduce testimonials (3 max on mobile)
   - Collapse FAQ by default
   - Remove decorative elements
   - Simplify forms (even more)

---

## Micro-Interactions & Animation

### High-Impact Moments (Focus Here):

1. **Page Load**
   - Staggered fade-in for sections
   - Hero animation on arrival
   - Logo bar subtle entrance

2. **Scroll Triggers**
   - Elements animate as they enter viewport
   - Parallax on hero background (subtle)
   - Counter animations for stats

3. **Hover States**
   - CTA buttons: Slight scale (1.02-1.05)
   - Cards: Subtle lift/shadow
   - Links: Color shift or underline animation

### Animation Specs:

| Animation Type | Duration | Easing |
|---------------|----------|--------|
| Fade in | 300-500ms | ease-out |
| Slide in | 400-600ms | ease-out |
| Button hover | 150-200ms | ease-in-out |
| Card lift | 200ms | ease-out |

**Principle:** One well-orchestrated page load > scattered micro-interactions

---

## Visual Trust Signals

### Above the Fold:
- Client logos (4-6)
- Star rating + review count
- "As featured in" media logos
- User count ("10,000+ teams")

### Near CTAs:
- Security badges
- Money-back guarantee
- "No credit card required"
- SSL/payment icons for checkout

### Footer:
- Privacy/Terms links
- Company address
- Contact information
- Social proof badges (G2, Capterra)

---

## Performance Requirements

| Metric | Target | Impact |
|--------|--------|--------|
| First Contentful Paint | <1.5s | User perception |
| Largest Contentful Paint | <2.5s | SEO + UX |
| Total Blocking Time | <200ms | Interactivity |
| Cumulative Layout Shift | <0.1 | Visual stability |

### Optimization Checklist:
- [ ] Images in WebP/AVIF format
- [ ] Lazy loading below fold
- [ ] System fonts for body text (optional)
- [ ] CSS animations over JS
- [ ] Critical CSS inlined
- [ ] Fonts preloaded
