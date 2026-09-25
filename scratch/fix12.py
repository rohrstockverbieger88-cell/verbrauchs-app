import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Add installPWA function and listener
js_logic = '''
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
        });

        async function installPWA() {
            closeMobileMenuHack();
            closeMobileMenuObjectHack();
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                deferredPrompt = null;
            } else {
                showToast("App Installation: Tippe im Menü deines Browsers (z.B. 'Teilen') auf 'Zum Home-Bildschirm'.", "info", 6000);
            }
        }
'''
app_content = app_content.replace("        // Klick außerhalb des Menüs schließt es", js_logic + "\n        // Klick außerhalb des Menüs schließt es")

# 2. Add the button to mobileMenuDropdown (appContainer)
old_menu_1 = '''                                    <a href="faq.html" onclick="closeMobileMenuHack(); closeMobileMenuObjectHack();"
                                        class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                        <i data-lucide="help-circle" class="w-4 h-4"></i> Hilfe
                                    </a>'''
new_menu_1 = '''                                    <button onclick="installPWA()"
                                        class="w-full text-left px-4 py-3 text-sm text-green-400 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                        <i data-lucide="smartphone" class="w-4 h-4"></i> App installieren
                                    </button>
                                    <a href="faq.html" onclick="closeMobileMenuHack(); closeMobileMenuObjectHack();"
                                        class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                        <i data-lucide="help-circle" class="w-4 h-4"></i> Hilfe
                                    </a>'''
app_content = app_content.replace(old_menu_1, new_menu_1)

# 3. Add the button to mobileMenuDropdownObject (objectSelectionView)
old_menu_2 = '''                                <a href="faq.html" onclick="closeMobileMenuHack(); closeMobileMenuObjectHack();"
                                    class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="help-circle" class="w-4 h-4"></i> Hilfe
                                </a>'''
new_menu_2 = '''                                <button onclick="installPWA()"
                                    class="w-full text-left px-4 py-3 text-sm text-green-400 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="smartphone" class="w-4 h-4"></i> App installieren
                                </button>
                                <a href="faq.html" onclick="closeMobileMenuHack(); closeMobileMenuObjectHack();"
                                    class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="help-circle" class="w-4 h-4"></i> Hilfe
                                </a>'''
app_content = app_content.replace(old_menu_2, new_menu_2)

with open(app_path, "w") as f:
    f.write(app_content)

print("done")
