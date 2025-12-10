# Modern Medical Tech Style Guide

**Style Overview**:
A soft-material design for a modern healthcare platform, featuring gentle elevation through subtle shadows and surface color contrast. Built on a soft natural green primary palette with barely-visible multi-color blur gradient backgrounds, complemented by harmonious Morandi-tone accents for a calm, healing, and professionally modern aesthetic.

## Colors
### Primary Colors
  - **primary-base**: `text-[#7FA990]` or `bg-[#7FA990]`
  - **primary-lighter**: `bg-[#A8C5B5]`
  - **primary-darker**: `text-[#6B8F7D]` or `bg-[#6B8F7D]`

### Background Colors

#### Structural Backgrounds

Choose based on layout type:

**For Vertical Layout** (Top Header + Optional Side Panels):
- **bg-nav-primary**: `bg-[hsla(155, 18%, 96%, 1)]` - Top header
- **bg-nav-secondary**: `bg-[hsla(155, 20%, 98%, 1)]` - Inner Left sidebar (if present)
- **bg-page**: `style="background: radial-gradient(ellipse 800px 600px at 20% 30%, hsla(155, 35%, 92%, 0.15), transparent 50%), radial-gradient(ellipse 700px 500px at 80% 70%, hsla(180, 30%, 90%, 0.12), transparent 50%), hsla(155, 15%, 98%, 1);"` - Page background (bg of Main Content area)

**For Horizontal Layout** (Side Navigation + Optional Top Bar):
- **bg-nav-primary**: `bg-[hsla(155, 18%, 96%, 1)]` - Left main sidebar
- **bg-nav-secondary**: `bg-[hsla(155, 20%, 98%, 1)]` - Inner Top header (if present)
- **bg-page**: `style="background: radial-gradient(ellipse 800px 600px at 20% 30%, hsla(155, 35%, 92%, 0.15), transparent 50%), radial-gradient(ellipse 700px 500px at 80% 70%, hsla(180, 30%, 90%, 0.12), transparent 50%), hsla(155, 15%, 98%, 1);"` - Page background (bg of Main Content area)

#### Container Backgrounds
For main content area. Adjust values when used on navigation backgrounds to ensure sufficient contrast.
- **bg-container-primary**: `bg-white/90`
- **bg-container-secondary**: `bg-white/75`
- **bg-container-inset**: `bg-[#7FA990]/8`
- **bg-container-inset-strong**: `bg-[#6B8F7D]/12`

### Text Colors
- **color-text-primary**: `text-[#2C3E3A]`
- **color-text-secondary**: `text-[#5A6B67]`
- **color-text-tertiary**: `text-[#8A9895]`
- **color-text-quaternary**: `text-[#B5C2BF]`
- **color-text-on-dark-primary**: `text-white/90` - Text on dark backgrounds and primary-base color surfaces
- **color-text-on-dark-secondary**: `text-white/70` - Text on dark backgrounds and primary-base color surfaces
- **color-text-link**: `text-[#7FA990]` - Links, text-only buttons without backgrounds, and clickable text in tables

### Functional Colors
Use **sparingly** to maintain a minimalist and calm overall style. Used for the surfaces of text-only cards, simple cards, buttons, and tags.
  - **color-success-default**: #C8E6D7
  - **color-success-light**: #E5F5ED - tag/label bg
  - **color-error-default**: #E6C8CD - alert banner bg
  - **color-error-light**: #F5E5E8 - tag/label bg
  - **color-warning-default**: #F0E5C8 - tag/label bg
  - **color-warning-light**: #F8F2E0 - tag/label bg, alert banner bg
  - **color-function-default**: #7FA990
  - **color-function-light**: #D4E8DE - tag/label bg

### Accent Colors
  - A secondary palette for occasional highlights and categorization. **Avoid overuse** to protect brand identity. Use **sparingly**.
  - **accent-dusty-emerald**: `text-[#8CA899]` or `bg-[#8CA899]`
  - **accent-soft-blue-gray**: `text-[#9BAEB8]` or `bg-[#9BAEB8]`

### Data Visualization Charts
For data visualization charts only.
  - Standard data colors: #7FA990, #8CA899, #9BAEB8, #A8C5B5, #B5C2BF, #C8D5CF
  - Important data can use small amounts of: #6B8F7D, #5A6B67

## Typography
- **Font Stack**:
  - **font-family-base**: `-apple-system, BlinkMacSystemFont, "Segoe UI"` — For regular UI copy

- **Font Size & Weight**:
  - **Caption**: `text-base font-normal`
  - **Body**: `text-lg font-normal`
  - **Body Emphasized**: `text-lg font-semibold`
  - **Card Title / Subtitle**: `text-xl font-semibold`
  - **Page Title**: `text-2xl font-semibold`
  - **Headline**: `text-4xl font-semibold`

- **Line Height**: 1.5

## Border Radius
  - **Small**: 8px — Elements inside cards (e.g., photos)
  - **Medium**: 12px
  - **Large**: 16px — Cards
  - **Full**: full — Toggles, avatars, small tags, inputs, etc.

## Layout & Spacing
  - **Tight**: 12px - For closely related small internal elements, such as icons and text within buttons
  - **Compact**: 16px - For small gaps between small containers, such as a line of tags
  - **Standard**: 24px - For gaps between medium containers like list items
  - **Relaxed**: 32px - For gaps between large containers and sections
  - **Section**: 40px - For major section divisions

## Create Boundaries (contrast of surface color, borders, shadows)
Case: Primarily relying on subtle shadows and surface color contrast to create gentle elevation and refined boundaries

### Borders
  - **Case 1**: Minimal borders. Only used for inputs and form elements.
    - **Input fields**: 1px solid #D4E8DE. `border border-[#D4E8DE]`
    - **Focus state**: 1px solid #7FA990. `border border-[#7FA990]`

### Dividers
  - **Case 1**: Minimal dividers, used sparingly.
  - **Case 2**: If needed for clear separation, `border-t` or `border-b` `border-[#E5F5ED]`.

### Shadows & Effects
  - **Case 1 (subtle elevation)**: `shadow-[0_2px_8px_rgba(127,169,144,0.08)]` - For cards and containers
  - **Case 2 (moderate elevation)**: `shadow-[0_4px_12px_rgba(127,169,144,0.12)]` - For floating elements, modals
  - **Case 3 (pronounced elevation)**: `shadow-[0_6px_20px_rgba(127,169,144,0.16)]` - For prominent interactive elements

## Visual Emphasis for Containers
When containers (tags, cards, list items, rows) need visual emphasis to indicate priority, status, or category, use the following techniques:

| Technique | Implementation Notes | Best For | Avoid |
|-----------|---------------------|----------|-------|
| Background Tint | Slightly darker/lighter color or reduce transparency of backgrounds | Gentle, common approach for moderate emphasis needs | Heavy colors on large areas (e.g., red background for entire large cards) |
| Border Highlight | Use thin border with opacity for subtlety | Active/selected states, form validation | - |
| Glow/Shadow Effect | Keep shadow subtle with low opacity, using primary color tint | Premium aesthetics, hover states | Overuse in flat designs |
| Status Tag/Label | Add colored tag/label inside container | Larger containers | - |

## Assets
### Image
- For normal `<img>`: object-cover
- For `<img>` with:
  - Slight overlay: object-cover brightness-95
  - Heavy overlay: object-cover brightness-75

### Icon
- Use Lucide icons from Iconify.
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
     Monochrome Logo: `<iconify-icon icon="simple-icons:x"></iconify-icon>`
     Colored Logo: `<iconify-icon icon="logos:google-icon"></iconify-icon>`

### User's Own Logo:
- To protect copyright, do **NOT** use real product logos as a logo for a new product, individual user, or other company products.
- **Icon-based**:
  - **Graphic**: Use a simple, relevant icon (e.g., a `stethoscope` icon for a medical app, a `file-text` icon for a transcription tool).

## Page Layout - Web
### Determine Layout Type
- Choose between Vertical or Horizontal layout based on whether the primary navigation is a full-width top header or a full-height sidebar (left/right).
- User requirements typically indicate the layout preference. If unclear, consider:
  - Marketing/content sites typically use Vertical Layout.
  - Functional/dashboard sites can use either, depending on visual style. Sidebars accommodate more complex navigation than top bars. For complex navigation needs with a preference for minimal chrome (Vertical Layout adds an extra fixed header), choose Horizontal Layout (omits the fixed top header).
- Vertical Layout Diagram:
```
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
```
- Horizontal Layout Diagram:
```
┌──────────┬──────────────────────────────┬───────────┐
│          │ Header (Secondary Nav)       │           │
│ Left     │ (optional)                   │ Right     │
│ Sidebar  ├──────────────────────────────┤ Sidebar   │
│ (Primary │ Main Content                 │ (Utility  │
│ Nav)     │                              │ Panel)    │
│          │                              │ (optional)│
│          │                              │           │
└──────────┴──────────────────────────────┴───────────┘
```
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

- **Button**: (Note: Use flex and items-center for the container)
  - Example 1 (Primary button):
    - button: flex items-center gap-2 bg-[#7FA990] text-white/90 px-6 py-3 rounded-full hover:bg-[#6B8F7D] transition shadow-[0_2px_8px_rgba(127,169,144,0.12)]
      - icon (if applicable)
      - span(button copy): whitespace-nowrap font-semibold
  - Example 2 (Secondary button):
    - button: flex items-center gap-2 bg-white/90 text-[#7FA990] px-6 py-3 rounded-full hover:bg-white transition shadow-[0_2px_8px_rgba(127,169,144,0.08)]
      - icon (if applicable)
      - span(button copy): whitespace-nowrap font-semibold
  - Example 3 (text button):
    - button: flex items-center gap-2 text-[#7FA990] hover:opacity-70 transition
      - icon (if applicable)
      - span(button copy): whitespace-nowrap

- **Tag Group (Filter Tags)** (Note: `overflow-x-auto` and `whitespace-nowrap` are required)
  - container(scrollable): flex gap-3 overflow-x-auto [&::-webkit-scrollbar]:hidden
    - label (Tag item):
      - input: type="radio" name="tag1" class="sr-only peer" checked
      - div: bg-white/75 text-[#5A6B67] px-4 py-2 rounded-full peer-checked:bg-[#7FA990] peer-checked:text-white/90 hover:opacity-70 transition whitespace-nowrap shadow-[0_2px_6px_rgba(127,169,144,0.06)] peer-checked:shadow-[0_2px_8px_rgba(127,169,144,0.12)]

### Data Entry
- **Progress bars/Slider**: h-2 bg-[#E5F5ED] rounded-full
  - progress-fill: bg-[#7FA990] h-full rounded-full
- **Checkbox**
  - label: flex items-center gap-3
    - input: type="checkbox" class="sr-only peer"
    - div: w-5 h-5 bg-white/90 rounded-md flex items-center justify-center peer-checked:bg-[#7FA990] text-transparent peer-checked:text-white/90 border border-[#D4E8DE] peer-checked:border-[#7FA990] transition shadow-[0_1px_3px_rgba(127,169,144,0.06)]
      - svg(Checkmark): stroke="currentColor" stroke-width="3"
    - span(text): text-[#2C3E3A]
- **Radio button**
  - label: flex items-center gap-3
    - input: type="radio" name="option1" class="sr-only peer"
    - div: w-5 h-5 bg-white/90 rounded-full flex items-center justify-center peer-checked:bg-[#7FA990] text-transparent peer-checked:text-white/90 border border-[#D4E8DE] peer-checked:border-[#7FA990] transition shadow-[0_1px_3px_rgba(127,169,144,0.06)]
      - svg(dot indicator): fill="currentColor"
    - span(text): text-[#2C3E3A]
- **Switch/Toggle**
  - label: flex items-center gap-3
    - div: relative
      - input: type="checkbox" class="sr-only peer"
      - div(Toggle track): w-14 h-7 bg-white/90 peer-checked:bg-[#7FA990] transition rounded-full shadow-[0_2px_6px_rgba(127,169,144,0.08)]
      - div(Toggle thumb): absolute top-0.5 left-0.5 w-6 h-6 bg-[#E5F5ED] peer-checked:bg-white rounded-full peer-checked:translate-x-7 transition shadow-[0_2px_4px_rgba(127,169,144,0.12)]
    - span(text): text-[#2C3E3A]

- **Select/Dropdown**
  - Select container: flex items-center gap-2 bg-white/90 px-4 py-3 rounded-full shadow-[0_2px_6px_rgba(127,169,144,0.06)] border border-[#D4E8DE]
    - text: text-[#2C3E3A]
    - Dropdown icon(square container): flex items-center justify-center bg-transparent w-5 h-5
      - icon: text-[#7FA990]

### Container
- **Navigation Menu - horizontal**
    - Navigation with sections/grouping:
        - Nav Container: flex items-center justify-between w-full px-8 py-4
        - Left Section: flex items-center gap-10
          - Menu Item: flex items-center gap-3 text-[#5A6B67] hover:text-[#7FA990] transition
        - Right Section: flex items-center gap-4
          - Menu Item: flex items-center gap-3 text-[#5A6B67] hover:text-[#7FA990] transition
          - Notification (if applicable): relative flex items-center justify-center w-10 h-10 rounded-full bg-white/75 shadow-[0_2px_6px_rgba(127,169,144,0.06)]
            - notification-icon: w-5 h-5 text-[#7FA990]
            - badge (if has unread): absolute -top-1 -right-1 w-5 h-5 rounded-full bg-[#7FA990] flex items-center justify-center shadow-[0_2px_4px_rgba(127,169,144,0.12)]
              - badge-count: text-xs text-white/90 font-semibold
          - Avatar(if applicable): flex items-center gap-2
            - avatar-image: w-10 h-10 rounded-full border-2 border-white/75 shadow-[0_2px_6px_rgba(127,169,144,0.08)]
            - dropdown-icon (if applicable): w-5 h-5 text-[#7FA990]

- **Card**
    - Example 1 (Vertical card with image and text):
        - Card: bg-white/90 rounded-2xl flex flex-col p-5 gap-4 shadow-[0_2px_8px_rgba(127,169,144,0.08)] hover:shadow-[0_4px_12px_rgba(127,169,144,0.12)] transition
        - Image: rounded-xl w-full object-cover
        - Text area: flex flex-col gap-3
          - card-title: text-xl font-semibold text-[#2C3E3A]
          - card-subtitle: text-base font-normal text-[#5A6B67]
    - Example 2 (Horizontal card with image and text):
        - Card: bg-white/90 rounded-2xl flex gap-5 p-5 shadow-[0_2px_8px_rgba(127,169,144,0.08)] hover:shadow-[0_4px_12px_rgba(127,169,144,0.12)] transition
        - Image: rounded-xl h-full object-cover w-32
        - Text area: flex flex-col gap-4 flex-1
          - card-title: text-xl font-semibold text-[#2C3E3A]
          - card-subtitle: text-base font-normal text-[#5A6B67]
    - Example 3 (Image-focused card):
        - Card: flex flex-col gap-4
        - Image: rounded-2xl w-full object-cover shadow-[0_2px_8px_rgba(127,169,144,0.08)]
        - Text area: flex flex-col gap-3
          - card-title: text-xl font-semibold text-[#2C3E3A]
          - card-subtitle: text-base font-normal text-[#5A6B67]
    - Example 4 (Simple status/info cards):
        - Card: bg-[#E5F5ED] rounded-2xl flex flex-col p-6 gap-3 shadow-[0_2px_6px_rgba(127,169,144,0.06)]
          - card-title: text-xl font-semibold text-[#2C3E3A]
          - card-content: text-base font-normal text-[#5A6B67]

## Additional Notes
This style guide creates a calm, healing atmosphere suitable for medical professionals while maintaining modern design standards. The soft-material approach with gentle shadows provides clear visual hierarchy without harsh contrasts, supporting the wellness-focused nature of the MediAI platform.

<colors_extraction>
#7FA990
#A8C5B5
#6B8F7D
hsla(155, 18%, 96%, 1)
hsla(155, 20%, 98%, 1)
radial-gradient(ellipse 800px 600px at 20% 30%, hsla(155, 35%, 92%, 0.15), transparent 50%), radial-gradient(ellipse 700px 500px at 80% 70%, hsla(180, 30%, 90%, 0.12), transparent 50%), hsla(155, 15%, 98%, 1)
#FFFFFFE6
#FFFFFFBF
#7FA99014
#6B8F7D1F
#2C3E3A
#5A6B67
#8A9895
#B5C2BF
#FFFFFFE6
#FFFFFFB3
#C8E6D7
#E5F5ED
#E6C8CD
#F5E5E8
#F0E5C8
#F8F2E0
#7FA990
#D4E8DE
#8CA899
#9BAEB8
#C8D5CF
#FFFFFF
</colors_extraction>
