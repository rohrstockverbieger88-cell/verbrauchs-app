import os
import re

# 1. Update app.html
app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

old_html = '''                        <textarea id="replyMessageText" rows="5" class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors resize-none mb-3 text-sm" placeholder="Deine Antwort..."></textarea>
                        <div class="flex justify-end gap-3">'''
new_html = '''                        <textarea id="replyMessageText" rows="5" class="w-full bg-gray-800 border border-gray-700 text-white rounded-lg p-3 outline-none focus:border-primary-500 transition-colors resize-none mb-3 text-sm" placeholder="Deine Antwort..."></textarea>
                        <div class="flex items-center gap-2 mb-3">
                            <input type="checkbox" id="replySendSignature" checked class="w-4 h-4 text-blue-600 bg-gray-800 border-gray-700 rounded focus:ring-blue-500 focus:ring-2 cursor-pointer">
                            <label for="replySendSignature" class="text-sm text-gray-400 cursor-pointer">Signatur anhängen</label>
                        </div>
                        <div class="flex justify-end gap-3">'''
app_content = app_content.replace(old_html, new_html)

old_js = '''            const btn = document.getElementById('sendReplyBtn');
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
                });'''
new_js = '''            const includeSignature = document.getElementById('replySendSignature').checked;
            
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
                        message: text,
                        includeSignature: includeSignature
                    })
                });'''
app_content = app_content.replace(old_js, new_js)

with open(app_path, "w") as f:
    f.write(app_content)

# 2. Update api/reply.js
api_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/api/reply.js"
with open(api_path, "r") as f:
    api_content = f.read()

old_api = '''  const { to, subject, message } = req.body;

  if (!to || !message) {
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
      to: to,
      subject: `RE: ${subject || 'Metraxo Anfrage'}`,
      text: `${message}\\n\\n---\\nViele Grüße,\\nDein Metraxo Team`
    });'''
new_api = '''  const { to, subject, message, includeSignature } = req.body;

  if (!to || !message) {
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
    const finalMessage = includeSignature !== false 
        ? `${message}\\n\\n---\\nViele Grüße,\\nDein Metraxo Team`
        : message;

    await transporter.sendMail({
      from: process.env.GMX_EMAIL,
      to: to,
      subject: `RE: ${subject || 'Metraxo Anfrage'}`,
      text: finalMessage
    });'''
api_content = api_content.replace(old_api, new_api)

with open(api_path, "w") as f:
    f.write(api_content)
print("done")
