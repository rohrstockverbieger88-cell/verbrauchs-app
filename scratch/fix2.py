import os

# 1. Update api/reply.js
api_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/api/reply.js"
with open(api_path, "r") as f:
    api_content = f.read()

old_text = "text: message"
new_text = "text: `${message}\\n\\n---\\nViele Grüße,\\nDein Metraxo Team`"
api_content = api_content.replace(old_text, new_text)

with open(api_path, "w") as f:
    f.write(api_content)

# 2. Update app.html
app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 2a. Fix updateNotificationUI
old_notif_ui = '''                activeNotifs.forEach(n => {
                    const cat = categories.find(c => c.id === n.categoryId);
                    if (!cat) return;

                    const btn = document.createElement('button');
                    btn.className = "w-full text-left px-4 py-3 hover:bg-gray-800 transition flex items-center gap-3 border-b border-gray-800 last:border-0";
                    btn.onclick = () => {
                        openCategory(cat.id);
                        openAddReadingModal();
                    };

                    btn.innerHTML = `
                        <div class="w-8 h-8 rounded-full bg-${getStyleClasses(cat.color).text.split('-')[1]}-500/10 ${getStyleClasses(cat.color).text} flex items-center justify-center shrink-0">
                            <i data-lucide="bell-ring" class="w-4 h-4"></i>
                        </div>
                        <div>
                            <div class="text-sm font-medium text-white">Zählerstand fällig</div>
                            <div class="text-xs text-gray-400">${cat.name} (${monthNames[n.month]} ${n.year}) eintragen</div>
                        </div>
                    `;
                    list.appendChild(btn);
                });
            }
            lucide.createIcons();
        }'''

new_notif_ui = '''                activeNotifs.forEach(n => {
                    const cat = categories.find(c => c.id === n.categoryId);
                    if (!cat) return;

                    const btn = document.createElement('button');
                    btn.className = "w-full text-left px-4 py-3 hover:bg-gray-800 transition flex items-center gap-3 border-b border-gray-800 last:border-0";
                    btn.onclick = () => {
                        openCategory(cat.id);
                        openAddReadingModal();
                    };

                    btn.innerHTML = `
                        <div class="w-8 h-8 rounded-full bg-${getStyleClasses(cat.color).text.split('-')[1]}-500/10 ${getStyleClasses(cat.color).text} flex items-center justify-center shrink-0">
                            <i data-lucide="bell-ring" class="w-4 h-4"></i>
                        </div>
                        <div>
                            <div class="text-sm font-medium text-white">Zählerstand fällig</div>
                            <div class="text-xs text-gray-400">${cat.name} (${monthNames[n.month]} ${n.year}) eintragen</div>
                        </div>
                    `;
                    list.appendChild(btn);
                });
            }
            lucide.createIcons();
        }'''

# Wait, `updateNotificationUI` in app.html was not completely replaced because I used the wrong target string.
# I will just regex replace the entire updateNotificationUI function block.
import re
app_content = re.sub(
    r'function updateNotificationUI\(\) \{.*?\n        \}',
    '''function updateNotificationUI() {
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

            const monthNames = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];

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
                        const cat = categories.find(c => c.id === n.categoryId);
                        if (!cat) return;

                        const btn = document.createElement('button');
                        btn.className = "w-full text-left px-4 py-3 hover:bg-gray-800 transition flex items-center gap-3 border-b border-gray-800 last:border-0";
                        btn.onclick = () => {
                            const parentId = index === 0 ? '#navActions' : '#navActionsObject';
                            document.querySelector(parentId + ' .group:hover .absolute')?.classList.add('hidden');
                            setTimeout(() => document.querySelector(parentId + ' .group .absolute')?.classList.remove('hidden'), 500);
                            
                            openCategory(cat.id);
                            openAddReadingModal();
                        };
                        const colorParts = getStyleClasses(cat.color).text.split('-');
                        const colorName = colorParts.length > 1 ? colorParts[1] : 'blue';
                        btn.innerHTML = `
                            <div class="w-8 h-8 rounded-full bg-${colorName}-500/10 ${getStyleClasses(cat.color).text} flex items-center justify-center shrink-0">
                                <i data-lucide="bell-ring" class="w-4 h-4"></i>
                            </div>
                            <div>
                                <div class="text-sm font-medium text-white">Zählerstand fällig</div>
                                <div class="text-xs text-gray-400">${cat.name} (${monthNames[n.month]} ${n.year}) eintragen</div>
                            </div>
                        `;
                        list.appendChild(btn);
                    });
                }
            });
            lucide.createIcons();
        }''',
    app_content,
    flags=re.DOTALL
)

# 2b. Add reply text UI in modal
modal_html_old = '''                    <div>
                        <span class="text-gray-400 text-sm block mb-2">Nachricht:</span>
                        <div id="readMsgContent" class="text-white text-sm whitespace-pre-wrap bg-gray-800/30 p-4 rounded-lg border border-gray-800 leading-relaxed"></div>
                    </div>
                    
                    <div id="replySection" class="hidden border-t border-gray-800 pt-6 mt-6">'''
modal_html_new = '''                    <div>
                        <span class="text-gray-400 text-sm block mb-2">Nachricht:</span>
                        <div id="readMsgContent" class="text-white text-sm whitespace-pre-wrap bg-gray-800/30 p-4 rounded-lg border border-gray-800 leading-relaxed"></div>
                    </div>

                    <div id="previousReplyContainer" class="hidden mt-4">
                        <span class="text-green-400 text-sm block mb-2 font-medium">Deine Antwort:</span>
                        <div id="readMsgReply" class="text-white text-sm whitespace-pre-wrap bg-gray-800/50 p-4 rounded-lg border border-green-500/30 leading-relaxed"></div>
                    </div>
                    
                    <div id="replySection" class="hidden border-t border-gray-800 pt-6 mt-6">'''
app_content = app_content.replace(modal_html_old, modal_html_new)

# 2c. loadAdminMessages row injection update to show if replied
row_injection_old = '''                        <td class="p-4 ${msg.read ? 'text-gray-400' : 'text-blue-400'}">${msg.subject || 'Kein Betreff'}</td>
                        <td class="p-4 text-right">
                            <button onclick="deleteMessage('${doc.id}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors opacity-0 group-hover:opacity-100" title="Löschen"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </td>'''
row_injection_new = '''                        <td class="p-4 ${msg.read ? 'text-gray-400' : 'text-blue-400'}">
                            ${msg.subject || 'Kein Betreff'}
                            ${msg.replyText ? '<br><span class="text-[10px] text-green-400 mt-1 inline-flex items-center gap-1"><i data-lucide="reply" class="w-3 h-3"></i> Beantwortet</span>' : ''}
                        </td>
                        <td class="p-4 text-right">
                            <button onclick="deleteMessage('${doc.id}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors opacity-0 group-hover:opacity-100" title="Löschen"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </td>'''
app_content = app_content.replace(row_injection_old, row_injection_new)

# 2d. openMessageReadModal update to show previous reply
read_modal_old = '''            document.getElementById('readMsgContent').textContent = msg.message || '';
            document.getElementById('replySection').classList.add('hidden');
            document.getElementById('replyMessageText').value = '';'''
read_modal_new = '''            document.getElementById('readMsgContent').textContent = msg.message || '';
            document.getElementById('replySection').classList.add('hidden');
            document.getElementById('replyMessageText').value = '';
            
            if (msg.replyText) {
                document.getElementById('previousReplyContainer').classList.remove('hidden');
                document.getElementById('readMsgReply').textContent = msg.replyText;
            } else {
                document.getElementById('previousReplyContainer').classList.add('hidden');
            }'''
app_content = app_content.replace(read_modal_old, read_modal_new)

# 2e. sendReply update to save to firestore
send_reply_old = '''                if (data.success) {
                    showToast("Antwort erfolgreich gesendet!", "success");
                    closeModal('messageReadModal');
                } else {'''
send_reply_new = '''                if (data.success) {
                    try {
                        await db.collection('messages').doc(currentReplyMsgId).update({
                            replyText: text,
                            repliedAt: firebase.firestore.FieldValue.serverTimestamp()
                        });
                        loadAdminMessages();
                    } catch(e) {
                        console.error('Failed to save reply', e);
                    }
                    showToast("Antwort erfolgreich gesendet!", "success");
                    closeModal('messageReadModal');
                } else {'''
app_content = app_content.replace(send_reply_old, send_reply_new)

with open(app_path, "w") as f:
    f.write(app_content)
print("done")
