import os
import re

app_html = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_html, 'r') as f:
    content = f.read()

# 1. Fix openModal in openMessageReadModal
content = content.replace("openModal('messageReadModal');", "document.getElementById('messageReadModal').classList.remove('hidden'); document.getElementById('messageReadModal').classList.add('flex');")

# 2. Add Bell to objectSelectionView nav
old_nav = '''                    <button onclick="logoutApp()" class="text-sm text-red-400 hover:text-white hover:bg-red-900/50 flex items-center gap-2 px-3 py-2 rounded-lg transition-colors">
                        <i data-lucide="log-out" class="w-4 h-4"></i> Abmelden
                    </button>
                </div>
            </div>
        </nav>'''

new_nav = '''                    <div class="flex items-center gap-2">
                        <!-- Notifications Dropdown (Object View) -->
                        <div class="relative group" id="navActionsObject">
                            <button
                                class="relative flex items-center justify-center w-9 h-9 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
                                title="Benachrichtigungen">
                                <i data-lucide="bell" class="w-4 h-4 text-gray-300"></i>
                                <span id="notificationBadgeObject"
                                    class="hidden absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white ring-2 ring-gray-900">0</span>
                            </button>
                            <div
                                class="absolute right-0 mt-2 w-72 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 overflow-hidden flex flex-col">
                                <div class="px-4 py-3 border-b border-gray-800 bg-gray-800/50 flex justify-between items-center">
                                    <span class="text-sm font-semibold text-white">Benachrichtigungen</span>
                                </div>
                                <div id="notificationListObject" class="flex flex-col max-h-64 overflow-y-auto custom-scrollbar">
                                    <!-- JS Injected -->
                                </div>
                            </div>
                        </div>

                        <button onclick="logoutApp()" class="text-sm text-red-400 hover:text-white hover:bg-red-900/50 flex items-center gap-2 px-3 py-2 rounded-lg transition-colors">
                            <i data-lucide="log-out" class="w-4 h-4"></i> Abmelden
                        </button>
                    </div>
                </div>
            </div>
        </nav>'''

content = content.replace(old_nav, new_nav)

# 3. Update updateNotificationUI to update both bells
old_notif_ui = '''        function updateNotificationUI() {
            const activeNotifs = notifications.filter(n => !n.isResolved);
            const adminCount = window.adminUnreadCount || 0;
            const totalCount = activeNotifs.length + adminCount;
            const badge = document.getElementById('notificationBadge');
            const list = document.getElementById('notificationList');

            if (!badge || !list) return;

            if (totalCount > 0) {
                badge.textContent = totalCount;
                badge.classList.remove('hidden');
                badge.classList.add('flex');
            } else {
                badge.classList.add('hidden');
                badge.classList.remove('flex');
            }

            list.innerHTML = '';
            if (totalCount === 0) {
                list.innerHTML = '<div class="px-4 py-3 text-sm text-gray-400 text-center">Keine neuen Benachrichtigungen</div>';
            } else {
                // Admin Notifications First
                if (adminCount > 0) {
                    const btn = document.createElement('button');
                    btn.className = "w-full text-left px-4 py-3 hover:bg-gray-800 transition flex items-center gap-3 border-b border-gray-800 last:border-0";
                    btn.onclick = () => {
                        document.querySelector('#navActions .group:hover .absolute')?.classList.add('hidden');
                        setTimeout(() => document.querySelector('#navActions .group .absolute')?.classList.remove('hidden'), 500);
                        showInboxView();
                    };
                    btn.innerHTML = `
                        <div class="w-8 h-8 rounded-full bg-blue-500/10 text-blue-500 flex items-center justify-center shrink-0">
                            <i data-lucide="mail" class="w-4 h-4"></i>
                        </div>
                        <div>
                            <div class="text-sm font-medium text-white">Neue Kontaktanfragen</div>
                            <div class="text-xs text-gray-400">Du hast ${adminCount} ungelesene Nachricht(en)</div>
                        </div>
                    `;
                    list.appendChild(btn);
                }

                activeNotifs.forEach(n => {
                    const btn = document.createElement('button');
                    btn.className = "w-full text-left px-4 py-3 hover:bg-gray-800 transition flex items-start gap-3 border-b border-gray-800 last:border-0";
                    btn.onclick = () => {
                        document.querySelector('#navActions .group:hover .absolute')?.classList.add('hidden');
                        setTimeout(() => document.querySelector('#navActions .group .absolute')?.classList.remove('hidden'), 500);
                        
                        const obj = objects.find(o => o.id === n.objectId);
                        if (obj) {
                            openCategory(n.categoryId);
                        }
                    };
                    btn.innerHTML = `
                        <div class="w-8 h-8 rounded-full bg-yellow-500/10 text-yellow-500 flex items-center justify-center shrink-0 mt-0.5">
                            <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                        </div>
                        <div>
                            <div class="text-sm font-medium text-white">Prüfung empfohlen</div>
                            <div class="text-xs text-gray-400 mt-0.5 leading-relaxed">${n.message}</div>
                            <div class="text-[10px] text-gray-500 mt-1 uppercase tracking-wider">${n.objectName} > ${n.categoryName}</div>
                        </div>
                    `;
                    list.appendChild(btn);
                });
            }
            lucide.createIcons();
        }'''

new_notif_ui = '''        function updateNotificationUI() {
            const activeNotifs = notifications.filter(n => !n.isResolved);
            const adminCount = window.adminUnreadCount || 0;
            const totalCount = activeNotifs.length + adminCount;
            
            const badges = [document.getElementById('notificationBadge'), document.getElementById('notificationBadgeObject')];
            const lists = [document.getElementById('notificationList'), document.getElementById('notificationListObject')];

            badges.forEach(badge => {
                if (!badge) return;
                if (totalCount > 0) {
                    badge.textContent = totalCount;
                    badge.classList.remove('hidden');
                    badge.classList.add('flex');
                } else {
                    badge.classList.add('hidden');
                    badge.classList.remove('flex');
                }
            });

            lists.forEach((list, index) => {
                if (!list) return;
                list.innerHTML = '';
                if (totalCount === 0) {
                    list.innerHTML = '<div class="px-4 py-3 text-sm text-gray-400 text-center">Keine neuen Benachrichtigungen</div>';
                } else {
                    if (adminCount > 0) {
                        const btn = document.createElement('button');
                        btn.className = "w-full text-left px-4 py-3 hover:bg-gray-800 transition flex items-center gap-3 border-b border-gray-800 last:border-0";
                        btn.onclick = () => {
                            const parentId = index === 0 ? '#navActions' : '#navActionsObject';
                            document.querySelector(parentId + ' .group:hover .absolute')?.classList.add('hidden');
                            setTimeout(() => document.querySelector(parentId + ' .group .absolute')?.classList.remove('hidden'), 500);
                            showInboxView();
                        };
                        btn.innerHTML = `
                            <div class="w-8 h-8 rounded-full bg-blue-500/10 text-blue-500 flex items-center justify-center shrink-0">
                                <i data-lucide="mail" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="text-sm font-medium text-white">Neue Kontaktanfragen</div>
                                <div class="text-xs text-gray-400">Du hast ${adminCount} ungelesene Nachricht(en)</div>
                            </div>
                        `;
                        list.appendChild(btn);
                    }

                    activeNotifs.forEach(n => {
                        const btn = document.createElement('button');
                        btn.className = "w-full text-left px-4 py-3 hover:bg-gray-800 transition flex items-start gap-3 border-b border-gray-800 last:border-0";
                        btn.onclick = () => {
                            const parentId = index === 0 ? '#navActions' : '#navActionsObject';
                            document.querySelector(parentId + ' .group:hover .absolute')?.classList.add('hidden');
                            setTimeout(() => document.querySelector(parentId + ' .group .absolute')?.classList.remove('hidden'), 500);
                            
                            const obj = objects.find(o => o.id === n.objectId);
                            if (obj) {
                                openCategory(n.categoryId);
                            }
                        };
                        btn.innerHTML = `
                            <div class="w-8 h-8 rounded-full bg-yellow-500/10 text-yellow-500 flex items-center justify-center shrink-0 mt-0.5">
                                <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="text-sm font-medium text-white">Prüfung empfohlen</div>
                                <div class="text-xs text-gray-400 mt-0.5 leading-relaxed">${n.message}</div>
                                <div class="text-[10px] text-gray-500 mt-1 uppercase tracking-wider">${n.objectName} > ${n.categoryName}</div>
                            </div>
                        `;
                        list.appendChild(btn);
                    });
                }
            });
            lucide.createIcons();
        }'''

content = content.replace(old_notif_ui, new_notif_ui)

with open(app_html, 'w') as f:
    f.write(content)
print("done")
