import os
import re

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Add ID to backToObjects button
old_btn = '<button onclick="backToObjects()" class="p-2 -ml-2 text-gray-400 hover:text-white rounded-lg hover:bg-gray-800 transition-colors" title="Zurück zur Objektübersicht">'
new_btn = '<button id="backToObjectsBtn" onclick="backToObjects()" class="p-2 -ml-2 text-gray-400 hover:text-white rounded-lg hover:bg-gray-800 transition-colors" title="Zurück zur Objektübersicht">'
app_content = app_content.replace(old_btn, new_btn)

# 2. Hide/Show backToObjectsBtn
old_show_detail = '''        function showDetail(catId) {
            currentCategoryId = catId;
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.add('hidden');
            document.getElementById('inboxView').classList.add('hidden');
            document.getElementById('detailView').classList.remove('hidden');'''
new_show_detail = '''        function showDetail(catId) {
            currentCategoryId = catId;
            document.getElementById('backToObjectsBtn').classList.add('hidden');
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.add('hidden');
            document.getElementById('inboxView').classList.add('hidden');
            document.getElementById('detailView').classList.remove('hidden');'''
app_content = app_content.replace(old_show_detail, new_show_detail)

old_show_dashboard = '''        function showDashboard() {
            currentCategoryId = null;
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.add('hidden');
            document.getElementById('inboxView').classList.add('hidden');
            document.getElementById('dashboardView').classList.remove('hidden');'''
new_show_dashboard = '''        function showDashboard() {
            currentCategoryId = null;
            document.getElementById('backToObjectsBtn').classList.remove('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.add('hidden');
            document.getElementById('inboxView').classList.add('hidden');
            document.getElementById('dashboardView').classList.remove('hidden');'''
app_content = app_content.replace(old_show_dashboard, new_show_dashboard)

# 3. Update exportModal HTML
old_export_modal = '''        <!-- Export Modal -->
        <div id="exportModal" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
            <div class="fixed inset-0 bg-gray-950/80 backdrop-blur-sm transition-opacity"
                onclick="closeModal('exportModal')"></div>
            <div class="relative bg-gray-900 border border-gray-700 rounded-xl shadow-2xl w-full max-w-sm slide-up p-6">
                <h3 class="text-lg font-bold flex items-center gap-2 mb-4 border-b border-gray-800 pb-2"><i
                        data-lucide="download" class="w-5 h-5"></i> Daten exportieren</h3>
                <div class="space-y-3">
                    <p class="text-xs text-gray-400 mb-2">Wähle das Format für den Export deiner Zählerstände.</p>
                    <button onclick="executeExport('excel')"
                        class="w-full px-4 py-3 text-sm font-medium text-white bg-green-600 hover:bg-green-500 rounded-lg transition-colors flex justify-center items-center gap-2 shadow-lg shadow-green-500/20">
                        <i data-lucide="file-spreadsheet" class="w-4 h-4"></i> Als Excel (.xlsx)
                    </button>
                    <button onclick="executeExport('csv')"
                        class="w-full px-4 py-3 text-sm font-medium text-gray-300 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors flex justify-center items-center gap-2 border border-gray-700">
                        <i data-lucide="file-text" class="w-4 h-4"></i> Als CSV (.csv)
                    </button>
                    <button onclick="closeModal('exportModal')"
                        class="w-full px-4 py-3 text-sm bg-transparent hover:text-white text-gray-400 rounded-lg">Abbrechen</button>
                </div>
            </div>
        </div>'''
new_export_modal = '''        <!-- Export Modal -->
        <div id="exportModal" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
            <div class="fixed inset-0 bg-gray-950/80 backdrop-blur-sm transition-opacity"
                onclick="closeModal('exportModal')"></div>
            <div class="relative bg-gray-900 border border-gray-700 rounded-xl shadow-2xl w-full max-w-md slide-up p-6">
                <h3 class="text-lg font-bold flex items-center gap-2 mb-4 border-b border-gray-800 pb-2"><i
                        data-lucide="download" class="w-5 h-5"></i> Daten exportieren</h3>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Format</label>
                        <select id="exportFormat" class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors text-sm">
                            <option value="excel">Excel (.xlsx)</option>
                            <option value="csv">CSV (.csv)</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Bereiche</label>
                        <div id="exportCategoriesList" class="bg-gray-800 border border-gray-700 rounded-lg p-3 max-h-40 overflow-y-auto space-y-2">
                            <!-- JS Injected -->
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-1">Von Datum</label>
                            <input type="date" id="exportDateFrom" class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors text-sm">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-1">Bis Datum</label>
                            <input type="date" id="exportDateTo" class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors text-sm">
                        </div>
                    </div>

                    <button onclick="executeExport()"
                        class="w-full mt-2 px-4 py-3 text-sm font-medium text-white bg-primary-600 hover:bg-primary-500 rounded-lg transition-colors flex justify-center items-center gap-2 shadow-lg shadow-primary-500/20">
                        <i data-lucide="download" class="w-4 h-4"></i> Exportieren
                    </button>
                    <button onclick="closeModal('exportModal')"
                        class="w-full px-4 py-2 text-sm bg-transparent hover:text-white text-gray-400 rounded-lg transition-colors">Abbrechen</button>
                </div>
            </div>
        </div>'''
app_content = app_content.replace(old_export_modal, new_export_modal)

# 4. Update JS logic for openExportModal and executeExport
old_js_export = '''        // --- Export / Import ---
        function openExportModal() {
            const modal = document.getElementById('exportModal');
            modal.classList.remove('hidden'); modal.classList.add('flex');
        }

        function executeExport(format = 'csv') {
            if (appData.length === 0) {
                showToast('Keine Daten', 'error'); return;
            }
            // Join with category names
            const exportData = appData.map(d => {
                const cat = categories.find(c => c.id === d.categoryId);
                return {
                    Datum: d.date,
                    Bereich: cat ? cat.name : 'Gelöscht',
                    Zählernummer: cat ? (cat.meterNumber || '') : '',
                    Einheit: cat ? cat.unit : '',
                    Stand: d.value,
                    Kommentar: cat ? (cat.comment || '').replace(/"/g, '""') : '',
                    Notiz: d.isMeterChangeStart ? "Neuer Zähler Einbau" : (d.isMeterChangeEnd ? "Alter Zähler Ausbau" : (d.isInitial ? "Startwert" : ""))
                };
            });'''
new_js_export = '''        // --- Export / Import ---
        function openExportModal() {
            const modal = document.getElementById('exportModal');
            
            const list = document.getElementById('exportCategoriesList');
            list.innerHTML = '';
            categories.forEach(c => {
                list.innerHTML += `
                    <label class="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                        <input type="checkbox" class="export-category-cb w-4 h-4 text-primary-600 bg-gray-900 border-gray-600 rounded focus:ring-primary-500 cursor-pointer" value="${c.id}" checked>
                        ${c.name}
                    </label>
                `;
            });
            if(categories.length === 0) {
                list.innerHTML = '<span class="text-sm text-gray-500">Keine Bereiche vorhanden</span>';
            }
            
            document.getElementById('exportDateFrom').value = '';
            document.getElementById('exportDateTo').value = '';
            
            modal.classList.remove('hidden'); modal.classList.add('flex');
        }

        function executeExport() {
            const format = document.getElementById('exportFormat').value;
            const fromDateStr = document.getElementById('exportDateFrom').value;
            const toDateStr = document.getElementById('exportDateTo').value;
            
            const cbs = document.querySelectorAll('.export-category-cb:checked');
            const selectedCatIds = Array.from(cbs).map(cb => cb.value);
            
            if (selectedCatIds.length === 0) {
                return showToast('Bitte mindestens einen Bereich auswählen', 'error');
            }
            
            if (appData.length === 0) {
                showToast('Keine Daten vorhanden', 'error'); return;
            }
            
            let filteredData = appData.filter(d => selectedCatIds.includes(d.categoryId));
            
            if (fromDateStr) {
                const fromDate = new Date(fromDateStr);
                filteredData = filteredData.filter(d => new Date(d.date) >= fromDate);
            }
            if (toDateStr) {
                const toDate = new Date(toDateStr);
                filteredData = filteredData.filter(d => new Date(d.date) <= toDate);
            }
            
            if (filteredData.length === 0) {
                showToast('Keine Daten für diesen Zeitraum', 'error'); return;
            }

            // Join with category names
            const exportData = filteredData.map(d => {
                const cat = categories.find(c => c.id === d.categoryId);
                return {
                    Datum: d.date,
                    Bereich: cat ? cat.name : 'Gelöscht',
                    Zählernummer: cat ? (cat.meterNumber || '') : '',
                    Einheit: cat ? cat.unit : '',
                    Stand: d.value,
                    Kommentar: cat ? (cat.comment || '').replace(/"/g, '""') : '',
                    Notiz: d.isMeterChangeStart ? "Neuer Zähler Einbau" : (d.isMeterChangeEnd ? "Alter Zähler Ausbau" : (d.isInitial ? "Startwert" : ""))
                };
            });'''
app_content = app_content.replace(old_js_export, new_js_export)

# Also close modal at the end of executeExport
old_execute_end = '''            }

        }

        // CSV Helper'''
new_execute_end = '''            }
            closeModal('exportModal');
        }

        // CSV Helper'''
app_content = app_content.replace(old_execute_end, new_execute_end)

with open(app_path, "w") as f:
    f.write(app_content)
print("done")
