import os
import re

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Add toggleUserRole function
js_to_insert = '''        async function toggleUserRole(userId, currentRole) {
            const newRole = currentRole === 'admin' ? 'user' : 'admin';
            if (!confirm(`Soll dieser Benutzer wirklich zum ${newRole.toUpperCase()} gemacht werden?`)) return;
            try {
                await db.collection('users').doc(userId).update({
                    role: newRole
                });
                showToast(`Benutzer ist nun ${newRole.toUpperCase()}.`, "success");
                loadAdminUsers();
            } catch (err) {
                console.error("Fehler beim Ändern der Rechte:", err);
                showToast("Fehler beim Ändern der Rechte.", "error");
            }
        }
'''
# I will insert it before async function loadAdminUsers()
app_content = app_content.replace('        async function loadAdminUsers() {', js_to_insert + '        async function loadAdminUsers() {')

# 2. Add the button in loadAdminUsers()
old_buttons = '''                            ${doc.id !== firebase.auth().currentUser.uid ? `
                                <button onclick="resetUserPassword('${doc.id}', '${u.email}')" class="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors" title="Passwort-Reset E-Mail senden"><i data-lucide="mail" class="w-4 h-4"></i></button>
                                <button onclick="deleteUserAccount('${doc.id}', '${u.email}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors ml-1" title="Benutzer löschen"><i data-lucide="user-x" class="w-4 h-4"></i></button>
                            ` : ''}'''
new_buttons = '''                            ${doc.id !== firebase.auth().currentUser.uid ? `
                                <button onclick="toggleUserRole('${doc.id}', '${u.role}')" class="p-2 text-${u.role === 'admin' ? 'orange' : 'blue'}-400 hover:text-white hover:bg-${u.role === 'admin' ? 'orange' : 'blue'}-500/20 rounded-lg transition-colors" title="${u.role === 'admin' ? 'Admin-Rechte entziehen' : 'Zum Admin machen'}"><i data-lucide="${u.role === 'admin' ? 'shield-minus' : 'shield-check'}" class="w-4 h-4"></i></button>
                                <button onclick="resetUserPassword('${doc.id}', '${u.email}')" class="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors ml-1" title="Passwort-Reset E-Mail senden"><i data-lucide="mail" class="w-4 h-4"></i></button>
                                <button onclick="deleteUserAccount('${doc.id}', '${u.email}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors ml-1" title="Benutzer löschen"><i data-lucide="user-x" class="w-4 h-4"></i></button>
                            ` : ''}'''
app_content = app_content.replace(old_buttons, new_buttons)

with open(app_path, "w") as f:
    f.write(app_content)
print("done")
