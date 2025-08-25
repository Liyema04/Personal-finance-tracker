# Transactions list — README (Beginner, KISS)

Purpose
- Explain how the list template and view work.
- Describe the two new features: Filtering and Lazy Load (on demand).
- Give quick steps to test and debug.

Files involved (main)
- templates/transactions/list_transaction.html
  - UI for showing transactions, filter dropdown and "Load more" button.
  - Small JS blocks: filter click handler, pagination-config JSON, and the client-side DjangoLazyTransactionsLoader class.
- templates/transactions/transaction_rows.html
  - Partial used by AJAX to render additional <tr> rows.
- src/transactions/views.py
  - transactions_list_page(request) — renders initial page and filter handling.
  - handle_ajax_transactions(request, transactions_qs) — returns JSON for offset/limit AJAX requests.
- static JS (optional)
  - You may move inline JS from the template to a static file (recommended for production).

Feature overview (KISS)
- Filtering
  - UI: dropdown items with data-type and fallback href for non-JS users.
  - Client: when a filter is clicked the JS builds a URL that preserves non-pagination query params and removes page/offset/limit, then navigates to it.
  - Server: TransactionFilter uses request.GET to filter the queryset. The initial page shows the first N results that match the filter.

- Lazy Load (on demand)
  - Client: DjangoLazyTransactionsLoader reads pagination-config (initial_page_size, load_more_size, api_url, csrf_token).
  - The loader tracks how many rows are currently in the DOM and uses offset = loadedRows, limit = loadMoreSize.
  - On click (or IntersectionObserver auto-load) it calls the API URL with offset & limit and expects JSON.
  - Server: handle_ajax_transactions slices the filtered queryset and returns:
    - success: true, html: "rendered rows", count, has_more, current_page, debug fields
  - Client inserts returned rows into <tbody> (supports returned HTML or JSON rows) and updates counters.

How filtering + lazy load interact
- When changing a filter we must reset pagination state:
  - Client removes offset/limit/page query params before navigating.
  - Client resets transactionLoader (disconnect observer & re-sync DOM count).
- Server always filters based on current GET params; AJAX calls include those params (except pagination ones which the client overrides).

Quick configuration points
- control sizes in template pagination-config JSON:
  - initial_page_size: number shown on first render (server uses paginator(15) by default)
  - load_more_size: how many are requested per "Load more" click (client & server)
- API URL is configured to the same view URL ({% url 'list_transaction' %}) — handle_ajax_transactions detects AJAX via X-Requested-With.
- CSRF: AJAX GETs typically don't need CSRF, but header X-CSRFToken is set by the loader if provided.

Testing steps (fast)
1. Load page, open DevTools → Network → Fetch/XHR.
2. Click Filter:
   - Confirm new page navigation URL contains transaction_type and does NOT include offset/limit/page.
   - If no network request, open Console for JS errors (template DOM broken?).
3. Click "Load more":
   - Observe a GET request to the API URL with offset and limit in the query string.
   - Response should be JSON with "success": true and "html" containing <tr> rows.
4. Curl examples:
   - Initial page (server-rendered): curl -I http://127.0.0.1:8000/dashboard
   - AJAX test (example): curl -G "http://127.0.0.1:8000/transactions/?offset=5&limit=5" -H "X-Requested-With: XMLHttpRequest"

Common problems & fixes
- No rows appended / duplicates:
  - Client kept stale offset/limit in query when switching filters — fix: remove pagination params when building filter URL.
- No AJAX request on filter click:
  - Broken DOM (unclosed tag) can stop JS — check Console for parse errors and fix HTML.
- 404 for partial template:
  - render_to_string('transactions/transaction_rows.html', ...) must point to an existing template. Ensure file exists.
- Template include vs static:
  - To inline SVG into the HTML use `{% include 'transactions/svg/your.svg' %}` — the file must live in templates.
  - To use `<img src="{% static 'path.svg' %}">` place SVG under static/ and ensure static config is correct.
- Fonts in external SVG:
  - External SVG loaded as <img> may not inherit page fonts and may load its own font. If you see different font render, inline the SVG or convert text to paths.

Debugging tips
- Use console logs already added by the client JS (it logs filter clicks, fetch URLs, and response data).
- Inspect Network → request URL & response JSON. Compare 'requested_offset' and 'returned_html_length' fields in JSON.
- Server-side: view has debug prints. Watch runserver console for DEBUG lines and stack traces.
- If template include fails: TemplateDoesNotExist means the included path is not in template search paths — move file to templates/transactions/svg/ or use {% static %}.

Minimal checklist to get working
- Ensure transaction_rows.html exists and matches server render expectations.
- Confirm transactions_list_page is included in urls.py and that handle_ajax_transactions is reachable (X-Requested-With header triggers it).
- Confirm initial template renders table rows and pagination-config values match server-side Paginator.
- Hard-refresh (Ctrl+F5) after template/JS changes.

If you want, I can:
- produce the exact minimal transaction_rows.html partial,
- create a static JS file for the loader and move inline script into it,
- or give exact curl output expectations for your current debug logs.