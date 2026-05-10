# AI Resume Optimizer - $10K Premium Design System

## Design Philosophy
Premium SaaS aesthetic with sophisticated animations, elevated shadows, glass morphism elements, and micro-interactions that communicate quality and trust.

## Color Palette

### Primary - Deep Indigo
- **Primary**: `#6366f1` (Indigo-500) - Main brand color
- **Primary Dark**: `#4f46e5` (Indigo-600) - Hover states
- **Primary Light**: `#818cf8` (Indigo-400) - Accents
- **Primary Glow**: `rgba(99, 102, 241, 0.15)` - Backgrounds

### Background Layers
- **Background**: `#fafbfc` - Base surface
- **Surface**: `#ffffff` - Cards, panels
- **Surface Elevated**: `#ffffff` with shadow-xl - Floating elements
- **Border**: `#e5e7eb` - Subtle borders
- **Border Hover**: `#d1d5db` - Hover borders

### Text Hierarchy
- **Text Primary**: `#111827` - Headlines
- **Text Secondary**: `#4b5563` - Body
- **Text Muted**: `#9ca3af` - Captions
- **Text Inverse**: `#ffffff` - On dark surfaces

### Accent Colors
- **Success**: `#10b981` (Emerald-500)
- **Warning**: `#f59e0b` (Amber-500)
- **Danger**: `#ef4444` (Red-500)
- **Info**: `#3b82f6` (Blue-500)

### Gradients
- **Hero Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Card Gradient**: `linear-gradient(180deg, #f9fafb 0%, #ffffff 100%)`
- **Glow Gradient**: `radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%)`

## Typography

### Font Stack
- **Headings**: `Inter` (Google Fonts) - Clean, professional
- **Body**: `Inter` - Consistent reading experience
- **Mono**: `JetBrains Mono` - Code/technical content

### Scale
- **Display**: 48px / 700 weight / -0.02em tracking
- **H1**: 36px / 600 weight
- **H2**: 30px / 600 weight
- **H3**: 24px / 600 weight
- **H4**: 20px / 600 weight
- **Body Large**: 18px / 400 weight / 1.7 line-height
- **Body**: 16px / 400 weight / 1.6 line-height
- **Small**: 14px / 500 weight
- **Caption**: 12px / 500 weight / uppercase / 0.05em tracking

## Spacing System
- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px
- **3xl**: 64px
- **4xl**: 96px

## Border Radius
- **sm**: 8px
- **md**: 12px
- **lg**: 16px
- **xl**: 24px
- **full**: 9999px

## Shadows (Premium)

```css
/* Subtle card shadow */
shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

/* Standard card */
shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);

/* Elevated card */
shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);

/* Floating elements */
shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);

/* Premium glow */
shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);

/* Inner glow for focus states */
shadow-inner-glow: inset 0 2px 4px rgba(99, 102, 241, 0.1);
```

## Animation Tokens

### Durations
- **instant**: 50ms
- **fast**: 150ms
- **normal**: 250ms
- **slow**: 400ms
- **slower**: 600ms

### Easings
- **ease-out**: cubic-bezier(0.16, 1, 0.3, 1) - Exits, reveals
- **ease-in-out**: cubic-bezier(0.65, 0, 0.35, 1) - Transitions
- **spring**: cubic-bezier(0.34, 1.56, 0.64, 1) - Bouncy interactions

## Component Patterns

### Premium Button
- Background: Primary gradient or solid
- Border-radius: lg (16px)
- Padding: px-6 py-3
- Shadow on hover with transform
- Active: scale-95
- Disabled: opacity-50 cursor-not-allowed

### Premium Card
- Background: white
- Border: 1px solid gray-200
- Border-radius: xl (24px)
- Shadow: shadow-lg
- Padding: p-8
- Hover: shadow-xl + translate-y-[-2px]

### Glass Card
- Background: rgba(255, 255, 255, 0.8)
- Backdrop-filter: blur(12px)
- Border: 1px solid rgba(255, 255, 255, 0.3)
- Border-radius: xl

### Stat Card
- Icon in gradient container
- Large number with animation
- Subtle background pattern
- Hover lift effect

### Navigation
- Sticky header with blur backdrop
- Logo with hover glow
- Nav items with underline animation
- CTA button with gradient

### Forms
- Floating labels
- Focus: ring-2 ring-primary/50
- Error states with shake animation
- Success with checkmark animation
- Loading spinner in input

### Tabs
- Pill style with smooth indicator
- Animated underline follow
- Hover: background-50

## Anti-Patterns
- No flat cards without shadow
- No gray-on-gray text
- No instant state changes (always animate)
- No emojis as icons (use Lucide/Phosphor)
- No horizontal scroll
- No fixed pixel widths