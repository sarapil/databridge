// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for DataBridge — Scene Dashboard & Visual Components

(function() {
    "use strict";

    // ── App Configuration ─────────────────────────────────────────
    const APP_CONFIG = {
        name: "databridge",
        title: "DataBridge",
        color: "#0EA5E9",
        gradient: "linear-gradient(135deg, #0EA5E9, #0284C7)",
        module: "DataBridge",
    };

    // ── CSS Variables Registration ────────────────────────────────
    function registerCSSVariables() {
        document.documentElement.style.setProperty("--databridge-primary", APP_CONFIG.color);
        document.documentElement.style.setProperty("--databridge-gradient", APP_CONFIG.gradient);
    }

    // ── Scene Dashboard Builder ───────────────────────────────────
    async function buildSceneDashboard(container) {
        if (!frappe.visual) {
            console.warn("[DataBridge] frappe_visual not available for scene dashboard");
            return null;
        }

        try {
            let sceneContainer = container.querySelector('#databridge-scene-header');
            if (!sceneContainer) {
                sceneContainer = document.createElement('div');
                sceneContainer.id = 'databridge-scene-header';
                sceneContainer.className = 'databridge-scene-container fv-fx-glass';
                container.insertBefore(sceneContainer, container.firstChild);
            }

            const scene = await frappe.visual.scenePresetOffice({
                container: '#databridge-scene-header',
                theme: 'cool',
                frames: [
                    { label: __('Active Syncs'), status: 'success' },
                    { label: __('Records Imported'), status: 'info' },
                    { label: __('Pending Jobs'), status: 'warning' },
                    { label: __('Failed Imports'), status: 'danger' }
                ],
                documents: [{ label: __('Recent Jobs'), href: '/app/db-import-job', color: '#0EA5E9' }],
                books: [{ label: __('DataBridge Help'), href: '/databridge-onboarding', color: '#0EA5E9' }]
            });

            if (frappe.visual.sceneDataBinder) {
                await frappe.visual.sceneDataBinder({
                    engine: scene,
                    frames: [
                        { label: __('Active Syncs'), doctype: 'DB Sync Configuration', aggregate: 'count', filters: { is_enabled: 1 }, status_rules: { '>0': 'success' } },
                        { label: __('Records Imported'), method: 'databridge.api.dashboard.get_total_records', status_rules: { '>10000': 'success', '<100': 'warning' } },
                        { label: __('Pending Jobs'), doctype: 'DB Import Job', aggregate: 'count', filters: { status: 'Pending' }, status_rules: { '>5': 'warning', '>20': 'danger' } },
                        { label: __('Failed Imports'), doctype: 'DB Import Job', aggregate: 'count', filters: { status: 'Failed' }, status_rules: { '>0': 'danger' } }
                    ],
                    refreshInterval: 30000
                });
            }
            return scene;
        } catch (e) {
            console.error("[DataBridge] Scene dashboard error:", e);
            return null;
        }
    }

    // ── KPI Cards Builder (Fallback) ──────────────────────────────
    async function buildKPICards(container) {
        const kpiContainer = document.createElement('div');
        kpiContainer.className = 'databridge-kpi-grid';
        kpiContainer.innerHTML = `
            <div class="databridge-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="syncs">
                <div class="databridge-kpi-icon">🔄</div>
                <div class="databridge-kpi-value" data-field="syncs_count">--</div>
                <div class="databridge-kpi-label">${__('Active Syncs')}</div>
            </div>
            <div class="databridge-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="records">
                <div class="databridge-kpi-icon">📊</div>
                <div class="databridge-kpi-value" data-field="records_count">--</div>
                <div class="databridge-kpi-label">${__('Records Imported')}</div>
            </div>
            <div class="databridge-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="connections">
                <div class="databridge-kpi-icon">🔗</div>
                <div class="databridge-kpi-value" data-field="connections_count">--</div>
                <div class="databridge-kpi-label">${__('Connections')}</div>
            </div>
            <div class="databridge-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="mappings">
                <div class="databridge-kpi-icon">🗺️</div>
                <div class="databridge-kpi-value" data-field="mappings_count">--</div>
                <div class="databridge-kpi-label">${__('Field Mappings')}</div>
            </div>
        `;
        container.insertBefore(kpiContainer, container.firstChild);

        try {
            const stats = await frappe.xcall('databridge.api.dashboard.get_dashboard_stats');
            if (stats) {
                animateNumber(kpiContainer.querySelector('[data-field="syncs_count"]'), stats.syncs_count || 0);
                animateNumber(kpiContainer.querySelector('[data-field="records_count"]'), stats.records_count || 0);
                animateNumber(kpiContainer.querySelector('[data-field="connections_count"]'), stats.connections_count || 0);
                animateNumber(kpiContainer.querySelector('[data-field="mappings_count"]'), stats.mappings_count || 0);
            }
        } catch (e) {
            console.warn("[DataBridge] KPI fetch failed:", e);
        }
    }

    // ── Number Animation ──────────────────────────────────────────
    function animateNumber(element, targetValue) {
        if (!element) return;
        const duration = 1000, start = 0, startTime = performance.now();
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            element.textContent = Math.round(start + (targetValue - start) * eased).toLocaleString();
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    }

    // ── Workspace Enhancement ─────────────────────────────────────
    async function enhanceWorkspace() {
        const workspaceMain = document.querySelector('.workspace-main');
        if (!workspaceMain) return;
        workspaceMain.classList.add('fv-fx-page-enter');
        if (frappe.visual && frappe.visual.scenePresetOffice) {
            await buildSceneDashboard(workspaceMain);
        } else {
            await buildKPICards(workspaceMain);
        }
    }

    // ── Form Dashboard Enhancement ────────────────────────────────
    function enhanceFormDashboard(frm) {
        if (!frm || !frappe.visual) return;
        const dbDocTypes = ['DB Import Job', 'DB Migration Project', 'DB Field Map', 'DB Sync Configuration', 'DB Source Connection', 'DB API Connection'];
        if (!dbDocTypes.includes(frm.doctype)) return;
        if (frappe.visual.formDashboard) {
            const dashContainer = frm.page.main.find('.form-dashboard');
            if (dashContainer.length) {
                frappe.visual.formDashboard(dashContainer[0], { doctype: frm.doctype, docname: frm.doc.name });
            }
        }
    }

    // ── Initialize ────────────────────────────────────────────────
    $(document).on("app_ready", function() {
        registerCSSVariables();
        if (frappe.visual && frappe.visual.ThemeManager) {
            try { frappe.visual.ThemeManager.registerApp(APP_CONFIG); } catch(e) {}
        }
    });

    $(document).on("page-change", function() {
        const route = frappe.get_route_str();
        if (route.includes('databridge') || route.includes('DataBridge')) setTimeout(enhanceWorkspace, 100);
        if (route === 'databridge-settings' && frappe.visual && frappe.visual.generator) {
            const page = frappe.container.page;
            if (page && page.main) frappe.visual.generator.settingsPage(page.main[0] || page.main, "DataBridge Settings");
        }
        if (route === 'databridge-reports' && frappe.visual && frappe.visual.generator) {
            const page = frappe.container.page;
            if (page && page.main) frappe.visual.generator.reportsHub(page.main[0] || page.main, "DataBridge");
        }
    });

    $(document).on("form-refresh", function(e, frm) { enhanceFormDashboard(frm); });

    frappe.databridge = frappe.databridge || {};
    frappe.databridge.visual = { buildSceneDashboard, buildKPICards, animateNumber };
})();
