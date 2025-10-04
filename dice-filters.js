(async () => {
  // ===== config =====
  const BOOLEAN = '(Appian OR "Appian Developer" OR "Appian Engineer" OR "Appian Architect" OR "Appian BPM" OR "Appian Designer" OR "Appian Consultant") AND (SAIL OR "Appian UI" OR "Appian RPA" OR "Appian Integration" OR "Appian Automation") AND ("Business Process Management" OR BPM) AND (Java OR J2EE OR "JavaScript" OR C#) AND ("low-code" OR "low code" OR "low-code development") AND (workflow OR "process modeling" OR "workflow automation") AND (integration OR API OR "third-party systems") AND (SQL OR "data modeling" OR "data management") AND (AWS OR "Amazon Web Services" OR "Cloud Integration")';
  const LOCATION = 'McLean, VA, USA';
  const DISTANCE_MILES = 50;
  const LAST_ACTIVE_DAYS = 20;

  // ===== utils =====
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const setVal = (el, val) => {
    el.value = val;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  };
  const clickIf = (el) => { if (el) el.click(); };
  const ensureOpen = async (toggleSel, panelSel) => {
    const toggle = document.querySelector(toggleSel);
    const panel  = document.querySelector(panelSel);
    if (toggle && panel && panel.getAttribute('aria-hidden') === 'true') {
      toggle.click();
      await sleep(150);
    }
  };

  try {
    // 0) Clear IntelliSearch “Job Titles” so it won’t hijack the query
    const intelli = document.querySelector('#dhi-typeahead-text-area-search-barjob-titlesInput');
    if (intelli) setVal(intelli, '');

    // 1) Put BOOLEAN into the Keyword or Boolean input
    let kb =
      document.querySelector('input[placeholder*="Keyword or Boolean"]') ||
      document.querySelector('textarea[placeholder*="Keyword or Boolean"]') ||
      document.querySelector('input[aria-label*="Keyword or Boolean"]') ||
      document.querySelector('textarea[aria-label*="Keyword or Boolean"]');
    if (!kb) {
      const label = Array.from(document.querySelectorAll('label'))
        .find(l => /keyword\s*or\s*boolean/i.test(l.textContent || ''));
      if (label) kb = label.parentElement.querySelector('input,textarea');
    }
    if (!kb) { console.warn('Keyword/Boolean field not found.'); return; }
    setVal(kb, BOOLEAN);

    // 2) Location (typeahead)
    const loc = document.querySelector('#google-location-search');
    if (loc) {
      setVal(loc, '');
      setVal(loc, LOCATION);
      await sleep(300);
      const list = document.getElementById('talent-search-location-search-typeahead-list');
      if (list) {
        const opt = Array.from(list.querySelectorAll('[role="option"], li, a, div'))
          .find(x => (x.textContent || '').toLowerCase().includes(LOCATION.toLowerCase()));
        clickIf(opt);
      } else {
        loc.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
      }
    }

    // 3) Distance = 50
    const distanceInput = Array.from(document.querySelectorAll('input[type="number"], input[type="text"]'))
      .find(i => {
        const ctx =
          (i.closest('.float-label-container')?.previousElementSibling?.textContent || '') + ' ' +
          (i.getAttribute('title') || '') + ' ' +
          (i.getAttribute('aria-label') || '') + ' ' +
          (i.placeholder || '');
        return /distance|miles/i.test(ctx);
      });
    if (distanceInput) setVal(distanceInput, String(DISTANCE_MILES));

    // 4) Willing to Relocate popover
    const relocateBtn = document.querySelector('#searchBarWillingToRelocatePopoverToggle');
    if (relocateBtn && relocateBtn.getAttribute('aria-expanded') !== 'true') relocateBtn.click();
    await sleep(150);

    const relocateAnywhere = document.querySelector('#willingtorelocate-facet-option-willing-to-relocate');
    if (relocateAnywhere && !relocateAnywhere.checked) relocateAnywhere.click();

    let includeLocals =
      document.querySelector('.popover-content input[data-cy="exclude-locals-checkbox"]') ||
      document.querySelector('.popover-content #excludeLocals') ||
      document.querySelector('.popover-content input[aria-label*="Include Candidates Living"]');
    if (includeLocals && !includeLocals.disabled) {
      const on = includeLocals.checked || includeLocals.getAttribute('aria-checked') === 'true';
      if (!on) includeLocals.click();
    }
    if (relocateBtn && relocateBtn.getAttribute('aria-expanded') === 'true') relocateBtn.click();

    // 5) Last Active (panel) -> 20
    await ensureOpen('#filter-accordion-date-updated-toggle', '#filter-accordion-date-updated-panel');
    const lastActiveInput = document.querySelector('#filterLastActiveOnBrand');
    if (lastActiveInput) setVal(lastActiveInput, String(LAST_ACTIVE_DAYS));

    // 6) Profile Source: Any
    const profileAny = document.querySelector('#profilesources-facet-option-0');
    if (profileAny && !profileAny.checked) profileAny.click();

    // 7) Contact Method -> uncheck ALL
    await ensureOpen('#filter-accordion-contact-methods-toggle', '#filter-accordion-contact-methods-panel');
    const contactPanel = document.querySelector('#filter-accordion-contact-methods-panel');
    if (contactPanel) {
      const boxes = contactPanel.querySelectorAll('input[type="checkbox"]');
      boxes.forEach(cb => {
        if (cb.checked || cb.getAttribute('aria-checked') === 'true') cb.click();
      });
    }

    // 8) Additional Filters -> uncheck ALL
    await ensureOpen('#filter-accordion-additional-filters-toggle', '#filter-accordion-additional-filters-panel');
    const addlPanel = document.querySelector('#filter-accordion-additional-filters-panel');
    if (addlPanel) {
      const boxes = addlPanel.querySelectorAll('input[type="checkbox"]');
      boxes.forEach(cb => {
        if (cb.checked || cb.getAttribute('aria-checked') === 'true') cb.click();
      });
    }

    // 9) Click Search (ONCE, at the end)
    const searchBtn = document.getElementById('searchButton') || document.querySelector('#searchButton');
    if (searchBtn) searchBtn.click();
    else {
      const btn = Array.from(document.querySelectorAll('button[type="submit"], button'))
        .find(b => /^search$/i.test((b.textContent || '').trim()));
      clickIf(btn);
    }

    // 10) Sanity logs
    await sleep(800);
    console.log('[STATE] lastActiveDays:', document.querySelector('#filterLastActiveOnBrand')?.value);
    console.log('[STATE] email checked:', document.querySelector('#contactinfo-facet-option-contact-method-email')?.checked);
    console.log('[STATE] phone checked:', document.querySelector('#contactinfo-facet-option-contact-method-phone')?.checked);
    console.log('[STATE] profile source any:', document.querySelector('#profilesources-facet-option-0')?.checked);
    console.log('[STATE] exclude 3rd party:', document.querySelector('#additionalfilters-facet-option-exclude-recruiters')?.checked);
    console.log('[STATE] exclude founders:', document.querySelector('#additionalfilters-facet-option-exclude-founders')?.checked);
  } catch (e) {
    console.error('combined script error:', e);
  }
})();
