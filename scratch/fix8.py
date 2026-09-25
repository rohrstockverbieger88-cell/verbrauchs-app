import os

# 1. Update app.html Dropdown
app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

old_dropdown_obj = '''                                <button onclick="closeMobileMenuObjectHack(); openContactModal('Verbesserung')"
                                    class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="message-square" class="w-4 h-4"></i> Verbesserung
                                </button>
                            </div>'''
new_dropdown_obj = '''                                <button onclick="closeMobileMenuObjectHack(); openContactModal('Verbesserung')"
                                    class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="message-square" class="w-4 h-4"></i> Verbesserung
                                </button>
                                <a href="https://link.amazon/B0dveTLTp" target="_blank" rel="noopener noreferrer"
                                    class="w-full text-left px-4 py-3 text-sm text-[#FF9900] hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="shopping-cart" class="w-4 h-4"></i> Auf Amazon shoppen
                                </a>
                                <a href="https://paypal.me/DeinPayPalLink" target="_blank" rel="noopener noreferrer"
                                    class="w-full text-left px-4 py-3 text-sm text-pink-400 hover:text-white hover:bg-gray-700 flex items-center gap-2 border-t border-gray-700">
                                    <i data-lucide="heart" class="w-4 h-4"></i> Entwickler spenden
                                </a>
                            </div>'''
app_content = app_content.replace(old_dropdown_obj, new_dropdown_obj)

with open(app_path, "w") as f:
    f.write(app_content)

# 2. Update index.html logic
index_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/index.html"
with open(index_path, "r") as f:
    index_content = f.read()

# I'll inject script logic for ?contact=true at the end before </body>
script_logic = '''
    <script>
        document.addEventListener("DOMContentLoaded", () => {
            if (window.location.search.includes("contact=true")) {
                setTimeout(() => openContactModal('Frage'), 500);
            }
        });
    </script>
</body>'''
if 'contact=true' not in index_content:
    index_content = index_content.replace('</body>', script_logic)

with open(index_path, "w") as f:
    f.write(index_content)

# 3. Update faq.html
faq_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/faq.html"
with open(faq_path, "r") as f:
    faq_content = f.read()

old_faq_footer = '''        <div class="max-w-3xl mx-auto px-4 flex flex-wrap justify-center gap-4 sm:gap-6 mb-4">
            <a href="faq.html" class="hover:text-primary-400">FAQ</a>
            <a href="impressum.html" class="hover:text-primary-400">Impressum</a>'''
new_faq_footer = '''        <div class="max-w-3xl mx-auto px-4 flex flex-wrap justify-center gap-4 sm:gap-6 mb-4">
            <a href="faq.html" class="hover:text-primary-400">FAQ</a>
            <a href="index.html?contact=true" class="hover:text-primary-400">Kontakt</a>
            <a href="impressum.html" class="hover:text-primary-400">Impressum</a>'''
faq_content = faq_content.replace(old_faq_footer, new_faq_footer)

old_faq_details = '''            <details class="group bg-slate-900 border border-slate-800 rounded-xl overflow-hidden [&_summary::-webkit-details-marker]:hidden">
                <summary class="flex cursor-pointer items-center justify-between gap-1.5 p-5 text-white font-medium">
                    Wie ändere ich mein Passwort?
                    <span class="shrink-0 transition duration-300 group-open:-rotate-180">
                        <i data-lucide="chevron-down" class="w-5 h-5 text-slate-400"></i>
                    </span>
                </summary>
                <div class="px-5 pb-5 text-slate-400 leading-relaxed text-sm border-t border-slate-800 pt-4 mt-2">
                    Klicke in der App auf das Optionen-Menü (oben rechts) und wähle <strong>"Passwort ändern"</strong>. Du erhältst dann eine E-Mail mit einem Link zum Zurücksetzen.
                </div>
            </details>
        </div>'''
new_faq_details = '''            <details class="group bg-slate-900 border border-slate-800 rounded-xl overflow-hidden [&_summary::-webkit-details-marker]:hidden">
                <summary class="flex cursor-pointer items-center justify-between gap-1.5 p-5 text-white font-medium">
                    Wie ändere ich mein Passwort?
                    <span class="shrink-0 transition duration-300 group-open:-rotate-180">
                        <i data-lucide="chevron-down" class="w-5 h-5 text-slate-400"></i>
                    </span>
                </summary>
                <div class="px-5 pb-5 text-slate-400 leading-relaxed text-sm border-t border-slate-800 pt-4 mt-2">
                    Klicke in der App auf das Optionen-Menü (oben rechts) und wähle <strong>"Passwort ändern"</strong>. Du erhältst dann eine E-Mail mit einem Link zum Zurücksetzen.
                </div>
            </details>

            <details class="group bg-slate-900 border border-slate-800 rounded-xl overflow-hidden [&_summary::-webkit-details-marker]:hidden">
                <summary class="flex cursor-pointer items-center justify-between gap-1.5 p-5 text-white font-medium">
                    Nichts passendes gefunden?
                    <span class="shrink-0 transition duration-300 group-open:-rotate-180">
                        <i data-lucide="chevron-down" class="w-5 h-5 text-slate-400"></i>
                    </span>
                </summary>
                <div class="px-5 pb-5 text-slate-400 leading-relaxed text-sm border-t border-slate-800 pt-4 mt-2">
                    <a href="index.html?contact=true" class="text-primary-400 hover:underline font-bold">Kontaktieren Sie uns hier</a>
                </div>
            </details>
        </div>'''
faq_content = faq_content.replace(old_faq_details, new_faq_details)

with open(faq_path, "w") as f:
    f.write(faq_content)
print("done")
