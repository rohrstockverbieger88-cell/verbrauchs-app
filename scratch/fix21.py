import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Add help text
old_html = """                        <label class="block text-sm font-medium text-gray-400 mb-1">Passwort bestätigen</label>
                        <input type="password" id="regPasswordConfirm" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:ring-1 focus:ring-primary-500 transition-colors">
                    </div>"""
new_html = """                        <label class="block text-sm font-medium text-gray-400 mb-1">Passwort bestätigen</label>
                        <input type="password" id="regPasswordConfirm" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:ring-1 focus:ring-primary-500 transition-colors">
                        <p class="mt-2 text-xs text-gray-500">Mind. 8 Zeichen, 1 Großbuchstabe, 1 Zahl, 1 Sonderzeichen.</p>
                    </div>"""
if old_html in app_content:
    app_content = app_content.replace(old_html, new_html)
else:
    print("Could not find HTML block")

# 2. Add validation logic
old_js = """                    if (pwd !== pwdConfirm) {
                        return showToast("Passwörter stimmen nicht überein!", "error");
                    }
                    if (!privacyChecked) {"""
new_js = """                    const pErr = validatePassword(pwd);
                    if (pErr) return showToast(pErr, "error");
                    
                    if (pwd !== pwdConfirm) {
                        return showToast("Passwörter stimmen nicht überein!", "error");
                    }
                    if (!privacyChecked) {"""
if old_js in app_content:
    app_content = app_content.replace(old_js, new_js)
else:
    print("Could not find JS block")

with open(app_path, "w") as f:
    f.write(app_content)
    
print("done")
