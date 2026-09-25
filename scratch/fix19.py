import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

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

if "<!-- Resend Verification Modal -->" not in app_content:
    app_content = app_content.replace('    <!-- Contact Modal -->', modal_html)
    with open(app_path, "w") as f:
        f.write(app_content)
    print("inserted modal")
else:
    print("modal already exists")
