import os
import re

app_html = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_html, 'r') as f:
    content = f.read()

# 1. Add navInboxBtn
nav_admin_str = '''                                    <button onclick="showAdminDashboard()" id="navAdminBtn"
                                        class="hidden w-full text-left px-4 py-3 text-sm text-primary-400 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                        <i data-lucide="users" class="w-4 h-4"></i> Benutzerverwaltung
                                    </button>'''
nav_inbox_str = '''                                    <button onclick="showAdminDashboard()" id="navAdminBtn"
                                        class="hidden w-full text-left px-4 py-3 text-sm text-primary-400 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                        <i data-lucide="users" class="w-4 h-4"></i> Benutzerverwaltung
                                    </button>
                                    <button onclick="showInboxView()" id="navInboxBtn"
                                        class="hidden w-full text-left px-4 py-3 text-sm text-blue-400 hover:text-white hover:bg-gray-700 flex items-center justify-between border-t border-gray-700">
                                        <div class="flex items-center gap-2"><i data-lucide="mail" class="w-4 h-4"></i> Postfach</div>
                                        <span id="inboxMenuBadge" class="hidden bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">0</span>
                                    </button>'''
content = content.replace(nav_admin_str, nav_inbox_str)

# 2. Extract Inbox from Admin Dashboard
old_inbox_start = '            <!-- Messages Inbox -->'
old_inbox_end = '        </div>\n\n        </main>'
inbox_regex = re.compile(re.escape(old_inbox_start) + r'.*?        </div>\n\n        </main>', re.DOTALL)

new_inbox_html = '''        </div>

        <div id="inboxView" class="hidden space-y-6 fade-in px-4 py-8 max-w-7xl mx-auto w-full">
            <div class="flex items-center gap-4 mb-8">
                <button onclick="showDashboard()"
                    class="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
                    title="Zurück">
                    <i data-lucide="arrow-left" class="w-5 h-5"></i>
                </button>
                <h2 class="text-2xl font-bold flex items-center gap-2">
                    <i data-lucide="mail" class="w-6 h-6 text-blue-500"></i> Postfach
                </h2>
            </div>
            <div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden shadow-2xl">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-800 bg-gray-800/50">
                                <th class="p-4 w-12"></th>
                                <th class="p-4">Datum</th>
                                <th class="p-4">Absender</th>
                                <th class="p-4">Betreff</th>
                                <th class="p-4">Aktionen</th>
                            </tr>
                        </thead>
                        <tbody id="adminMessagesList" class="divide-y divide-gray-800 text-sm">
                            <!-- JS Injected Messages -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        </main>'''
content = inbox_regex.sub(new_inbox_html, content)

# 3. Insert Modal
modals_marker = '        <!-- ================== MODALS ================== -->\n\n        <!-- Add Category Modal -->'
new_modal_str = '''        <!-- ================== MODALS ================== -->

        <!-- Message Read Modal -->
        <div id="messageReadModal" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
            <div class="fixed inset-0 bg-gray-950/80 backdrop-blur-sm shadow-sm transition-opacity" onclick="closeModal('messageReadModal')"></div>
            <div class="relative bg-gray-900 border border-gray-700 rounded-xl shadow-2xl w-full max-w-2xl slide-up max-h-[90vh] flex flex-col">
                <div class="p-5 border-b border-gray-800 flex justify-between items-center shrink-0">
                    <h3 class="text-lg font-bold flex items-center gap-2"><i data-lucide="mail-open" class="w-5 h-5 text-blue-500"></i> Nachricht lesen</h3>
                    <button onclick="closeModal('messageReadModal')" class="text-gray-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
                </div>
                <div class="p-5 overflow-y-auto custom-scrollbar flex-1 space-y-6">
                    <div class="grid grid-cols-2 gap-4 text-sm bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                        <div><span class="text-gray-400 block mb-1">Von:</span><span id="readMsgSender" class="text-white font-medium"></span></div>
                        <div><span class="text-gray-400 block mb-1">Datum:</span><span id="readMsgDate" class="text-white font-medium"></span></div>
                        <div class="col-span-2"><span class="text-gray-400 block mb-1">Betreff:</span><span id="readMsgSubject" class="text-white font-medium"></span></div>
                    </div>
                    <div>
                        <span class="text-gray-400 text-sm block mb-2">Nachricht:</span>
                        <div id="readMsgContent" class="text-white text-sm whitespace-pre-wrap bg-gray-800/30 p-4 rounded-lg border border-gray-800 leading-relaxed"></div>
                    </div>
                    
                    <div id="replySection" class="hidden border-t border-gray-800 pt-6 mt-6">
                        <h4 class="text-sm font-semibold text-white mb-3">Antwort schreiben</h4>
                        <textarea id="replyMessageText" rows="5" class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors resize-none mb-3 text-sm" placeholder="Deine Antwort..."></textarea>
                        <div class="flex justify-end gap-3">
                            <button type="button" onclick="document.getElementById('replySection').classList.add('hidden')" class="px-4 py-2 text-sm text-gray-400 hover:text-white transition-colors">Abbrechen</button>
                            <button type="button" id="sendReplyBtn" onclick="sendReply()" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 rounded-lg transition-colors flex items-center gap-2 shadow-lg shadow-blue-500/20">
                                <i data-lucide="send" class="w-4 h-4"></i> Senden
                            </button>
                        </div>
                    </div>
                </div>
                <div class="p-4 border-t border-gray-800 flex justify-end gap-3 shrink-0 bg-gray-900/50 rounded-b-xl">
                    <button type="button" onclick="closeModal('messageReadModal')" class="px-4 py-2 text-sm text-gray-300 hover:text-white bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors">Schließen</button>
                    <button type="button" onclick="document.getElementById('replySection').classList.remove('hidden'); document.getElementById('replyMessageText').focus();" class="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-500 rounded-lg transition-colors flex items-center gap-2 shadow-lg shadow-primary-500/20">
                        <i data-lucide="reply" class="w-4 h-4"></i> Antworten
                    </button>
                </div>
            </div>
        </div>

        <!-- Add Category Modal -->'''
content = content.replace(modals_marker, new_modal_str)

# 4. JS Toggle Logic
old_show_admin = '''        function showAdminDashboard() {
            closeMobileMenuHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.remove('hidden');
            loadAdminUsers();
        }'''
new_show_admin = '''        function showAdminDashboard() {
            closeMobileMenuHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('inboxView')?.classList.add('hidden');
            document.getElementById('adminDashboardView').classList.remove('hidden');
            loadAdminUsers();
        }

        function showInboxView() {
            closeMobileMenuHack();
            if (!isAdmin) return showToast("Keine Berechtigung", "error");
            document.getElementById('dashboardView').classList.add('hidden');
            document.getElementById('detailView').classList.add('hidden');
            document.getElementById('adminDashboardView').classList.add('hidden');
            document.getElementById('inboxView').classList.remove('hidden');
            loadAdminMessages();
        }'''
content = content.replace(old_show_admin, new_show_admin)

# 5. Remove loadAdminMessages from loadAdminUsers
content = content.replace('''            // Load Admin Messages
            loadAdminMessages();''', '')

# 6. Hide inbox and admin in renderView
old_render = '''        function renderView() {
            lucide.createIcons();
            if (activeCategoryId === null) {'''
new_render = '''        function renderView() {
            lucide.createIcons();
            document.getElementById('adminDashboardView')?.classList.add('hidden');
            document.getElementById('inboxView')?.classList.add('hidden');
            
            if (activeCategoryId === null) {'''
content = content.replace(old_render, new_render)

# 7. Unhide navInboxBtn on login
old_login = '''                        document.getElementById('navAdminBtn').classList.remove('hidden');'''
new_login = '''                        document.getElementById('navAdminBtn').classList.remove('hidden');
                        document.getElementById('navInboxBtn')?.classList.remove('hidden');'''
content = content.replace(old_login, new_login)

# 8. LoadAdminMessages update
old_load_msg = '''        async function loadAdminMessages() {
            const list = document.getElementById('adminMessagesList');
            list.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-gray-500">Lade Nachrichten...</td></tr>';
            try {
                const snap = await db.collection('messages').orderBy('timestamp', 'desc').get();
                list.innerHTML = '';
                if (snap.empty) {
                    list.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-gray-500">Keine Nachrichten vorhanden.</td></tr>';
                    return;
                }
                snap.forEach(doc => {
                    const msg = doc.data();
                    const tr = document.createElement('tr');
                    tr.className = `border-b border-gray-800 hover:bg-gray-800/50 transition-colors ${msg.read ? 'opacity-60' : 'font-medium text-white'}`;
                    
                    const dateStr = msg.timestamp ? new Date(msg.timestamp.toDate()).toLocaleString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute:'2-digit' }) : 'Gerade eben';
                    
                    tr.innerHTML = `
                        <td class="py-3 pr-4 whitespace-nowrap text-xs text-gray-400">${dateStr}</td>
                        <td class="py-3 px-4">${msg.email || 'Keine E-Mail'}</td>
                        <td class="py-3 px-4 text-primary-400">${msg.subject || 'Kein Betreff'}</td>
                        <td class="py-3 px-4 text-gray-400 truncate max-w-[200px]">${msg.message}</td>
                        <td class="py-3 pl-4 text-right">
                            ${!msg.read ? `<button onclick="markMessageRead('${doc.id}')" class="p-2 text-green-400 hover:text-white hover:bg-green-500/20 rounded-lg transition-colors" title="Gelesen"><i data-lucide="check" class="w-4 h-4"></i></button>` : ''}
                            <button onclick="deleteMessage('${doc.id}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors ml-1" title="Löschen"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </td>
                    `;
                    list.appendChild(tr);
                });
                lucide.createIcons();
            } catch (err) {
                console.error(err);
                showToast("Fehler beim Laden", "error");
            }
        }'''

new_load_msg = '''        let currentReplyMsgId = null;
        let currentReplyEmail = null;
        let currentReplySubject = null;

        async function loadAdminMessages() {
            const list = document.getElementById('adminMessagesList');
            list.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-gray-500">Lade Nachrichten...</td></tr>';
            try {
                const snap = await db.collection('messages').orderBy('timestamp', 'desc').get();
                list.innerHTML = '';
                if (snap.empty) {
                    list.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-gray-500">Keine Nachrichten vorhanden.</td></tr>';
                    return;
                }
                snap.forEach(doc => {
                    const msg = doc.data();
                    const tr = document.createElement('tr');
                    tr.className = `border-b border-gray-800 hover:bg-gray-800/50 transition-colors cursor-pointer group ${msg.read ? 'text-gray-400' : 'text-white font-bold bg-gray-800/30'}`;
                    
                    const dateStr = msg.timestamp ? new Date(msg.timestamp.toDate()).toLocaleString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute:'2-digit' }) : 'Gerade eben';
                    
                    tr.onclick = (e) => {
                        if (e.target.closest('button')) return; // ignore if button clicked
                        openMessageReadModal(doc.id, msg, dateStr);
                    };

                    tr.innerHTML = `
                        <td class="p-4">
                            <i data-lucide="${msg.read ? 'mail-open' : 'mail'}" class="w-5 h-5 ${msg.read ? 'text-gray-500' : 'text-blue-500'}"></i>
                        </td>
                        <td class="p-4 whitespace-nowrap text-sm ${msg.read ? 'text-gray-500' : 'text-gray-300'}">${dateStr}</td>
                        <td class="p-4">${msg.email || 'Keine E-Mail'}</td>
                        <td class="p-4 ${msg.read ? 'text-gray-400' : 'text-blue-400'}">${msg.subject || 'Kein Betreff'}</td>
                        <td class="p-4 text-right">
                            <button onclick="deleteMessage('${doc.id}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors opacity-0 group-hover:opacity-100" title="Löschen"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </td>
                    `;
                    list.appendChild(tr);
                });
                lucide.createIcons();
            } catch (err) {
                console.error(err);
                showToast("Fehler beim Laden", "error");
            }
        }

        async function openMessageReadModal(id, msg, dateStr) {
            document.getElementById('readMsgSender').textContent = msg.email || 'Unbekannt';
            document.getElementById('readMsgDate').textContent = dateStr;
            document.getElementById('readMsgSubject').textContent = msg.subject || 'Kein Betreff';
            document.getElementById('readMsgContent').textContent = msg.message || '';
            document.getElementById('replySection').classList.add('hidden');
            document.getElementById('replyMessageText').value = '';
            
            currentReplyMsgId = id;
            currentReplyEmail = msg.email;
            currentReplySubject = msg.subject;

            openModal('messageReadModal');

            if (!msg.read) {
                try {
                    await db.collection('messages').doc(id).update({ read: true });
                    // Refresh unread count in background
                    updateUnreadMessagesBadge();
                    // Mark visually read immediately
                    loadAdminMessages();
                } catch(e) {
                    console.error(e);
                }
            }
        }

        async function sendReply() {
            const text = document.getElementById('replyMessageText').value.trim();
            if (!text) return showToast("Bitte einen Text eingeben", "error");
            if (!currentReplyEmail) return showToast("Absender hat keine E-Mail hinterlegt", "error");
            
            const btn = document.getElementById('sendReplyBtn');
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Sende...';
            btn.disabled = true;

            try {
                const res = await fetch('/api/reply', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        to: currentReplyEmail,
                        subject: currentReplySubject,
                        message: text
                    })
                });

                const data = await res.json();
                if (data.success) {
                    showToast("Antwort erfolgreich gesendet!", "success");
                    closeModal('messageReadModal');
                } else {
                    showToast("Fehler beim Senden: " + data.error, "error");
                }
            } catch (err) {
                console.error(err);
                showToast("Fehler beim Server-Verbindungsaufbau", "error");
            } finally {
                btn.innerHTML = originalHtml;
                btn.disabled = false;
                lucide.createIcons();
            }
        }'''
content = content.replace(old_load_msg, new_load_msg)

# 9. Update notification badge routing
old_notif_ui = '''                        showAdminDashboard();'''
new_notif_ui = '''                        showInboxView();'''
content = content.replace(old_notif_ui, new_notif_ui)

# 10. Update badge number on navInboxBtn
old_badge_func = '''                        if (!badge) {
                            badge = document.createElement('span');
                            badge.id = 'adminUnreadBadge';
                            badge.className = 'ml-auto bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full';
                            document.getElementById('navAdminBtn').appendChild(badge);
                        }'''
new_badge_func = '''                        if (!badge) {
                            badge = document.createElement('span');
                            badge.id = 'adminUnreadBadge';
                            badge.className = 'hidden';
                            // no longer inject into navAdminBtn, we use inboxMenuBadge directly
                            document.body.appendChild(badge);
                        }'''
content = content.replace(old_badge_func, new_badge_func)

old_badge_update = '''                        badge.textContent = snap.size;
                        window.adminUnreadCount = snap.size;
                    } else {
                        if (badge) badge.remove();
                        window.adminUnreadCount = 0;
                    }'''
new_badge_update = '''                        badge.textContent = snap.size;
                        window.adminUnreadCount = snap.size;
                        const mBadge = document.getElementById('inboxMenuBadge');
                        if (mBadge) { mBadge.textContent = snap.size; mBadge.classList.remove('hidden'); }
                    } else {
                        if (badge) badge.remove();
                        window.adminUnreadCount = 0;
                        const mBadge = document.getElementById('inboxMenuBadge');
                        if (mBadge) { mBadge.classList.add('hidden'); }
                    }'''
content = content.replace(old_badge_update, new_badge_update)

with open(app_html, 'w') as f:
    f.write(content)
print("done")
