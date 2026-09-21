# TRANSFORM recipes

The concrete presentation upgrades `implement-plan` applies, grouped by dimension. This is the *how*. The *what to change* (which components, which phase) comes from `plan.md`, and the *boundary* (what must not move) comes from `plan.md`'s 5 logic-freeze instructions.

## Design tokens
- Colors → semantic tokens or one consistent Tailwind ramp (`slate`, `zinc`, or `neutral`); no pure `#000000` or `#ffffff`.
- Confirm the `cn()` helper (`clsx` + `tailwind-merge`) exists; route every class composition through it.
- Dark mode via `dark:` variants on semantic tokens, not raw colors.

## Typography & visual hierarchy
- Display / page titles: `text-2xl sm:text-3xl font-semibold tracking-tight text-foreground`
- Section headers: `text-lg sm:text-xl font-medium tracking-tight text-foreground`
- Card titles: `text-base font-medium text-foreground`
- Primary body: `text-sm font-normal leading-relaxed text-muted-foreground`
- Captions / meta: `text-xs font-medium tracking-wide uppercase text-muted-foreground/80`
- Numerical readouts (currency, timers, metrics, timestamps): `font-mono tabular-nums`
- Hold a ~3:1 contrast between headings and supporting text; `max-w-prose` on long-form; `truncate` / `line-clamp-2` + full tooltip on dynamic user content.

## Spatial rhythm, depth & bento
- 8pt grid: paddings/margins to `gap-2` (8px) / `gap-3` (12px) / `gap-4` (16px) / `gap-6` (24px); component padding `p-4 sm:p-6`; card/modal headers `px-6 py-4`; form fields `space-y-4`.
- Layered, semi-transparent borders: `border border-zinc-200/80 dark:border-zinc-800/80`.
- Glassmorphism on floating cards/headers: `bg-white/70 dark:bg-zinc-900/70 backdrop-blur-md backdrop-saturate-150`.
- Premium cards: `shadow-sm ring-1 ring-black/5 dark:ring-white/10`.
- Bento grids: `grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4`; featured items span columns (`md:col-span-2`).
- Unified corner radii `rounded-xl` / `rounded-2xl`; concentric radius rule `R_inner = R_outer - padding`.

## Micro-interactions & motion
- Transitions: `transition-all duration-150 ease-out`.
- Hover elevation: `hover:bg-zinc-50 dark:hover:bg-zinc-800/60 hover:border-zinc-300 dark:hover:border-zinc-700`.
- Active press: `active:scale-[0.98] active:transition-transform`.
- Focus: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 dark:focus-visible:ring-offset-zinc-950`.
- Loading skeletons: `animate-pulse rounded-md bg-zinc-200/70 dark:bg-zinc-800/70`; optional linear-gradient shimmer on primary loading.
- Spring motion: `transition={{ type: "spring", stiffness: 350, damping: 25 }}`; shared tab indicator via `layoutId="active-indicator"` inside `AnimatePresence` / `motion.*`.

## Responsive & mobile
- Touch targets: `min-h-[44px] min-w-[44px] sm:min-h-[36px] sm:min-w-[36px]`; add `touch-manipulation`.
- Tables → cards on mobile: `hidden sm:table` + `sm:hidden flex flex-col gap-3`.
- Modals → bottom sheets on mobile: `inset-x-0 bottom-0 rounded-t-2xl sm:inset-auto sm:rounded-xl` (Vaul / Radix Sheet pattern).
- Sticky mobile CTA: `fixed bottom-0 left-0 right-0 p-4 bg-background/80 backdrop-blur-lg border-t sm:static sm:bg-transparent sm:p-0 sm:border-0`.
- Overflow: `min-w-0` on flex items; `overflow-x-auto` + custom scrollbar on wide code blocks/charts.

## Accessibility
- `aria-label` / `aria-expanded` / `role` on interactive elements; focus traps in dialogs/modals; full keyboard navigation; WCAG AA contrast.
