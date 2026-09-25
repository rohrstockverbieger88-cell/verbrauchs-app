import os
import re

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Update showAdminDashboard to unhide appContainer
old_admin = '''        function showAdminDashboard() {
            closeMobileMenuHack();
            closeMobileMenuObjectHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('inboxView')?.classList.add('hidden');
            document.getElementById('adminDashboardView').classList.remove('hidden');
            loadAdminUsers();
        }'''
new_admin = '''        function showAdminDashboard() {
            closeMobileMenuHack();
            closeMobileMenuObjectHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            
            document.getElementById('objectSelectionView').classList.add('hidden');
            document.getElementById('appContainer').classList.remove('hidden');
            document.getElementById('appContainer').classList.add('flex');
            
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('inboxView')?.classList.add('hidden');
            document.getElementById('adminDashboardView').classList.remove('hidden');
            loadAdminUsers();
        }'''
app_content = app_content.replace(old_admin, new_admin)

# 2. Extract changePasswordModal and move it to the end (before Contact Modal)
# We need to find the exact block.
modal_start_string = '        <!-- Change Password Modal -->\n        <div id="changePasswordModal"'
# Let's use regex to extract it to be safe, up to the closing </div> of the modal.
# Looking at the code, it's 29 lines long, ending with </div>
modal_regex = r'(        <!-- Change Password Modal -->\n        <div id="changePasswordModal"[\s\S]*?</div>\n        </div>\n)'
match = re.search(modal_regex, app_content)

if match:
    modal_content = match.group(1)
    # Remove it from its current position
    app_content = app_content.replace(modal_content, '')
    
    # Insert it before Contact Modal
    contact_modal_marker = '    <!-- Contact Modal -->'
    app_content = app_content.replace(contact_modal_marker, modal_content + '\n' + contact_modal_marker)
else:
    print("Could not find changePasswordModal!")

with open(app_path, "w") as f:
    f.write(app_content)

print("done")
