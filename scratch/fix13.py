import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# 1. Update duration in installPWA
old_toast = 'showToast("App Installation: Tippe im Menü deines Browsers (z.B. \'Teilen\') auf \'Zum Home-Bildschirm\'.", "info", 6000);'
new_toast = 'showToast("Um einen Shortcut zu erstellen, tippe im Menü deines Browsers (z.B. das \'Teilen\'-Symbol auf dem iPhone oder die 3 Punkte in Chrome) auf \'Zum Home-Bildschirm\' oder \'Installieren\'.", "info", 12000);'
app_content = app_content.replace(old_toast, new_toast)

# 2. Update button text in the menus
old_btn = '<i data-lucide="smartphone" class="w-4 h-4"></i> App installieren'
new_btn = '<i data-lucide="smartphone" class="w-4 h-4"></i> Shortcut zu Homescreen/Desktop'
app_content = app_content.replace(old_btn, new_btn)

with open(app_path, "w") as f:
    f.write(app_content)

print("done")
