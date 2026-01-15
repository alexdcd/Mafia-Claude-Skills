# Sections Catalog

Complete reference of all landing page sections with purpose, structure, and examples.

---

## 1. Announcement Bar

**Purpose:** Create urgency, highlight offers without cluttering hero

**Position:** Top of page (above navigation)

**Structure:**
```html
<div class="announcement-bar">
  <span class="emoji">🔥</span>
  <span class="message">Limited time: 50% off all plans</span>
  <a href="#pricing" class="cta">Claim offer →</a>
</div>
```

**Best practices:**
- One message only
- Dismissible (X button)
- Link to relevant section
- High contrast background

**Copy examples:**
- "🎉 Just launched: AI Writing Assistant — Try it free"
- "⏰ Price increases Friday — Lock in current rate"
- "🚀 10,000 teams trust us — Join them today"

---

## 2. Hero Section

**Purpose:** Capture attention, communicate value, drive primary action

**Position:** First visible section (above fold)

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [H1: Outcome-focused headline]                     │
│  [H2: How you deliver that outcome]                 │
│                                                     │
│  [CTA Button]        [Product Visual/Demo]          │
│  [Micro-copy]                                       │
│                                                     │
│  [Social proof: logos or "Trusted by X users"]      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Copy example:**
```
H1: "Create Invoices in 30 Seconds, Not 30 Minutes"
H2: "The simplest invoicing tool for freelancers. 
     No accounting degree required."

CTA: "Start Free Trial"
Micro: "No credit card needed"

Social: "Trusted by 50,000+ freelancers"
```

---

## 3. Logo Bar (Social Proof Bar)

**Purpose:** Instant credibility, "halo effect" from recognized brands

**Position:** Immediately after hero or within hero

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  "Trusted by teams at"                              │
│  [Logo] [Logo] [Logo] [Logo] [Logo] [Logo]          │
└─────────────────────────────────────────────────────┘
```

**Best practices:**
- 4-6 logos maximum
- Grayscale (doesn't compete with CTAs)
- Include recognizable names
- Add context text ("Used by...", "Featured in...")

---

## 4. Problem Agitation

**Purpose:** Create emotional resonance, make visitor feel understood

**Position:** After hero, before solution

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  "Sound familiar?"                                  │
│                                                     │
│  😩 Pain point 1 with emotional consequence         │
│  😤 Pain point 2 with emotional consequence         │
│  😫 Pain point 3 with emotional consequence         │
│                                                     │
│  "There's a better way."                            │
└─────────────────────────────────────────────────────┘
```

**Copy example:**
```
"Manual invoicing is killing your productivity"

❌ Spending hours in spreadsheets instead of doing real work
❌ Chasing payments because you forgot to follow up
❌ Looking unprofessional with inconsistent invoice formats

"What if invoicing took 30 seconds instead of 30 minutes?"
```

---

## 5. Solution / Benefits

**Purpose:** Position product as the answer to stated problems

**Position:** Immediately after problem section

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  "Here's how [Product] fixes this"                  │
│                                                     │
│  ✅ Benefit 1 (addresses pain point 1)              │
│  ✅ Benefit 2 (addresses pain point 2)              │
│  ✅ Benefit 3 (addresses pain point 3)              │
│                                                     │
│  [Product screenshot showing the solution]          │
└─────────────────────────────────────────────────────┘
```

---

## 6. How It Works

**Purpose:** Reduce uncertainty, show simplicity of adoption

**Position:** After solution, before features

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  "Get started in 3 simple steps"                    │
│                                                     │
│  [1] ──────── [2] ──────── [3]                      │
│  Step 1       Step 2       Step 3                   │
│  Icon         Icon         Icon                     │
│  Description  Description  Description              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Best practices:**
- Maximum 3-5 steps
- Use icons/illustrations
- Short descriptions (1-2 sentences)
- Optional: mini-demo video

**Copy example:**
```
Step 1: "Sign up in 60 seconds"
Step 2: "Create your first invoice"
Step 3: "Get paid faster"
```

---

## 7. Features (Bento Grid)

**Purpose:** Showcase capabilities, allow non-linear exploration

**Position:** Middle of page

**Structure:**
```
┌─────────────────┬─────────────────┬─────────────────┐
│     Feature 1   │     Feature 2   │     Feature 3   │
│     (large)     │    (medium)     │    (medium)     │
│                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┤
│     Feature 4   │     Feature 5   │     Feature 6   │
│    (medium)     │    (medium)     │    (medium)     │
└─────────────────┴─────────────────┴─────────────────┘
```

**Card structure:**
```
[Icon]
[Feature title]
[1-2 sentence benefit]
[Optional: mini-screenshot]
```

**Best practices:**
- Highlight 1-2 key features with larger cards
- Benefits > Features in copy
- Include visuals where possible
- Link to feature pages for details

---

## 8. Testimonials / Wall of Love

**Purpose:** Build trust through social proof, address objections

**Position:** After features, before pricing

**Formats:**

**A. Video Testimonials (Best)**
```
┌─────────────────────────────────────────────────────┐
│  [Video]  [Video]  [Video]                          │
│  Name,    Name,    Name,                            │
│  Title    Title    Title                            │
└─────────────────────────────────────────────────────┘
```

**B. Quote Cards**
```
┌─────────────────────────────────────────────────────┐
│  "Quote with specific result or emotion"            │
│                                                     │
│  [Photo] Name Surname                               │
│          Title at Company                           │
└─────────────────────────────────────────────────────┘
```

**C. Screenshot Wall**
```
[Twitter screenshot] [LinkedIn post] [G2 review]
[Email screenshot] [Slack message] [Tweet]
```

**Best practices:**
- Include specific results/metrics
- Full names and real photos
- Company/role for B2B
- Mix of formats (video + text)
- Address different objections

---

## 9. Comparison Table (Us vs Them)

**Purpose:** Position against alternatives, prevent comparison shopping

**Position:** After testimonials, before pricing

**Structure:**
```
┌─────────────────┬─────────────┬─────────────┬─────────────┐
│    Feature      │   Us ✨     │ Competitor A│ Competitor B│
├─────────────────┼─────────────┼─────────────┼─────────────┤
│ Feature 1       │     ✅      │     ✅      │     ❌      │
│ Feature 2       │     ✅      │     ❌      │     ✅      │
│ Feature 3       │     ✅      │     ❌      │     ❌      │
│ Price           │    $29      │    $99      │    $49      │
└─────────────────┴─────────────┴─────────────┴─────────────┘
```

**Best practices:**
- Only include features where you win
- Be factually accurate
- Don't badmouth competitors
- Highlight your differentiator

---

## 10. Pricing Section

**Purpose:** Convert intent to action, filter qualified leads

**Position:** Late in page (after trust is built)

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  "Simple, transparent pricing"                      │
│                                                     │
│  [Toggle: Monthly / Annual (save 20%)]              │
│                                                     │
│  ┌─────────┐  ┌─────────────┐  ┌─────────┐        │
│  │ Starter │  │   Pro ⭐    │  │Enterprise│        │
│  │  $9/mo  │  │  $29/mo     │  │  Custom  │        │
│  │         │  │ Most Popular│  │          │        │
│  │ Feature │  │ Feature     │  │ Feature  │        │
│  │ Feature │  │ Feature     │  │ Feature  │        │
│  │ Feature │  │ Feature     │  │ Feature  │        │
│  │         │  │ Feature     │  │ Feature  │        │
│  │  [CTA]  │  │   [CTA]     │  │  [CTA]   │        │
│  └─────────┘  └─────────────┘  └─────────┘        │
│                                                     │
│  "30-day money-back guarantee"                      │
└─────────────────────────────────────────────────────┘
```

---

## 11. FAQ Section

**Purpose:** Address objections, reduce support load

**Position:** After pricing, before final CTA

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  "Frequently Asked Questions"                       │
│                                                     │
│  ▶ Question 1 (objection)                           │
│    Answer that addresses concern                    │
│                                                     │
│  ▶ Question 2 (logistics)                           │
│    Answer with specifics                            │
│                                                     │
│  ▶ Question 3 (comparison)                          │
│    Answer positioning your product                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Essential questions to include:**
- "Is there a free trial?"
- "Can I cancel anytime?"
- "How is this different from X?"
- "What if it doesn't work for me?"
- "How long does setup take?"
- "Do you offer support?"

---

## 12. Founder's Note

**Purpose:** Humanize brand, build emotional connection

**Position:** Near end of page (after pricing/FAQ)

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  [Photo of founder]                                 │
│                                                     │
│  "A note from our founder"                          │
│                                                     │
│  Personal story about why you built this.           │
│  What problem you faced. How it felt.               │
│  Why you're passionate about solving it.            │
│                                                     │
│  [Signature]                                        │
│  Name, Founder                                      │
└─────────────────────────────────────────────────────┘
```

**Best for:** Micro-SaaS, indie products, creator economy, coaching

---

## 13. Guarantee / Risk Reversal

**Purpose:** Remove final barrier to conversion

**Position:** Near final CTA

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  🛡️ Our 30-Day Money-Back Guarantee                 │
│                                                     │
│  Try [Product] risk-free. If you're not completely  │
│  satisfied within 30 days, email us for a full      │
│  refund. No questions asked.                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 14. Final CTA Block

**Purpose:** Last conversion opportunity with reinforced value

**Position:** Bottom of page (before footer)

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  "Ready to [outcome]?"                              │
│                                                     │
│  Quick reminder of main benefit.                    │
│  Join X customers who already have.                 │
│                                                     │
│            [Primary CTA Button]                     │
│            No credit card required                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 15. Footer (Minimal)

**Purpose:** Legal requirements, trust, secondary navigation

**Structure:**
```
┌─────────────────────────────────────────────────────┐
│  [Logo]                                             │
│                                                     │
│  © 2026 Company Name                                │
│  Privacy Policy | Terms of Service                  │
│                                                     │
│  [Social Icons]                                     │
└─────────────────────────────────────────────────────┘
```

**Best practices:**
- No navigation that competes with CTA
- Keep minimal
- Include required legal links
- Optional: Contact email

---

## Section Order Summary

**SaaS/Tool (12-14 sections):**
1. Announcement Bar
2. Hero
3. Logo Bar
4. Problem
5. Solution
6. How It Works
7. Features (Bento)
8. Testimonials
9. Comparison
10. Pricing
11. FAQ
12. Founder's Note
13. Final CTA
14. Footer

**Course/Coaching (10-12 sections):**
1. Hero (with video)
2. Pain Points
3. Your Story
4. Transformation
5. Curriculum
6. Bonuses
7. Student Results
8. Pricing
9. FAQ
10. Urgency
11. Final CTA
12. Footer

**Lead Magnet (6-8 sections):**
1. Hero + Form
2. What's Inside
3. Who It's For
4. Author Credibility
5. Social Proof
6. Final CTA
