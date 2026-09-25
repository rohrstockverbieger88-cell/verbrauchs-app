import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Add dropdown HTML to objectSelectionView
old_html = '''                        <!-- Notifications Dropdown (Object View) -->
                        <div class="relative group" id="navActionsObject">
                            <button
                                class="relative flex items-center justify-center w-9 h-9 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
                                title="Benachrichtigungen">'''
new_html = '''                        <!-- Options Dropdown (Object View) -->
                        <div class="relative">
                            <button id="menuToggleButtonObject" onclick="toggleMenuObject()"
                                class="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors text-sm font-medium"
                                title="Optionen">
                                <i data-lucide="menu" class="w-4 h-4"></i><span
                                    class="hidden sm:inline">Optionen</span>
                            </button>
                            <div id="mobileMenuDropdownObject"
                                class="absolute right-0 mt-2 w-48 bg-gray-800 border border-gray-700 rounded-lg shadow-xl opacity-0 invisible transition-all z-50 overflow-hidden">
                                <button onclick="closeMobileMenuObjectHack(); openChangePasswordModal()"
                                    class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2">
                                    <i data-lucide="key" class="w-4 h-4"></i> Passwort ändern
                                </button>
                                <a href="faq.html"
                                    class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="help-circle" class="w-4 h-4"></i> Hilfe
                                </a>
                                <button onclick="showAdminDashboard()" id="navAdminBtnObject"
                                    class="hidden w-full text-left px-4 py-3 text-sm text-primary-400 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="users" class="w-4 h-4"></i> Benutzerverwaltung
                                </button>
                                <button onclick="showInboxView()" id="navInboxBtnObject"
                                    class="hidden w-full text-left px-4 py-3 text-sm text-blue-400 hover:text-white hover:bg-gray-700 flex items-center justify-between border-t border-gray-700">
                                    <div class="flex items-center gap-2"><i data-lucide="mail" class="w-4 h-4"></i> Postfach</div>
                                    <span id="inboxMenuBadgeObject" class="hidden bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">0</span>
                                </button>
                                <button onclick="closeMobileMenuObjectHack(); openContactModal('Verbesserung')"
                                    class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="message-square" class="w-4 h-4"></i> Verbesserung
                                </button>
                            </div>
                        </div>
                        
                        <!-- Notifications Dropdown (Object View) -->
                        <div class="relative group" id="navActionsObject">
                            <button
                                class="relative flex items-center justify-center w-9 h-9 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
                                title="Benachrichtigungen">'''
app_content = app_content.replace(old_html, new_html)

# 2. Add javascript logic for menu toggle
js_insert = '''
        function toggleMenuObject() {
            const menu = document.getElementById('mobileMenuDropdownObject');
            if (menu.classList.contains('opacity-0')) {
                menu.classList.remove('opacity-0', 'invisible');
                menu.classList.add('opacity-100', 'visible');
            } else {
                closeMobileMenuObjectHack();
            }
        }
        function closeMobileMenuObjectHack() {
            const menu = document.getElementById('mobileMenuDropdownObject');
            if (menu) {
                menu.classList.add('opacity-0', 'invisible');
                menu.classList.remove('opacity-100', 'visible');
            }
        }
'''
app_content = app_content.replace('        function closeMobileMenuHack() {', js_insert + '        function closeMobileMenuHack() {')

# 3. Add to showAdminDashboard/showInboxView hide
old_close = 'closeMobileMenuHack();'
new_close = 'closeMobileMenuHack();\n            closeMobileMenuObjectHack();'
app_content = app_content.replace('        function showInboxView() {\n            closeMobileMenuHack();', '        function showInboxView() {\n            closeMobileMenuHack();\n            closeMobileMenuObjectHack();')
app_content = app_content.replace('        function showAdminDashboard() {\n            closeMobileMenuHack();', '        function showAdminDashboard() {\n            closeMobileMenuHack();\n            closeMobileMenuObjectHack();')

# 4. Admin buttons toggle
old_auth = '''                    if (role === 'admin') {
                        isAdmin = true;
                        document.getElementById('navAdminBtn').classList.remove('hidden');
                        document.getElementById('navInboxBtn')?.classList.remove('hidden');
                        updateUnreadMessagesBadge();
                    } else {
                        isAdmin = false;
                        document.getElementById('navAdminBtn').classList.add('hidden');
                    }'''
new_auth = '''                    if (role === 'admin') {
                        isAdmin = true;
                        document.getElementById('navAdminBtn').classList.remove('hidden');
                        document.getElementById('navInboxBtn')?.classList.remove('hidden');
                        if(document.getElementById('navAdminBtnObject')) document.getElementById('navAdminBtnObject').classList.remove('hidden');
                        if(document.getElementById('navInboxBtnObject')) document.getElementById('navInboxBtnObject').classList.remove('hidden');
                        updateUnreadMessagesBadge();
                    } else {
                        isAdmin = false;
                        document.getElementById('navAdminBtn').classList.add('hidden');
                        document.getElementById('navInboxBtn')?.classList.add('hidden');
                        if(document.getElementById('navAdminBtnObject')) document.getElementById('navAdminBtnObject').classList.add('hidden');
                        if(document.getElementById('navInboxBtnObject')) document.getElementById('navInboxBtnObject').classList.add('hidden');
                    }'''
app_content = app_content.replace(old_auth, new_auth)

# 5. Badges
old_badge = '''                const b = document.getElementById('inboxMenuBadge');
                if (b) {
                    b.textContent = window.adminUnreadCount;
                    b.classList.remove('hidden');
                }'''
new_badge = '''                const b = document.getElementById('inboxMenuBadge');
                if (b) {
                    b.textContent = window.adminUnreadCount;
                    b.classList.remove('hidden');
                }
                const b2 = document.getElementById('inboxMenuBadgeObject');
                if (b2) {
                    b2.textContent = window.adminUnreadCount;
                    b2.classList.remove('hidden');
                }'''
app_content = app_content.replace(old_badge, new_badge)

old_badge_hide = '''                const b = document.getElementById('inboxMenuBadge');
                if (b) b.classList.add('hidden');'''
new_badge_hide = '''                const b = document.getElementById('inboxMenuBadge');
                if (b) b.classList.add('hidden');
                const b2 = document.getElementById('inboxMenuBadgeObject');
                if (b2) b2.classList.add('hidden');'''
app_content = app_content.replace(old_badge_hide, new_badge_hide)

with open(app_path, "w") as f:
    f.write(app_content)
print("done")
