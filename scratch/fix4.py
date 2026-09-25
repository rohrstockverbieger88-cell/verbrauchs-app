import os
import re

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Update showInboxView
old_show_inbox = '''        function showInboxView() {
            closeMobileMenuHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.add('hidden');
            document.getElementById('inboxView').classList.remove('hidden');
            loadAdminMessages();
        }'''
new_show_inbox = '''        function showInboxView() {
            closeMobileMenuHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            
            // If called from object selection, switch to appContainer first
            document.getElementById('objectSelectionView').classList.add('hidden');
            document.getElementById('objectSelectionView').classList.remove('flex');
            document.getElementById('appContainer').classList.remove('hidden');
            document.getElementById('appContainer').classList.add('flex');
            
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.add('hidden');
            document.getElementById('inboxView').classList.remove('hidden');
            loadAdminMessages();
        }
        
        function closeInboxView() {
            document.getElementById('inboxView').classList.add('hidden');
            if (currentObjectId) {
                showDashboard();
            } else {
                backToObjects();
            }
        }'''
app_content = app_content.replace(old_show_inbox, new_show_inbox)

# 2. Update the Back button in inboxView
old_back_btn = '''            <div class="flex items-center gap-4 mb-8">
                <button onclick="showDashboard()"'''
new_back_btn = '''            <div class="flex items-center gap-4 mb-8">
                <button onclick="closeInboxView()"'''
app_content = app_content.replace(old_back_btn, new_back_btn)

# 3. Update the admin menu dropdown back button? The adminDashboardView has a back button too.
old_admin_back = '''        function showAdminDashboard() {
            closeMobileMenuHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('inboxView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.remove('hidden');
            loadAdminUsers();
        }'''
new_admin_back = '''        function showAdminDashboard() {
            closeMobileMenuHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            
            document.getElementById('objectSelectionView').classList.add('hidden');
            document.getElementById('objectSelectionView').classList.remove('flex');
            document.getElementById('appContainer').classList.remove('hidden');
            document.getElementById('appContainer').classList.add('flex');
            
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('inboxView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.remove('hidden');
            loadAdminUsers();
        }
        
        function closeAdminDashboard() {
            document.getElementById('adminDashboardView').classList.add('hidden');
            if (currentObjectId) {
                showDashboard();
            } else {
                backToObjects();
            }
        }'''
app_content = app_content.replace(old_admin_back, new_admin_back)

# 4. Update the Back button in adminDashboardView
old_admin_back_html = '''        <div id="adminDashboardView" class="hidden space-y-6 fade-in px-4 py-8 max-w-7xl mx-auto w-full">
            <div class="flex items-center gap-4 mb-8">
                <button onclick="showDashboard()"'''
new_admin_back_html = '''        <div id="adminDashboardView" class="hidden space-y-6 fade-in px-4 py-8 max-w-7xl mx-auto w-full">
            <div class="flex items-center gap-4 mb-8">
                <button onclick="closeAdminDashboard()"'''
app_content = app_content.replace(old_admin_back_html, new_admin_back_html)

with open(app_path, "w") as f:
    f.write(app_content)
print("done")
