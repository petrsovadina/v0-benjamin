# MediAI Professional Healthcare Style Guide

**Style Overview**:
A clean minimalist light theme built on calm navy blue with off-white backgrounds, emphasizing medical-grade professionalism through subtle surface color differences and generous whitespace for comfortable extended use with sensitive health data.
Avoid gradients, borders, shadows, and any colors not defined in this style.

## Colors
### Primary Colors
  - **primary-base**: `text-[#2C5282]` or `bg-[#2C5282]`
  - **primary-lighter**: `bg-[#4A6FA5]`
  - **primary-darker**: `text-[#1A365D]` or `bg-[#1A365D]`

### Background Colors

#### Structural Backgrounds

Choose based on layout type:

**For Vertical Layout** (Top Header + Optional Side Panels):
- **bg-nav-primary**: `bg-[hsla(211, 36%, 91%, 1)]` - Top header
- **bg-nav-secondary**: `bg-[hsla(211, 38%, 94%, 1)]` - Inner Left sidebar (if present)
- **bg-page**: `bg-[hsla(211, 30%, 97%, 1)]` - Page background (bg of Main Content area)

**For Horizontal Layout** (Side Navigation + Optional Top Bar):
- **bg-nav-primary**: `bg-[hsla(211, 36%, 91%, 1)]` - Left main sidebar
- **bg-nav-secondary**: `bg-[hsla(211, 38%, 94%, 1)]` - Inner Top header (if present)
- **bg-page**: `bg-[hsla(211, 30%, 97%, 1)]` - Page background (bg of Main Content area)

#### Container Backgrounds
For main content area. Adjust values when used on navigation backgrounds to ensure sufficient contrast.
- **bg-container-primary**: `bg-white`
- **bg-container-secondary**: `bg-[hsla(211, 40%, 98%, 1)]`
- **bg-container-inset**: `bg-[hsla(211, 45%, 96%, 1)]`
- **bg-container-inset-strong**: `bg-[hsla(211, 50%, 93%, 1)]`

### Text Colors
- **color-text-primary**: `text-[hsla(211, 30%, 20%, 1)]`
- **color-text-secondary**: `text-[hsla(211, 20%, 40%, 1)]`
- **color-text-tertiary**: `text-[hsla(211, 15%, 55%, 1)]`
- **color-text-quaternary**: `text-[hsla(211, 10%, 70%, 1)]`
- **color-text-on-dark-primary**: `text-white/90` - Text on dark backgrounds and primary-base color surfaces
- **color-text-on-dark-secondary**: `text-white/70` - Text on dark backgrounds and primary-base color surfaces
- **color-text-link**: `text-[#2C5282]` - Links, text-only buttons without backgrounds, and clickable text in tables

### Functional Colors
Use **sparingly** to maintain a minimalist and neutral overall style. Used for the surfaces of text-only cards, simple cards, buttons, and tags.
  - **color-success-default**: #C6E5D6 - alert banner bg
  - **color-success-light**: #E8F5ED - tag/label bg
  - **color-error-default**: #E8C5C2 - alert banner bg
  - **color-error-light**: #F7E5E4 - tag/label bg
  - **color-warning-default**: #F5E5C6 - alert banner bg
  - **color-warning-light**: #FBF3E0 - tag/label bg
  - **color-function-default**: #2C5282
  - **color-function-light**: #D6E4F0 - tag/label bg

### Accent Colors
  - A secondary palette for occasional highlights and categorization. **Avoid overuse** to protect brand identity. Use **sparingly**.
  - **accent-teal-soft**: `text-[#5A9E9E]` or `bg-[#5A9E9E]`
  - **accent-teal-light**: `text-[#A8D5D5]` or `bg-[#A8D5D5]`

### Data Visualization Charts
For data visualization charts only.
  - Standard data colors: #E8E9ED, #C5C9D6, #9BA3B8, #6B7694, #4A5568, #2D3748
  - Important data can use small amounts of: #5A9E9E, #A8D5D5, #2C5282, #4A6FA5

## Typography
- **Font Stack**:
  - **font-family-base**: `-apple-system, BlinkMacSystemFont, "Segoe UI"` — For regular UI copy

- **Font Size & Weight**:
  - **Caption**: `text-sm font-normal`
  - **Body**: `text-base font-normal`
  - **Body Emphasized**: `text-base font-semibold`
  - **Card Title / Subtitle**: `text-lg font-semibold`
  - **Page Title**: `text-xl font-semibold`
  - **Headline**: `text-3xl font-semibold`

- **Line Height**: 1.6

## Border Radius
  - **Small**: 6px — Elements inside cards (e.g., photos, small buttons)
  - **Medium**: 8px — Input fields, smaller cards
  - **Large**: 12px — Cards, containers
  - **Full**: full — Toggles, avatars, small tags, pills

## Layout & Spacing
  - **Tight**: 8px - For closely related small internal elements, such as icons and text within buttons
  - **Compact**: 16px - For small gaps between small containers, such as a line of tags
  - **Standard**: 24px - For gaps between medium containers like list items
  - **Relaxed**: 32px - For gaps between large containers and sections
  - **Section**: 48px - For major section divisions


## Create Boundaries (contrast of surface color, borders, shadows)
No borders, dividers, or shadows. Boundaries are created primarily through subtle surface color differences with very weak contrast, maintaining a unified minimalist aesthetic suitable for medical professionals' extended daily use.

### Borders
  - **Case 1**: No Borders.

### Dividers
  - **Case 1**: No dividers.

### Shadows & Effects
  - **Case 1**: No shadow.

## Visual Emphasis for Containers
When containers (tags, cards, list items, rows) need visual emphasis to indicate priority, status, or category, use the following techniques:

| Technique | Implementation Notes | Best For | Avoid |
|-----------|---------------------|----------|-------|
| Background Tint | Slightly darker/lighter color or reduce transparency of backgrounds | Gentle, common approach for moderate emphasis needs | Heavy colors on large areas (e.g., red background for entire large cards) |
| Status Tag/Label | Add colored tag/label inside container | Larger containers | - |

## Assets
### Image

- For normal `<img>`: object-cover
- For `<img>` with:
  - Slight overlay: object-cover brightness-85
  - Heavy overlay: object-cover brightness-50

### Icon

- Use Lucide icons from Iconify.
- To ensure an aesthetic layout, each icon should be centered in a square container, typically without a background, matching the icon's size.
- Use Tailwind font size to control icon size
- Example:
  ```html
  <div class="flex items-center justify-center bg-transparent w-5 h-5">
  <iconify-icon icon="lucide:flag" class="text-base"></iconify-icon>
  </div>
  ```

### Third-Party Brand Logos:
   - Use Brand Icons from Iconify.
   - Logo Example:
     Monochrome Logo: `<iconify-icon icon="simple-icons:x"></iconify-icon>`
     Colored Logo: `<iconify-icon icon="logos:google-icon"></iconify-icon>`

### User's Own Logo:
- To protect copyright, do **NOT** use real product logos as a logo for a new product, individual user, or other company products.
- **Icon-based**:
  - **Graphic**: Use a simple, relevant icon (e.g., a `stethoscope` icon for a medical app, a `activity` icon for health monitoring).

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
<body class="w-[1440px] min-h-[700px] font-[-apple-system,BlinkMacSystemFont,'Segoe UI'] leading-[1.6]">

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
<body class="w-[1440px] min-h-[700px] flex font-[-apple-system,BlinkMacSystemFont,'Segoe UI'] leading-[1.6]">

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

- **Button**: (Note: Use flex and items-center for the container)
  - Example 1 (Primary button):
    - button: flex items-center gap-2 bg-[#2C5282] text-white/90 hover:bg-[#1A365D] rounded-lg px-6 py-3 transition
      - icon (if applicable)
      - span(button copy): whitespace-nowrap text-base font-semibold
  - Example 2 (Secondary button):
    - button: flex items-center gap-2 bg-[hsla(211,45%,96%,1)] text-[#2C5282] hover:bg-[hsla(211,50%,93%,1)] rounded-lg px-6 py-3 transition
      - icon (if applicable)
      - span(button copy): whitespace-nowrap text-base font-semibold
  - Example 3 (Text button):
    - button: flex items-center gap-2 text-[#2C5282] hover:opacity-70 transition
      - icon (if applicable)
      - span(button copy): whitespace-nowrap text-base font-normal

- **Tag Group (Filter Tags)** (Note: `overflow-x-auto` and `whitespace-nowrap` are required)
  - container(scrollable): flex gap-2 overflow-x-auto [&::-webkit-scrollbar]:hidden
    - label (Tag item 1):
      - input: type="radio" name="tag1" class="sr-only peer" checked
      - div: rounded-full px-4 py-2 bg-[hsla(211,45%,96%,1)] text-[hsla(211,20%,40%,1)] peer-checked:bg-[#2C5282] peer-checked:text-white/90 hover:opacity-80 transition whitespace-nowrap text-sm

### Data Entry
- **Progress bars/Slider**: h-2 bg-[hsla(211,45%,96%,1)] rounded-full
  - filled portion: bg-[#2C5282] h-full rounded-full

- **Checkbox**
  - label: flex items-center gap-3
    - input: type="checkbox" class="sr-only peer"
    - div: w-5 h-5 bg-[hsla(211,45%,96%,1)] rounded-md flex items-center justify-center peer-checked:bg-[#2C5282] text-transparent peer-checked:text-white/90 transition
      - svg(Checkmark): stroke="currentColor" stroke-width="3"
    - span(text): text-base text-[hsla(211,20%,40%,1)]

- **Radio button**
  - label: flex items-center gap-3
    - input: type="radio" name="option1" class="sr-only peer"
    - div: w-5 h-5 bg-[hsla(211,45%,96%,1)] rounded-full flex items-center justify-center peer-checked:bg-[#2C5282] text-transparent peer-checked:text-white/90 transition
      - svg(dot indicator): fill="currentColor"
    - span(text): text-base text-[hsla(211,20%,40%,1)]

- **Switch/Toggle**
  - label: flex items-center gap-3
    - div: relative
      - input: type="checkbox" class="sr-only peer"
      - div(Toggle track): w-12 h-6 bg-[hsla(211,45%,96%,1)] rounded-full peer-checked:bg-[#2C5282] transition
      - div(Toggle thumb): absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full peer-checked:translate-x-6 transition shadow-sm
    - span(text): text-base text-[hsla(211,20%,40%,1)]

- **Select/Dropdown**
  - Select container: flex items-center gap-2 bg-white rounded-lg px-4 py-3
    - text: text-base text-[hsla(211,20%,40%,1)]
    - Dropdown icon(square container): flex items-center justify-center bg-transparent w-5 h-5
      - icon: text-base text-[hsla(211,15%,55%,1)]


### Container
- **Navigation Menu - horizontal**
    - Navigation with sections/grouping:
        - Nav Container: flex items-center justify-between w-full px-8 py-4
        - Left Section: flex items-center gap-12
          - Menu Item: flex items-center gap-2 text-base text-[hsla(211,20%,40%,1)] hover:text-[#2C5282] transition
        - Right Section: flex items-center gap-6
          - Menu Item: flex items-center gap-2 text-base text-[hsla(211,20%,40%,1)] hover:text-[#2C5282] transition
          - Notification (if applicable): relative flex items-center justify-center w-10 h-10
            - notification-icon: w-5 h-5 text-[hsla(211,20%,40%,1)]
            - badge (if has unread): absolute -top-1 -right-1 w-5 h-5 bg-[#E8C5C2] rounded-full flex items-center justify-center
              - badge-count: text-xs font-semibold text-[hsla(211,30%,20%,1)]
          - Avatar(if applicable): flex items-center gap-2
            - avatar-image: w-9 h-9 rounded-full
            - dropdown-icon (if applicable): w-4 h-4 text-[hsla(211,15%,55%,1)]

- **Card**
    - Example 1 (Vertical card with image and text):
        - Card: bg-white rounded-xl flex flex-col p-6 gap-4
        - Image: rounded-lg w-full object-cover
        - Text area: flex flex-col gap-3
          - card-title: text-lg font-semibold text-[hsla(211,30%,20%,1)]
          - card-subtitle: text-sm font-normal text-[hsla(211,20%,40%,1)]
    - Example 2 (Horizontal card with image and text):
        - Card: bg-white rounded-xl flex gap-6 p-6
        - Image: rounded-lg h-full object-cover
        - Text area: flex flex-col gap-3
          - card-title: text-lg font-semibold text-[hsla(211,30%,20%,1)]
          - card-subtitle: text-sm font-normal text-[hsla(211,20%,40%,1)]
    - Example 3 (Image-focused card: no background or padding. Avoid rounded corners on container as they cause only top corners of image to be rounded):
        - Card: flex flex-col gap-4
        - Image: rounded-xl w-full object-cover
        - Text area: flex flex-col gap-3
          - card-title: text-lg font-semibold text-[hsla(211,30%,20%,1)]
          - card-subtitle: text-sm font-normal text-[hsla(211,20%,40%,1)]
    - Example 4 (text-only cards, simple cards, such as Patient Summary Cards, Transcription Status Cards):
        - Card: bg-white rounded-xl flex flex-col p-6 gap-4

## Additional Notes

For medical data presentation:
- Prioritize readability and scanability for extended professional use
- Maintain clear visual hierarchy for patient information and medical records
- Use subtle background tints to differentiate sections without visual fatigue
- Ensure sufficient contrast for accessibility and precision in medical contexts
- Apply generous spacing to prevent information density from overwhelming users


<colors_extraction>
#2C5282
#4A6FA5
#1A365D
hsla(211, 36%, 91%, 1)
hsla(211, 38%, 94%, 1)
hsla(211, 30%, 97%, 1)
#FFFFFF
hsla(211, 40%, 98%, 1)
hsla(211, 45%, 96%, 1)
hsla(211, 50%, 93%, 1)
hsla(211, 30%, 20%, 1)
hsla(211, 20%, 40%, 1)
hsla(211, 15%, 55%, 1)
hsla(211, 10%, 70%, 1)
#FFFFFFE6
#FFFFFFB3
#C6E5D6
#E8F5ED
#E8C5C2
#F7E5E4
#F5E5C6
#FBF3E0
#D6E4F0
#5A9E9E
#A8D5D5
#E8E9ED
#C5C9D6
#9BA3B8
#6B7694
#4A5568
#2D3748
</colors_extraction>
