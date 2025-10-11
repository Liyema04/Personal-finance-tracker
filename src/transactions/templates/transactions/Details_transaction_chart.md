# Related Moves — Chart Breakdown (Beginner, K.I.S.S.)

This page explains the percent-donut chart used on the transaction detail ("Related Moves") card. Keep It Simple — every section below is short and actionable.

---

What the chart shows
- A donut that visualises how much a specific category (e.g. Entertainment) contributes as a percentage of the user's total moves.
- Center text shows the percent (large) and a small subtitle (remainder or category name).
- A small rounded cap shows the arc end for visual polish.

Files involved
- Template: transactions/detail_transaction.html
  - Canvas: <canvas id="chart" data-category="..."> — category string injected via `data-category`.
  - Fallback text: #category-percent-label
  - JS: inline script at bottom builds chartData and plugins.
- JS inside template: builds dataset from `avg_percentage` context value and creates Chart.js doughnut.
- Chart.js: loaded from CDN in the template (or you can use a local static copy).

Data flow (simple)
1. Django view computes p_move_category (numeric percent).
2. View puts `avg_percentage` and `category_display` into the template context.
3. Template renders:
   - canvas data attribute: data-category="{{ category_display|default:transaction.category|escapejs }}"
   - JS reads `avg_percentage` and `data-category`, builds datasets: [primaryPercent, remainder]
4. Chart.js renders doughnut and custom plugin draws center text + rounded cap.

Key JS responsibilities (KISS)
- Read numeric percent: const pct = Number({{ avg_percentage|default:0 }});
- Clamp to 0–100 and compute remainder: primary = Math.min(Math.max(pct,0),100)
- Create chart dataset: data: [primary, 100-primary]
- Custom draw helpers:
  - drawArc(chart, arc, color): fills donut segment on canvas reliably
  - animateArc(chart): compute dynamic color based on arc angle for gradient-like effect
  - drawRoundCaps(chart, arc): draw circular caps at arc ends
- Custom plugin `customText`:
  - beforeDraw: draw base circle (grey)
  - afterDraw: draw center percentage and category text (centered)
  - afterRender: re-apply fill + caps after resize or updates
- Resize handler: debounced resize -> chart.resize(); chart.update('none'); then re-draw custom canvas fills

Why this approach
- Using Chart.js for layout + a custom plugin for canvas drawing keeps the donut responsive while letting us draw custom fills, rounded ends and centered text reliably.
- Passing category via data-attribute avoids messy multi-line template strings in JS.

Common issues & quick fixes (KISS)
- "Canvas is already in use" — fix: destroy existing chart instance before creating a new one.
  - Example: if (window.sentiChart) { window.sentiChart.destroy(); window.sentiChart = null; }
- Center text not centered / broken words — fix: read category from canvas dataset and collapse whitespace (no splitting on wrong chars).
  - Use: const rawCategory = canvas.dataset.category || ''; const category = String(rawCategory).replace(/\s+/g,' ').trim();
- Chart segment disappears but caps show — fix: use even-odd fill and compute radii from meta/controller; normalize start/end angles (see drawArc).
- Styles not applied (CSS loads as HTML) — use Django static tag: @import url("{% static 'css/new-index.css' %}");

Small tweaks you can make (one-line)
- Change donut thickness: adjust CSS/Chart cutout option (cutout: '90%').
- Change center font size: ctx.font = 'bold 48px Roboto, Arial, sans-serif';
- Change animation speed: chartData.options.animation.duration = 800;
- Use local Chart.js: replace CDN <script> with <script src="{% static 'js/chart.min.js' %}"></script>

How to test quickly
1. Hard-refresh (Ctrl+F5) to avoid cached JS/CSS.
2. Open DevTools → Console: ensure no JS errors.
3. Inspect canvas element: should have data-category and the chart instance on window.sentiChart.
4. Resize window — the donut and center text should stay centered and redraw correctly.
5. Use curl to test server-side value:
   curl "http://127.0.0.1:8000/transactions/86/" and inspect HTML for data-category and avg_percentage present.

Accessibility & fallback
- A visible fallback label (#category-percent-label) shows percentage when Chart.js fails.
- Keep `aria-label` on the canvas or include a textual summary in DOM for screen readers.
