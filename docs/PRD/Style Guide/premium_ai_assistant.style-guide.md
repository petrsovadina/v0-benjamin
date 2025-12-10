# MediAI Premium Glassmorphism Style Guide

**Style Overview**:
A sophisticated glassmorphism design with crystalline transparency effects on a pure white background, featuring deep charcoal primary colors with silver accents and cool-toned slate blue and soft cyan highlights for a premium AI-powered medical platform aesthetic.

## Colors
### Primary Colors
  - **primary-base**: `text-[#2C3541]` or `bg-[#2C3541]` - Deep charcoal for primary elements
  - **primary-lighter**: `text-[#495766]` or `bg-[#495766]` - Lighter charcoal for secondary emphasis
  - **primary-darker**: `text-[#1A1F28]` or `bg-[#1A1F28]` - Darkest charcoal for high contrast

### Background Colors

#### Structural Backgrounds
Pure white background for maximum clarity and sophisticated minimalism.

Choose based on layout type:

**For Vertical Layout** (Top Header + Optional Side Panels):
- **bg-nav-primary**: `bg-white` - Top header
- **bg-nav-secondary**: `bg-white` - Inner Left sidebar (if present)
- **bg-page**: `bg-white` - Page background (bg of Main Content area)

**For Horizontal Layout** (Side Navigation + Optional Top Bar):
- **bg-nav-primary**: `bg-white` - Left main sidebar
- **bg-nav-secondary**: `bg-white` - Inner Top header (if present)
- **bg-page**: `bg-white` - Page background (bg of Main Content area)

#### Container Backgrounds
Glassmorphism containers with crystalline transparency. For main content area.

- **bg-container-primary**: `bg-white/0` - Most content uses colorless, transparent containers; glassmorphism relies on generous whitespace for refined minimalism
- **bg-container-secondary**: `glass-subtle` - For cards, tags, and standard buttons
```css
.glass-subtle {
  background: rgba(255, 255, 255, 0.25);
  box-shadow: inset 6px 0px 10px -4px rgba(255, 255, 255, 0.45),
              inset -6px 0px 10px -4px rgba(255, 255, 255, 0.45),
              0 2px 8px rgba(44, 53, 65, 0.06);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}
```
- **bg-container-tertiary**: `glass-strong` - For emphasized cards, active states, and primary buttons
```css
.glass-strong {
  background: rgba(255, 255, 255, 0.40);
  box-shadow: inset 12px 0px 24px -12px rgba(255, 255, 255, 0.50),
              inset -12px 0px 24px -12px rgba(255, 255, 255, 0.50),
              inset -2px 0px 3px -1px rgba(255, 255, 255, 0.60),
              inset 2px 0px 3px -1px rgba(255, 255, 255, 0.60),
              0 4px 12px rgba(44, 53, 65, 0.08);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.4);
}
```
- **bg-container-inset**: `glass-inset-subtle` - For input fields
```css
.glass-inset-subtle {
  background: rgba(0, 0, 0, 0.015);
  box-shadow: inset 4px 4px 8px -4px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(44, 53, 65, 0.08);
}
```
- **bg-container-inset-strong**: `glass-inset-strong` - For checkbox backgrounds, slider tracks
```css
.glass-inset-strong {
  background: rgba(0, 0, 0, 0.025);
  box-shadow: inset 4px 4px 10px -4px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(44, 53, 65, 0.12);
}
```

### Text Colors
- **color-text-primary**: `text-[#2C3541]` - Primary deep charcoal for headings and key content
- **color-text-secondary**: `text-[#495766]` - Secondary text for supporting information
- **color-text-tertiary**: `text-[#6B7785]` - Tertiary text for metadata and labels
- **color-text-quaternary**: `text-[#98A2AE]` - Quaternary text for subtle hints
- **color-text-on-dark-primary**: `text-white/95` - Text on dark backgrounds and primary-base surfaces
- **color-text-on-dark-secondary**: `text-white/75` - Secondary text on dark backgrounds
- **color-text-link**: `text-[#5B7A9F]` - Links and clickable text

### Functional Colors
Use sparingly to maintain sophisticated aesthetic. Used for status indicators, alerts, and functional feedback.
  - **color-success-default**: `#7ECBAE` - Success states, confirmation messages
  - **color-success-light**: `#C5E8DC` - Success tag/label backgrounds
  - **color-error-default**: `#D98D8D` - Error states, critical alerts
  - **color-error-light**: `#F5D4D4` - Error tag/label backgrounds
  - **color-warning-default**: `#E8C591` - Warning states, caution messages
  - **color-warning-light**: `#F7E8D0` - Warning tag/label backgrounds
  - **color-function-default**: `#5B7A9F` - Functional elements, progress indicators
  - **color-function-light**: `#D0DFEF` - Functional tag/label backgrounds

### Accent Colors
Cool-toned adjacent colors for sophisticated balance and premium feel.
  - **accent-slate-blue**: `text-[#6E8CAD]` or `bg-[#6E8CAD]` - Primary accent for highlights
  - **accent-soft-cyan**: `text-[#7BAEC4]` or `bg-[#7BAEC4]` - Secondary accent for categorization
  - **accent-silver**: `text-[#B8C4D0]` or `bg-[#B8C4D0]` - Subtle metallic accent

### Data Visualization Charts
For data visualization charts only. Cool-toned palette harmonizing with primary and accent colors.
  - Standard data colors: `#E8EBEF`, `#C8D1DB`, `#98A2AE`, `#6B7785`, `#495766`, `#2C3541`
  - Important data can use small amounts of: `#6E8CAD`, `#5B7A9F`, `#7BAEC4`, `#7ECBAE`

## Typography
- **Font Stack**:
  - **font-family-base**: `-apple-system, BlinkMacSystemFont, "Segoe UI"` — For regular UI copy

- **Font Size & Weight**:
  - **Caption**: `text-sm font-normal`
  - **Body**: `text-base font-normal`
  - **Body Emphasized**: `text-base font-semibold`
  - **Card Title / Subtitle**: `text-lg font-semibold`
  - **Page Title**: `text-2xl font-semibold`
  - **Headline**: `text-4xl font-semibold`

- **Line Height**: 1.5

## Border Radius
  - **Small**: 12px — Elements inside cards (e.g., icons, small tags)
  - **Medium**: 16px — Buttons, inputs, standard cards
  - **Large**: 24px — Large cards, modal dialogs
  - **Full**: full — Avatars, pill-shaped toggles

## Layout & Spacing
  - **Tight**: 8px - For closely related small internal elements (icon-text pairs in buttons)
  - **Compact**: 12px - For small gaps between compact UI elements (tag groups)
  - **Standard**: 20px - For gaps between medium containers (list items, form fields)
  - **Relaxed**: 32px - For gaps between large containers and card groups
  - **Section**: 48px - For major section divisions and page structure

## Create Boundaries (contrast of surface color, borders, shadows)
Glassmorphism style creates boundaries through translucent glass-like surfaces with blur effects, subtle white inner shadows, thin light borders, and soft cool-toned outer shadows.

### Borders
  - **Glass Container Borders**: 1px solid with white transparency for crystalline edges
    - **Subtle Glass**: `border border-white/30` - Standard glass containers
    - **Strong Glass**: `border border-white/40` - Emphasized glass containers
    - **Inset Containers**: `border border-[#2C3541]/8` or `border-[#2C3541]/12` - Input fields and inset elements

### Dividers
  - Use subtle dividers when needed: `border-t border-[#2C3541]/6` or `border-b border-[#2C3541]/6`

### Shadows & Effects
  - **Glassmorphism Effects**: Achieved through combination of backdrop blur, inner white shadows, and subtle outer shadows (see Container Backgrounds section)
  - **Additional Floating Shadow**: `shadow-[0_8px_24px_rgba(44,53,65,0.10)]` - For modals and prominent floating elements
  - **Hover Enhancement**: Add `brightness-105` on hover to glass elements for subtle luminosity

## Visual Emphasis for Containers
When containers (tags, cards, list items, rows) need visual emphasis to indicate priority, status, or category, use the following techniques:
| Technique | Implementation Notes | Best For | Avoid |
|-----------|---------------------|----------|-------|
| Glass Intensity | Increase background opacity and blur strength (bg-white/25 → bg-white/40) | Primary technique for glassmorphism style | Overuse - maintain transparency hierarchy |
| Border Highlight | Increase border opacity or add accent color tint (border-white/30 → border-[#6E8CAD]/40) | Active/selected states | Solid heavy borders that break glass aesthetic |
| Glow Effect | Add subtle luminous outer shadow with accent color | Premium hover states, AI feature indicators | Bright neon effects |
| Status Tag/Label | Add small colored glass tag with functional colors inside container | Status indicators, categorization | - |
| Accent Gradient Edge | Subtle gradient border or left accent bar using accent colors | Priority items in lists | - |

## Assets
### Image
  - For normal `<img>`: `object-cover`
  - For `<img>` with:
    - Slight overlay: `object-cover brightness-95`
    - Heavy overlay: `object-cover brightness-75`

### Icon
- Use Lucide icons from Iconify for clean, professional appearance.
- To ensure an aesthetic layout, each icon should be centered in a square container, typically without a background, matching the icon's size.
- Use Tailwind font size to control icon size
- Example:
  ```html
  <div class="flex items-center justify-center bg-transparent w-5 h-5">
  <iconify-icon icon="lucide:activity" class="text-base"></iconify-icon>
  </div>
  ```

### Third-Party Brand Logos:
   - Use Brand Icons from Iconify.
   - Logo Example:
     Monochrome Logo: `<iconify-icon icon="simple-icons:openai"></iconify-icon>`
     Colored Logo: `<iconify-icon icon="logos:google-icon"></iconify-icon>`

### User's Own Logo:
- To protect copyright, do **NOT** use real product logos as a logo for a new product, individual user, or other company products.
- **Icon-based**:
  - **Graphic**: Use a simple, relevant icon (e.g., a `stethoscope` icon for medical apps, a `mic` icon for transcription features).

## Page Layout - Web (*EXTREMELY* important)
### Determine Layout Type
- Choose between Vertical or Horizontal layout based on whether the primary navigation is a full-width top header or a full-height sidebar (left/right).
- User requirements typically indicate the layout preference. If unclear, consider:
  - Marketing/content sites typically use Vertical Layout.
  - Functional/dashboard sites can use either, depending on visual style. Sidebars accommodate more complex navigation than top bars. For complex navigation needs with a preference for minimal chrome (Vertical Layout adds an extra fixed header), choose Horizontal Layout (omits the fixed top header).
- Vertical Layout Diagram:
┌──────────────────────────────────────────────────────┐
│  Header (Primary Nav)                                │
├──────────┬──────────────────────────────┬────────────┤
│Left      │ Sub-header (Tertiary Nav)    │ Right      │
│Sidebar   │ (optional)                   │ Sidebar    │
│(Secondary├──────────────────────────────┤ (Utility   │
│Nav)      │ Main Content                 │ Panel)     │
│(optional)│                              │ (optional) │
│          │                              │            │
└──────────┴──────────────────────────────┴────────────┘
- Horizontal Layout Diagram:
┌──────────┬──────────────────────────────┬───────────┐
│          │ Header (Secondary Nav)       │           │
│ Left     │ (optional)                   │ Right     │
│ Sidebar  ├──────────────────────────────┤ Sidebar   │
│ (Primary │ Main Content                 │ (Utility  │
│ Nav)     │                              │ Panel)    │
│          │                              │ (optional)│
│          │                              │           │
└──────────┴──────────────────────────────┴───────────┘
### Detailed Layout Code
**Vertical Layout**
```html
<!-- Body: Adjust width (w-[1440px]) based on target screen size -->
<body class="w-[1440px] min-h-[700px] font-[-apple-system,BlinkMacSystemFont,'Segoe UI'] leading-[1.5]">

  <!-- Header (Primary Nav): Fixed height -->
  <header class="w-full">
    <!-- Header content -->
  </header>

  <!-- Content Container: Must include 'flex' class -->
  <div class="w-full flex min-h-[700px]">
    <!-- Left Sidebar (Secondary Nav) (Optional): Remove if not needed. If Left Sidebar exists, use its ml to control left page margin -->
    <aside class="flex-shrink-0 min-w-fit">

    </aside>

    <!-- Main Content Area:
     Use Main Content Area's horizontal padding (px) to control distance from main content to sidebars or page edges.
     For pages without sidebars (like Marketing Pages, simple content pages such as help centers, privacy policies) use larger values (px-30 to px-80), for pages with sidebars (Functional/Dashboard Pages, complex content pages with multi-level navigation like knowledge base articles) use moderate values (px-8 to px-16) -->
    <main class="flex-1 overflow-x-hidden flex flex-col">
    <!--  Main Content -->

    </main>

    <!-- Right Sidebar (Utility Panel) (Optional): Remove if not needed. If Right Sidebar exists, use its mr to control right page margin -->
    <aside class="flex-shrink-0 min-w-fit">
    </aside>

  </div>
</body>
```

**Horizontal Layout**

```html
<!-- Body: Adjust width (w-[1440px]) based on target screen size. Must include 'flex' class -->
<body class="w-[1440px] min-h-[700px] flex font-[-apple-system,BlinkMacSystemFont,'Segoe UI'] leading-[1.5]">

<!-- Left Sidebar (Primary Nav): Use its ml to control left page margin -->
  <aside class="flex-shrink-0 min-w-fit">
  </aside>

  <!-- Content Container-->
  <div class="flex-1 overflow-x-hidden flex flex-col min-h-[700px]">

    <!-- Header (Secondary Nav) (Optional): Remove if not needed. If Header exists, use its mx to control distance to left/right sidebars or page margins -->
    <header class="w-full">
    </header>

    <!-- Main Content Area: Use Main Content Area's pl to control distance from main content to left sidebar. Use pr to control distance to right sidebar/right page edge -->
    <main class="w-full">
    </main>


  </div>

  <!-- Right Sidebar (Utility Panel) (Optional): Remove if not needed. If Right Sidebar exists, use its mr to control right page margin -->
  <aside class="flex-shrink-0 min-w-fit">
  </aside>

</body>
```

## Tailwind Component Examples (Key attributes)
**Important Note**: Use utility classes directly. Do NOT create custom CSS classes or add styles in <style> tags for the following components

### Basic

- **Button**:
  - Example 1 (Glass button with text):
    - button: `flex items-center gap-2 glass-subtle hover:glass-strong transition-all duration-200 px-6 py-3 rounded-2xl`
      - icon (optional)
      - span(button copy): `whitespace-nowrap`
  - Example 2 (Primary glass button):
    - button: `flex items-center gap-2 glass-strong hover:brightness-105 transition-all duration-200 px-6 py-3 rounded-2xl`
      - icon (optional)
      - span(button copy): `whitespace-nowrap`
  - Example 3 (Icon-only button):
    - button: `flex items-center justify-center w-10 h-10 glass-subtle hover:glass-strong transition-all duration-200 rounded-xl`
      - icon

- **Tag Group (Filter Tags)**
  - container(scrollable): `flex gap-3 overflow-x-auto [&::-webkit-scrollbar]:hidden`
    - label (Tag item):
      - input: `type="radio" name="tag1" class="sr-only peer" checked`
      - div: `glass-subtle peer-checked:glass-strong hover:brightness-105 transition-all duration-200 whitespace-nowrap px-4 py-2 rounded-full`

### Data Entry
- **Progress bars/Slider**: `h-2 rounded-full`
- **Checkbox**
  - label: `flex items-center gap-3`
    - input: `type="checkbox" class="sr-only peer"`
    - div: `glass-inset-subtle rounded-lg w-5 h-5 flex items-center justify-center peer-checked:glass-strong text-transparent peer-checked:text-[#6E8CAD] transition-all duration-200`
      - svg(Checkmark): `stroke="currentColor" stroke-width="3"`
    - span(text)
- **Radio button**
  - label: `flex items-center gap-3`
    - input: `type="radio" name="option1" class="sr-only peer"`
    - div: `glass-inset-subtle rounded-full w-5 h-5 flex items-center justify-center peer-checked:glass-strong text-transparent peer-checked:text-[#6E8CAD] transition-all duration-200`
      - svg(dot indicator): `fill="currentColor"`
    - span(text)
- **Switch/Toggle**
  - label: `flex items-center gap-3`
    - div: `relative`
      - input: `type="checkbox" class="sr-only peer"`
      - div(Toggle track): `w-14 h-7 glass-inset-subtle peer-checked:glass-strong rounded-full transition-all duration-200`
      - div(Toggle thumb): `absolute top-1 left-1 w-5 h-5 bg-white rounded-full shadow-[0_2px_4px_rgba(44,53,65,0.2)] peer-checked:translate-x-7 peer-checked:bg-[#6E8CAD] transition-all duration-200`
    - span(text)

- **Select/Dropdown**
  - Select container: `flex items-center gap-2 glass-inset-subtle px-4 py-2 rounded-xl`
    - text
    - Dropdown icon(square container): `flex items-center justify-center bg-transparent w-5 h-5`
      - icon: `lucide:chevron-down`

### Container
- **Navigation Menu - horizontal**
    - Nav Container: `flex items-center justify-between w-full glass-subtle px-8 py-4`
    - Left Section: `flex items-center gap-10`
      - Menu Item: `flex items-center gap-3 hover:brightness-105 transition-all duration-200`
    - Right Section: `flex items-center gap-6`
      - Menu Item: `flex items-center gap-3 hover:brightness-105 transition-all duration-200`
      - Notification (if applicable): `relative flex items-center justify-center w-10 h-10 glass-subtle rounded-xl hover:glass-strong transition-all duration-200`
        - notification-icon: `w-5 h-5`
        - badge (if has unread): `absolute -top-1 -right-1 w-5 h-5 rounded-full flex items-center justify-center bg-[#D98D8D] text-white text-xs font-semibold`
          - badge-count
      - Avatar(if applicable): `flex items-center gap-3`
        - avatar-image: `w-10 h-10 rounded-full border-2 border-white/30`
        - dropdown-icon (if applicable): `w-5 h-5`

- **Card**
    - Example 1 (Vertical glass card with image and text):
        - Card: `glass-subtle hover:glass-strong transition-all duration-200 rounded-2xl flex flex-col p-6 gap-4`
        - Image: `rounded-xl w-full`
        - Text area: `flex flex-col gap-3`
          - card-title: `text-lg font-semibold`
          - card-subtitle: `text-sm font-normal`
    - Example 2 (Horizontal glass card with image and text):
        - Card: `glass-subtle hover:glass-strong transition-all duration-200 rounded-2xl flex gap-6 p-6`
        - Image: `rounded-xl h-full`
        - Text area: `flex flex-col gap-4`
          - card-title: `text-lg font-semibold`
          - card-subtitle: `text-sm font-normal`
    - Example 3 (Image-focused card with minimal glass):
        - Card: `flex flex-col gap-4`
        - Image: `rounded-2xl w-full glass-subtle`
        - Text area: `flex flex-col gap-3`
          - card-title: `text-lg font-semibold`
          - card-subtitle: `text-sm font-normal`
    - Example 4 (Emphasized glass card with accent):
        - Card: `glass-strong rounded-2xl flex flex-col p-6 gap-4 border-l-4 border-[#6E8CAD]`

## Additional Notes
- **Glassmorphism Hierarchy**: Maintain transparency hierarchy - most content uses bg-white/0 (transparent), secondary elements use glass-subtle, only emphasized elements use glass-strong
- **White Space**: Generous spacing is essential for glassmorphism's refined aesthetic - don't overcrowd containers
- **Blur Consistency**: All glass effects include backdrop-filter blur for authentic glass appearance
- **Hover States**: Enhance glass elements on hover with brightness-105 for subtle luminosity increase
- **Medical Context**: While maintaining premium AI sophistication, ensure text readability and accessibility for medical professionals working in various lighting conditions
- **Cool-Toned Palette**: Slate blue and soft cyan accents provide sophisticated balance without overwhelming the crystalline transparency
- **Border Treatment**: Thin white borders (border-white/30 or border-white/40) create crisp crystalline edges on glass surfaces

<colors_extraction>
#2C3541
#495766
#1A1F28
#FFFFFF
#FFFFFF40
#FFFFFF66
#FFFFFF4D
#FFFFFF73
#FFFFFF80
#FFFFFF99
#00000004
#00000007
#0000000F
#0000001A
#2C354114
#2C35411F
#6B7785
#98A2AE
#5B7A9F
#7ECBAE
#C5E8DC
#D98D8D
#F5D4D4
#E8C591
#F7E8D0
#D0DFEF
#6E8CAD
#7BAEC4
#B8C4D0
#E8EBEF
#C8D1DB
rgba(255, 255, 255, 0.25)
rgba(255, 255, 255, 0.40)
rgba(0, 0, 0, 0.015)
rgba(0, 0, 0, 0.025)
#6E8CAD66
</colors_extraction>
