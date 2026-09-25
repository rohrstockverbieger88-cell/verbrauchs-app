import os
import re

# 1. Update index.html
index_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/index.html"
with open(index_path, "r") as f:
    idx_content = f.read()

idx_form_old = '''                    <div>
                        <label class="block text-sm font-medium text-slate-400 mb-1">Deine E-Mail</label>
                        <input type="email" id="contactEmail" required class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="name@beispiel.de">
                    </div>'''
idx_form_new = '''                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-400 mb-1">Vorname</label>
                            <input type="text" id="contactFirstName" required class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="Max">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-400 mb-1">Nachname</label>
                            <input type="text" id="contactLastName" required class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="Mustermann">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-400 mb-1">Deine E-Mail</label>
                        <input type="email" id="contactEmail" required class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="name@beispiel.de">
                    </div>'''
idx_content = idx_content.replace(idx_form_old, idx_form_new)

idx_send_old = '''            const email = document.getElementById('contactEmail').value;
            const subjectSelect = document.getElementById('contactSubject').value;
            const customSubject = document.getElementById('customContactSubject').value;
            const message = document.getElementById('contactMessage').value;

            const finalSubject = subjectSelect === 'Anderes' ? customSubject : subjectSelect;

            try {
                // 1. Send via Vercel Backend (Email)
                fetch('/api/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, subject: finalSubject, message })
                }).catch(e => console.error("API Error:", e));

                // 2. Save to Firestore (Admin Inbox)
                await db.collection('messages').add({
                    email: email,
                    subject: finalSubject,
                    message: message,
                    timestamp: firebase.firestore.FieldValue.serverTimestamp(),
                    read: false
                });'''
idx_send_new = '''            const firstName = document.getElementById('contactFirstName').value;
            const lastName = document.getElementById('contactLastName').value;
            const email = document.getElementById('contactEmail').value;
            const subjectSelect = document.getElementById('contactSubject').value;
            const customSubject = document.getElementById('customContactSubject').value;
            const message = document.getElementById('contactMessage').value;

            const finalSubject = subjectSelect === 'Anderes' ? customSubject : subjectSelect;

            try {
                // 1. Send via Vercel Backend (Email)
                fetch('/api/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ firstName, lastName, email, subject: finalSubject, message })
                }).catch(e => console.error("API Error:", e));

                // 2. Save to Firestore (Admin Inbox)
                await db.collection('messages').add({
                    firstName: firstName,
                    lastName: lastName,
                    email: email,
                    subject: finalSubject,
                    message: message,
                    timestamp: firebase.firestore.FieldValue.serverTimestamp(),
                    read: false
                });'''
idx_content = idx_content.replace(idx_send_old, idx_send_new)

with open(index_path, "w") as f:
    f.write(idx_content)

# 2. Update app.html
app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

app_form_old = '''                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Deine E-Mail</label>
                        <input type="email" id="contactEmail" required class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="name@beispiel.de">
                    </div>'''
app_form_new = '''                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-1">Vorname</label>
                            <input type="text" id="contactFirstName" required class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="Max">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-1">Nachname</label>
                            <input type="text" id="contactLastName" required class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="Mustermann">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Deine E-Mail</label>
                        <input type="email" id="contactEmail" required class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors" placeholder="name@beispiel.de">
                    </div>'''
app_content = app_content.replace(app_form_old, app_form_new)

app_send_old = '''            const email = document.getElementById('contactEmail').value;
            const subjectSelect = document.getElementById('contactSubject').value;
            const customSubject = document.getElementById('customContactSubject').value;
            const message = document.getElementById('contactMessage').value;

            const finalSubject = subjectSelect === 'Anderes' ? customSubject : subjectSelect;

            try {
                // 1. Send via Vercel Backend (Email)
                fetch('/api/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, subject: finalSubject, message })
                }).catch(e => console.error("API Error:", e));

                // 2. Save to Firestore (Admin Inbox)
                await db.collection('messages').add({
                    email: email,
                    subject: finalSubject,
                    message: message,
                    timestamp: firebase.firestore.FieldValue.serverTimestamp(),
                    read: false
                });'''
app_send_new = '''            const firstName = document.getElementById('contactFirstName').value;
            const lastName = document.getElementById('contactLastName').value;
            const email = document.getElementById('contactEmail').value;
            const subjectSelect = document.getElementById('contactSubject').value;
            const customSubject = document.getElementById('customContactSubject').value;
            const message = document.getElementById('contactMessage').value;

            const finalSubject = subjectSelect === 'Anderes' ? customSubject : subjectSelect;

            try {
                // 1. Send via Vercel Backend (Email)
                fetch('/api/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ firstName, lastName, email, subject: finalSubject, message })
                }).catch(e => console.error("API Error:", e));

                // 2. Save to Firestore (Admin Inbox)
                await db.collection('messages').add({
                    firstName: firstName,
                    lastName: lastName,
                    email: email,
                    subject: finalSubject,
                    message: message,
                    timestamp: firebase.firestore.FieldValue.serverTimestamp(),
                    read: false
                });'''
app_content = app_content.replace(app_send_old, app_send_new)

app_table_old = '''                <div class="overflow-x-auto">
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
                </div>'''
app_table_new = '''                <div class="w-full">
                    <div class="hidden sm:grid grid-cols-12 gap-4 text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-800 bg-gray-800/50 p-4">
                        <div class="col-span-1"></div>
                        <div class="col-span-2">Datum</div>
                        <div class="col-span-3">Name</div>
                        <div class="col-span-3">E-Mail</div>
                        <div class="col-span-2">Betreff</div>
                        <div class="col-span-1 text-right">Aktionen</div>
                    </div>
                    <div id="adminMessagesList" class="divide-y divide-gray-800 text-sm flex flex-col">
                        <!-- JS Injected Messages -->
                    </div>
                </div>'''
app_content = app_content.replace(app_table_old, app_table_new)

app_load_msg_old = '''                if (snap.empty) {
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
                        <td class="p-4 ${msg.read ? 'text-gray-400' : 'text-blue-400'}">
                            ${msg.subject || 'Kein Betreff'}
                            ${msg.replyText ? '<br><span class="text-[10px] text-green-400 mt-1 inline-flex items-center gap-1"><i data-lucide="reply" class="w-3 h-3"></i> Beantwortet</span>' : ''}
                        </td>
                        <td class="p-4 text-right">
                            <button onclick="deleteMessage('${doc.id}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors opacity-0 group-hover:opacity-100" title="Löschen"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </td>
                    `;
                    list.appendChild(tr);
                });'''
app_load_msg_new = '''                if (snap.empty) {
                    list.innerHTML = '<div class="p-4 text-center text-gray-500 w-full">Keine Nachrichten vorhanden.</div>';
                    return;
                }
                snap.forEach(doc => {
                    const msg = doc.data();
                    const div = document.createElement('div');
                    div.className = `grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 p-4 border-b border-gray-800 hover:bg-gray-800/50 transition-colors cursor-pointer group relative items-start sm:items-center ${msg.read ? 'text-gray-400' : 'text-white font-bold bg-gray-800/30'}`;
                    
                    const dateStr = msg.timestamp ? new Date(msg.timestamp.toDate()).toLocaleString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute:'2-digit' }) : 'Gerade eben';
                    
                    div.onclick = (e) => {
                        if (e.target.closest('button')) return;
                        openMessageReadModal(doc.id, msg, dateStr);
                    };

                    const fullName = (msg.firstName && msg.lastName) ? `${msg.firstName} ${msg.lastName}` : (msg.firstName || msg.lastName || 'Unbekannt');

                    div.innerHTML = `
                        <!-- Mobile View Wrapper for top row -->
                        <div class="flex items-center justify-between w-full sm:col-span-1 sm:w-auto mb-2 sm:mb-0">
                            <i data-lucide="${msg.read ? 'mail-open' : 'mail'}" class="w-5 h-5 ${msg.read ? 'text-gray-500' : 'text-blue-500'}"></i>
                            <div class="sm:hidden text-xs ${msg.read ? 'text-gray-500' : 'text-gray-400'}">${dateStr}</div>
                        </div>
                        
                        <div class="hidden sm:block sm:col-span-2 text-xs ${msg.read ? 'text-gray-500' : 'text-gray-300'}">${dateStr}</div>
                        
                        <div class="w-full sm:col-span-3 mb-1 sm:mb-0">
                            <div class="font-medium ${msg.read ? 'text-gray-400' : 'text-white'}">${fullName}</div>
                            <div class="sm:hidden text-xs text-gray-500 mt-0.5 break-all">${msg.email || 'Keine E-Mail'}</div>
                        </div>
                        
                        <div class="hidden sm:block sm:col-span-3 text-gray-400 truncate">${msg.email || 'Keine E-Mail'}</div>
                        
                        <div class="w-full sm:col-span-2 ${msg.read ? 'text-gray-400' : 'text-blue-400'} truncate pr-8 sm:pr-0">
                            ${msg.subject || 'Kein Betreff'}
                            ${msg.replyText ? '<br><span class="text-[10px] text-green-400 mt-1 inline-flex items-center gap-1"><i data-lucide="reply" class="w-3 h-3"></i> Beantwortet</span>' : ''}
                        </div>
                        
                        <div class="absolute right-4 bottom-4 sm:relative sm:right-0 sm:bottom-0 sm:col-span-1 text-right mt-2 sm:mt-0">
                            <button onclick="deleteMessage('${doc.id}')" class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition-colors opacity-100 sm:opacity-0 group-hover:opacity-100 bg-gray-900/80 sm:bg-transparent" title="Löschen"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </div>
                    `;
                    list.appendChild(div);
                });'''
app_content = app_content.replace(app_load_msg_old, app_load_msg_new)

app_err_old = '''            } catch (err) {
                console.error("Error loading messages:", err);
                list.innerHTML = '<tr><td colspan="5" class="p-4 text-center text-red-400">Fehler beim Laden. (Fehlen Datenbank-Regeln?)</td></tr>';
            }'''
app_err_new = '''            } catch (err) {
                console.error("Error loading messages:", err);
                list.innerHTML = '<div class="p-4 text-center text-red-400 w-full">Fehler beim Laden. (Fehlen Datenbank-Regeln?)</div>';
            }'''
app_content = app_content.replace(app_err_old, app_err_new)

app_modal_read_old = '''        async function openMessageReadModal(id, msg, dateStr) {
            document.getElementById('readMsgSender').textContent = msg.email || 'Unbekannt';'''
app_modal_read_new = '''        async function openMessageReadModal(id, msg, dateStr) {
            const fullName = (msg.firstName && msg.lastName) ? `${msg.firstName} ${msg.lastName}` : (msg.firstName || msg.lastName || 'Unbekannt');
            document.getElementById('readMsgSender').textContent = `${fullName} (${msg.email || 'Keine E-Mail'})`;'''
app_content = app_content.replace(app_modal_read_old, app_modal_read_new)

with open(app_path, "w") as f:
    f.write(app_content)

# 3. Update api/contact.js
api_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/api/contact.js"
with open(api_path, "r") as f:
    api_content = f.read()

api_old = '''  const { email, subject, message } = req.body;

  if (!email || !message) {
    return res.status(400).json({ message: 'Missing fields' });
  }

  const transporter = nodemailer.createTransport({
    host: 'mail.gmx.net',
    port: 465,
    secure: true,
    auth: {
      user: process.env.GMX_EMAIL,
      pass: process.env.GMX_PASSWORD
    }
  });

  try {
    await transporter.sendMail({
      from: process.env.GMX_EMAIL,
      to: process.env.GMX_EMAIL,
      replyTo: email,
      subject: `Metraxo Kontakt: ${subject}`,
      text: `Neue Nachricht über das Metraxo Kontaktformular:\\n\\nAbsender: ${email}\\nBetreff: ${subject}\\n\\nNachricht:\\n${message}`
    });'''
api_new = '''  const { firstName, lastName, email, subject, message } = req.body;

  if (!email || !message) {
    return res.status(400).json({ message: 'Missing fields' });
  }

  const transporter = nodemailer.createTransport({
    host: 'mail.gmx.net',
    port: 465,
    secure: true,
    auth: {
      user: process.env.GMX_EMAIL,
      pass: process.env.GMX_PASSWORD
    }
  });

  try {
    const fullName = (firstName && lastName) ? `${firstName} ${lastName}` : (firstName || lastName || 'Unbekannt');
    await transporter.sendMail({
      from: process.env.GMX_EMAIL,
      to: process.env.GMX_EMAIL,
      replyTo: email,
      subject: `Metraxo Kontakt: ${subject}`,
      text: `Neue Nachricht über das Metraxo Kontaktformular:\\n\\nAbsender: ${fullName} (${email})\\nBetreff: ${subject}\\n\\nNachricht:\\n${message}`
    });'''
api_content = api_content.replace(api_old, api_new)

with open(api_path, "w") as f:
    f.write(api_content)
print("done")
