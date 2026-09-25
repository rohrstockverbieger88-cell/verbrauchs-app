import os
import re

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Inject validatePassword function and auth.languageCode = 'de';
auth_init = "const auth = firebase.auth();"
auth_replacement = """const auth = firebase.auth();
        auth.languageCode = 'de';

        function validatePassword(password) {
            if (password.length < 8) return "Das Passwort muss mindestens 8 Zeichen lang sein.";
            if (!/[A-Z]/.test(password)) return "Das Passwort muss mindestens einen Großbuchstaben enthalten.";
            if (!/[a-z]/.test(password)) return "Das Passwort muss mindestens einen Kleinbuchstaben enthalten.";
            if (!/[0-9]/.test(password)) return "Das Passwort muss mindestens eine Zahl enthalten.";
            if (!/[^A-Za-z0-9]/.test(password)) return "Das Passwort muss mindestens ein Sonderzeichen enthalten.";
            return null;
        }"""
app_content = app_content.replace(auth_init, auth_replacement, 1)

# 2. Add validation to changePasswordForm
old_cp = """                    if (p1 !== p2) return showToast("Passwörter stimmen nicht überein!", "error");

                    if (auth.currentUser) {"""
new_cp = """                    if (p1 !== p2) return showToast("Passwörter stimmen nicht überein!", "error");
                    
                    const pErr = validatePassword(p1);
                    if (pErr) return showToast(pErr, "error");

                    if (auth.currentUser) {"""
app_content = app_content.replace(old_cp, new_cp)

# 3. Add validation to createUserForm
old_cu = """                    const pwd = document.getElementById('newUserInputPassword').value;

                    try {"""
new_cu = """                    const pwd = document.getElementById('newUserInputPassword').value;

                    const pErr = validatePassword(pwd);
                    if (pErr) return showToast(pErr, "error");

                    try {"""
app_content = app_content.replace(old_cu, new_cu)

# 4. Insert resetPasswordModal HTML
# Let's put it right before "<!-- Contact Modal -->" which is at the end of the body
modal_html = """
        <!-- Reset Password Modal -->
        <div id="resetPasswordModal" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
            <div class="fixed inset-0 bg-gray-950/90 backdrop-blur-md transition-opacity"></div>
            <div class="relative bg-gray-900 border border-gray-700 rounded-xl shadow-2xl w-full max-w-sm slide-up p-5">
                <div class="flex justify-between items-center border-b border-gray-800 pb-3 mb-4">
                    <h3 class="text-lg font-bold flex items-center gap-2"><i data-lucide="key" class="w-5 h-5 text-primary-400"></i> Neues Passwort vergeben</h3>
                </div>
                <form id="resetPasswordForm" class="space-y-4">
                    <input type="hidden" id="resetOobCode">
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Neues Passwort</label>
                        <input type="password" id="resetPassword1" required minlength="8"
                            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:ring-1 focus:ring-primary-500 transition-colors"
                            placeholder="********">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Passwort bestätigen</label>
                        <input type="password" id="resetPassword2" required minlength="8"
                            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:ring-1 focus:ring-primary-500 transition-colors"
                            placeholder="********">
                    </div>
                    <ul class="text-xs text-gray-500 space-y-1 mt-2 mb-2 list-disc pl-4">
                        <li>Mindestens 8 Zeichen</li>
                        <li>Ein Groß- und ein Kleinbuchstabe</li>
                        <li>Eine Zahl und ein Sonderzeichen</li>
                    </ul>
                    <button type="submit"
                        class="w-full bg-primary-600 hover:bg-primary-500 text-white font-medium py-3 rounded-lg flex justify-center items-center gap-2 mt-4">
                        Passwort speichern
                    </button>
                </form>
            </div>
        </div>
        <!-- Contact Modal -->"""

app_content = app_content.replace('        <!-- Contact Modal -->', modal_html)

# 5. Insert logic for reset password mode
# We will insert it inside the DOMContentLoaded of the script, maybe just after firebaseConfig initialization
# Actually, the best place is right before `auth.onAuthStateChanged(...)`
auth_state = "        auth.onAuthStateChanged(async (user) => {"
reset_logic = """
        // Handle Password Reset Mode
        const urlParams = new URLSearchParams(window.location.search);
        const mode = urlParams.get('mode');
        const actionCode = urlParams.get('oobCode');

        if (mode === 'resetPassword' && actionCode) {
            document.getElementById('resetOobCode').value = actionCode;
            document.getElementById('resetPasswordModal').classList.remove('hidden');
            document.getElementById('resetPasswordModal').classList.add('flex');
        }

        window.addEventListener('DOMContentLoaded', () => {
            const rpForm = document.getElementById('resetPasswordForm');
            if (rpForm) {
                rpForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const code = document.getElementById('resetOobCode').value;
                    const p1 = document.getElementById('resetPassword1').value;
                    const p2 = document.getElementById('resetPassword2').value;

                    if (p1 !== p2) return showToast("Passwörter stimmen nicht überein", "error");
                    const pErr = validatePassword(p1);
                    if (pErr) return showToast(pErr, "error");

                    try {
                        const toast = showToast("Passwort wird gespeichert...", "loading");
                        await auth.confirmPasswordReset(code, p1);
                        dismissToast(toast);
                        showToast("Passwort erfolgreich zurückgesetzt! Sie können sich nun einloggen.", "success");
                        closeModal('resetPasswordModal');
                        // Clean up URL
                        window.history.replaceState({}, document.title, window.location.pathname);
                    } catch(err) {
                        showToast("Fehler: " + err.message, "error");
                    }
                });
            }
        });

        auth.onAuthStateChanged(async (user) => {"""
app_content = app_content.replace(auth_state, reset_logic)


with open(app_path, "w") as f:
    f.write(app_content)

print("done")
