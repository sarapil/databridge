# DataBridge Dashboard — Screen Spec
# لوحة تحكم DataBridge

## Overview

Primary workspace dashboard showing import/export activity, sync status, and data quality metrics.

## Scenarios Served

- Admin DS-001: Configure New Data Source
- Operator DS-001: Run CSV Import
- Manager WS-001: Monitor Sync Profiles

## frappe_visual Components

- `frappe.visual.scenePresetOffice` — Animated workspace header with KPI frames
- `frappe.visual.funnel` — Import pipeline visualization (Pending → Processing → Complete)
- `frappe.visual.sparkline` — Import volume trend per week
- `frappe.visual.donut` — Error distribution by type

## CSS Effects (3+)

- `.fv-fx-glass` — Dashboard card backgrounds
- `.fv-fx-hover-lift` — Card hover interaction
- `.fv-fx-page-enter` — Page entrance animation

## Responsive Breakpoints

| Breakpoint | Layout |
|-----------|--------|
| >= 1280px | 3-column grid |
| 768-1279px | 2-column grid |
| < 768px | Single column stack |

## RTL Support

CSS Logical Properties used throughout. All labels wrapped in `__()`.

## Dark Mode

Uses CSS variables only — no hardcoded colors.
