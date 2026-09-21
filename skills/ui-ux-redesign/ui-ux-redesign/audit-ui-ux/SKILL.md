---
name: audit-ui-ux
description: Run a read-only UI/UX audit of the project in this workspace and write the structured UI/UX Audit Dossier to ui-ux-audit.md.
disable-model-invocation: true
---

# audit-ui-ux — read-only UI/UX audit of the workspace project

Map the project's runtime setup, state lifecycles, and visual debt into a structured **dossier** — the *UI/UX Audit Dossier* — that becomes the exact input to `/plan-redesign`. This command is strictly **read-only**: it inspects and reports; it writes no application code.

## The flow

**1. Environment & configuration discovery.** Detect the framework and runtime (Next.js version from `package.json`; App Router vs Pages Router vs hybrid; React version; TypeScript; bundler), the styling foundation (Tailwind v3 vs v4; `tailwind.config.*` or CSS `@theme`; custom palettes, fonts, spacing tokens, animations; `clsx` / `tailwind-merge` / `cva` helpers; global CSS overrides), and the component ecosystem (UI primitives, icon libraries, animation libraries, toast/feedback libraries).
*Done when:* every framework, styling, and component-ecosystem fact above is recorded from the actual files.

**2. Codebase topology & component hierarchy.** Map all routes, layouts, `error.tsx`, and `loading.tsx`. File every component into one of three categories: atomic primitives (buttons, inputs, badges, modals, cards), domain/feature components (profile card, analytics chart, checkout drawer), and layout wrappers (nav, sidebar, app shell, footer).
*Done when:* the route map is complete and every component is categorized.

**3. Logic & state freeze matrix — the boundary the redesign must not cross.** Catalog every logic anchor that must stay untouched: server vs client boundaries (`'use client'` vs RSC); data-fetching and mutation hooks (SWR, React Query, Apollo, server actions, `fetch` in `useEffect`); form and validation controllers (React Hook Form, Formik, Zod, Yup); state management (Redux, Zustand, Recoil, Jotai, Context, `useSearchParams`); and critical event handlers (`onClick`, `onSubmit`, `onChange`, `onKeyDown`, debounce timers, telemetry such as `gtag` / `posthog` / `mixpanel`).
*Done when:* the freeze matrix lists, per key component, its state hooks, handlers, and external APIs/actions.

**4. Visual debt & inconsistency inventory.** Audit the visual layer across four categories: typography debt (mixed families, unstandardized sizes, arbitrary weights, inconsistent `leading-*` / `tracking-*`); spatial and layout debt (inconsistent padding scales, hardcoded arbitrary values like `w-[342px]`, inline hex/RGB styles, missing responsive breakpoints, broken flex wrapping); depth flaws (flat unbordered cards, muddy dark shadows, weak dark-mode border contrast); and interactive & accessibility gaps (missing `hover:` / `active:` / `focus-visible:` / `disabled:` states, missing loading skeletons, missing `aria-*` / `role`).
*Done when:* each of the four debt categories has a concrete, file-referenced list (or an explicit "none found").

**5. Write the dossier.** Save `ui-ux-audit.md` at the project root containing: the project metadata, the design-system status, the logic-freeze matrix (as a table), the visual-debt inventory, and the **priority refactor candidates** — each component with file path, severity (high / medium / low), and transformation goals. Append the machine-readable JSON dossier (schema below).
*Done when:* `ui-ux-audit.md` exists with all four audit sections filled and a non-empty priority refactor list, ready to hand to `/plan-redesign`.

## Dossier JSON schema (append to ui-ux-audit.md)

```json
{
  "project_metadata": {
    "next_version": "string",
    "router_type": "app | pages | hybrid",
    "react_version": "string",
    "tailwind_version": "string",
    "installed_ui_libraries": ["string"],
    "installed_icon_libraries": ["string"],
    "installed_motion_libraries": ["string"],
    "utility_helpers": ["tailwind-merge", "clsx", "cva"]
  },
  "design_system_status": {
    "custom_tokens_defined": true,
    "color_palette_type": "default-tailwind | custom-css-variables | hardcoded-values",
    "typography_found": ["Inter", "system-ui", "arbitrary"],
    "dark_mode_supported": true,
    "global_css_overrides": ["string"]
  },
  "logic_freeze_matrix": [
    {
      "component_path": "string",
      "component_type": "RSC | Client Component",
      "critical_state_hooks": ["useState", "useQuery", "useForm"],
      "critical_handlers": ["handleSubmit", "handleSort", "onSelectChange"],
      "external_apis_or_actions": ["fetchUsers", "updateBillingAction"]
    }
  ],
  "visual_debt_audit": {
    "typography_inconsistencies": ["string"],
    "spatial_bottlenecks": ["string"],
    "arbitrary_values_detected": ["string"],
    "elevation_and_depth_flaws": ["string"],
    "accessibility_and_contrast_gaps": ["string"],
    "responsive_breakpoint_failures": ["string"]
  },
  "priority_refactor_candidates": [
    {
      "component_name": "string",
      "file_path": "string",
      "severity": "high | medium | low",
      "transformation_goals": "string"
    }
  ]
}
```
