# Conversion Elements

## CTA Button Optimization

### Placement Strategy

| Location | Purpose | Conversion Impact |
|----------|---------|------------------|
| Hero (above fold) | Primary conversion | Highest priority |
| After problem section | Catch motivated readers | High |
| After social proof | Leverage trust momentum | High |
| After pricing | Capture decision-makers | High |
| Sticky bar (mobile) | Always accessible | +12-32% mobile CVR |
| Exit intent popup | Last chance | +5-10% recovery |

### Sticky CTA Implementation

**Desktop:** Sticky header with CTA after 50% scroll
**Mobile:** Bottom bar that appears after first scroll

```css
/* Mobile sticky CTA */
.sticky-cta {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  background: white;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  z-index: 1000;
}
```

### CTA Button Anatomy

```
┌─────────────────────────────────────┐
│         Start My Free Trial         │  ← Primary text (action + benefit)
└─────────────────────────────────────┘
         No credit card required          ← Micro-copy (objection handler)
```

### Button Text Hierarchy (Best to Worst)

1. **Personalized + Outcome:** "Get My Free Audit"
2. **Outcome-focused:** "Start Saving Time"
3. **Action + Benefit:** "Try Free for 14 Days"
4. **Simple Action:** "Get Started"
5. ❌ **Generic:** "Submit", "Learn More", "Click Here"

### Objection Handler Examples

| CTA | Micro-copy |
|-----|-----------|
| Start Free Trial | No credit card required |
| Get My Report | Free, takes 2 minutes |
| Book a Demo | 15 min, no commitment |
| Buy Now | 30-day money-back guarantee |
| Download Free | No spam, ever |
| Join Waitlist | Be first to know |

---

## Form Optimization

### Field Reduction Data

| Fields | Conversion Rate |
|--------|----------------|
| 3 fields | 10% |
| 4 fields | 8% |
| 5 fields | 6% |
| 6+ fields | <5% |

**Rule:** Reduce from 11 to 4 fields = +120% conversions

### Minimum Viable Forms

**Lead Magnet:** Email only
**Free Trial:** Email + Password
**SaaS Signup:** Email + Password + Name
**Demo Request:** Email + Name + Company + Phone

### Multi-Step Form Strategy

For longer forms, use progressive disclosure:

**Step 1 (Low friction):**
- "What's your goal?" (radio buttons)
- "What's your company size?" (dropdown)

**Step 2 (Medium friction):**
- Name
- Email

**Step 3 (Higher friction):**
- Phone (optional)
- Company details

**Why it works:** Sunk cost fallacy—after Step 1, users feel invested

### Form Design Best Practices

1. **Label placement:** Above field (not placeholder text as label)
2. **Field size:** Full width on mobile, 50-60% on desktop
3. **Error handling:** Inline, real-time validation
4. **Submit button:** Full width, high contrast
5. **Progress indicator:** For multi-step forms
6. **Autofill support:** Enable browser autofill

---

## Pricing Section

### The 3-Tier Psychology

```
┌─────────┐  ┌─────────────┐  ┌─────────┐
│  Starter │  │   PRO ⭐    │  │ Business│
│   $9/mo  │  │  $29/mo     │  │  $99/mo │
│          │  │ MOST POPULAR│  │         │
└─────────┘  └─────────────┘  └─────────┘
```

**Goldilocks Effect:** Most users pick the middle tier when properly highlighted.

### Pricing Table Elements

1. **Tier name:** Clear hierarchy (Starter → Pro → Enterprise)
2. **Price:** Monthly with annual savings shown
3. **Feature list:** 5-7 features per tier
4. **Differentiator:** What makes each tier different
5. **CTA:** Under each tier (same or differentiated)
6. **Highlight:** "Most Popular" or "Best Value" badge

### Monthly vs Annual Toggle

```
┌─────────────────────────────────┐
│  ○ Monthly    ● Annual (17% off) │
└─────────────────────────────────┘
```

**Best practices:**
- Default to Annual (higher revenue)
- Show savings clearly ("2 months free")
- Or: Default to Monthly (lower barrier) for acquisition focus

### Price Anchoring

**Strategy 1:** Show original price crossed out
```
$99/mo → $49/mo (50% off)
```

**Strategy 2:** Compare to competitor pricing
```
"Same features as [Competitor] at half the price"
```

**Strategy 3:** Value stack comparison
```
Value: $2,000+ → Your price: $299
```

### Enterprise Pricing

When to use "Contact Us":
- Only for truly variable pricing (usage-based, custom)
- Always include "Starting at $X" if possible

Include:
- Expected response time
- What the call covers
- Social proof specific to enterprise

---

## Risk Reversal

### Types of Guarantees

| Type | Best For | Copy Example |
|------|----------|--------------|
| Money-back | Products, courses | "30-day money-back guarantee" |
| Free trial | SaaS | "14-day free trial, no card required" |
| Results-based | Services | "Full refund if no ROI in 90 days" |
| Satisfaction | General | "Not happy? We'll make it right" |

### Placement

1. **Near CTA:** Directly under or beside the button
2. **Pricing section:** Under each tier
3. **Final CTA block:** Reinforce before final conversion
4. **FAQ:** Address as a question

### Guarantee Copy Examples

**SaaS:**
```
Try risk-free for 14 days. No credit card required.
Cancel anytime with one click.
```

**Course:**
```
30-day money-back guarantee. If you don't love it, 
email us for a full refund. No questions asked.
```

**Service:**
```
Not satisfied? We'll work until you are—or refund 100%.
```

---

## Urgency & Scarcity

### Authentic Urgency (Use)

- Limited-time pricing (actual deadline)
- Cohort-based enrollment (actual start date)
- Limited spots (actual capacity)
- Bonus expiration (actual removal date)

### Fake Urgency (Avoid)

- Countdown timers that reset
- "Only 3 left!" when unlimited
- Fake scarcity for digital products
- Permanent "sale" pricing

### Implementation

**Countdown timer:** Only for real deadlines
```
Price increases in: 2d 14h 32m
```

**Stock indicator:** Only for real limits
```
87% enrolled — 13 spots remaining
```

**Social proof urgency:**
```
127 people viewing this page
23 signed up in the last hour
```

---

## Exit Intent Strategy

### When to Use

- High-value pages (pricing, checkout)
- Lead magnets with low conversion
- After significant time on page (>30s)

### Exit Intent Offers

1. **Discount:** "Wait! Get 10% off your first month"
2. **Alternative offer:** "Not ready? Get our free guide instead"
3. **Question:** "Is something holding you back?" + FAQ
4. **Reminder:** "Your trial is waiting" + benefits summary

### Exit Popup Best Practices

- Delay: Only after 5+ seconds on page
- Frequency: Once per session
- Mobile: Scroll-triggered (no true exit intent)
- Value: Must offer something worthwhile
- Easy close: Clear X button, no dark patterns

---

## Trust Indicators

### Placement Near CTAs

```
┌─────────────────────────────────┐
│       Start Free Trial          │
└─────────────────────────────────┘
   🔒 256-bit SSL  |  No spam ever

  ⭐⭐⭐⭐⭐ 4.9/5 on G2 (200+ reviews)
```

### Trust Badge Types

| Badge | Use Case |
|-------|----------|
| SSL/Security | Any form with personal data |
| Payment icons | Checkout pages |
| G2/Capterra | B2B SaaS |
| Money-back | Paid products |
| "As seen in" | Any (if genuine) |
| SOC2/GDPR | Enterprise, security-conscious |
