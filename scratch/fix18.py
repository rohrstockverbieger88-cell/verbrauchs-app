import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. onAuthStateChanged early return
old_auth = """        auth.onAuthStateChanged(async (user) => {
            authLoadingView.classList.add('hidden');

            if (user) {
                currentUser = user;"""
new_auth = """        auth.onAuthStateChanged(async (user) => {
            authLoadingView.classList.add('hidden');

            if (user) {
                if (!user.emailVerified) {
                    // Bleibe auf der Login-Seite, wenn die E-Mail nicht bestätigt ist
                    return;
                }
                currentUser = user;"""
app_content = app_content.replace(old_auth, new_auth)

# 2. Add Resend Verification Modal HTML
modal_html = """
        <!-- Resend Verification Modal -->
        <div id="resendVerificationModal" class="fixed inset-0 z-50 hidden items-center justify-center p-4">
            <div class="fixed inset-0 bg-gray-950/90 backdrop-blur-md transition-opacity"></div>
            <div class="relative bg-gray-900 border border-red-900/50 rounded-xl shadow-2xl w-full max-w-sm slide-up p-5 text-center">
                <div class="mx-auto w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center mb-4 border border-red-500/30">
                    <i data-lucide="mail-warning" class="w-6 h-6 text-red-400"></i>
                </div>
                <h3 class="text-xl font-bold text-white mb-2">E-Mail nicht bestätigt</h3>
                <p class="text-gray-400 text-sm mb-6">Sie müssen erst den Bestätigungslink in Ihrer E-Mail anklicken, bevor Sie sich einloggen können.</p>
                
                <div class="space-y-3">
                    <button onclick="resendVerificationEmail()" class="w-full bg-primary-600 hover:bg-primary-500 text-white font-medium py-3 rounded-lg transition-colors">
                        Bestätigungsmail erneut senden
                    </button>
                    <button onclick="closeResendModal()" class="w-full bg-gray-800 hover:bg-gray-700 text-gray-300 font-medium py-3 rounded-lg transition-colors">
                        Abbrechen
                    </button>
                </div>
            </div>
        </div>
        <!-- Contact Modal -->"""
app_content = app_content.replace('        <!-- Contact Modal -->', modal_html)

# 3. Add JS function for resendVerificationEmail
js_functions = """
        async function resendVerificationEmail() {
            if (auth.currentUser && !auth.currentUser.emailVerified) {
                try {
                    const toast = showToast("Sende E-Mail...", "loading");
                    auth.languageCode = 'de';
                    await auth.currentUser.sendEmailVerification();
                    dismissToast(toast);
                    showToast("Bestätigungsmail erfolgreich gesendet!", "success");
                    closeResendModal();
                } catch(err) {
                    showToast("Fehler beim Senden: " + err.message, "error");
                }
            } else {
                showToast("Sitzung abgelaufen. Bitte erneut einloggen.", "error");
                closeResendModal();
            }
        }
        
        function closeResendModal() {
            document.getElementById('resendVerificationModal').classList.add('hidden');
            document.getElementById('resendVerificationModal').classList.remove('flex');
            auth.signOut();
        }
        
        auth.onAuthStateChanged(async (user) => {"""
app_content = app_content.replace('        auth.onAuthStateChanged(async (user) => {', js_functions)

# 4. Modify loginForm handler
old_login = """                } else {
                    await auth.signInWithEmailAndPassword(email, pwd);
                }"""
new_login = """                } else {
                    const userCred = await auth.signInWithEmailAndPassword(email, pwd);
                    if (!userCred.user.emailVerified) {
                        document.getElementById('resendVerificationModal').classList.remove('hidden');
                        document.getElementById('resendVerificationModal').classList.add('flex');
                    }
                }"""
app_content = app_content.replace(old_login, new_login)


# 5. Modify createUserForm (Admin side)
old_create_admin = """                        const userCred = await secondaryApp.auth().createUserWithEmailAndPassword(email, pwd);
                        await secondaryApp.auth().signOut();"""
new_create_admin = """                        secondaryApp.auth().languageCode = 'de';
                        const userCred = await secondaryApp.auth().createUserWithEmailAndPassword(email, pwd);
                        await userCred.user.sendEmailVerification();
                        await secondaryApp.auth().signOut();"""
app_content = app_content.replace(old_create_admin, new_create_admin)

# 6. Modify Registration flow in loginForm
old_reg = """                    const userCred = await auth.createUserWithEmailAndPassword(email, pwd);
                    await db.collection("users").doc(userCred.user.uid).set({ 
                        email, 
                        firstName,
                        lastName,
                        name: firstName + " " + lastName,
                        role: "User",
                        createdAt: firebase.firestore.FieldValue.serverTimestamp()
                    });

                    showToast("Registrierung erfolgreich! Lade Dashboard...", "success");"""

new_reg = """                    const userCred = await auth.createUserWithEmailAndPassword(email, pwd);
                    await db.collection("users").doc(userCred.user.uid).set({ 
                        email, 
                        firstName,
                        lastName,
                        name: firstName + " " + lastName,
                        role: "User",
                        createdAt: firebase.firestore.FieldValue.serverTimestamp()
                    });

                    auth.languageCode = 'de';
                    await userCred.user.sendEmailVerification();
                    showToast("Registrierung erfolgreich! Bitte bestätigen Sie Ihre E-Mail-Adresse.", "success");
                    await auth.signOut();
                    toggleAuthMode();
                    return;"""
app_content = app_content.replace(old_reg, new_reg)

with open(app_path, "w") as f:
    f.write(app_content)
    
print("done")
