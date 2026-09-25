import os

old_nav = '''    <nav class="glass-card border-x-0 border-t-0 p-4 sticky top-0 z-50">
        <div class="max-w-3xl mx-auto flex items-center gap-3">
            <a href="index.html" class="flex items-center gap-2 hover:opacity-80 transition">
                <img src="./icon.svg" class="w-8 h-8">
                <span class="font-bold text-xl">Metraxo</span>
            </a>
        </div>
    </nav>'''

new_nav = '''    <nav class="glass-card border-x-0 border-t-0 p-4 sticky top-0 z-50">
        <div class="max-w-3xl mx-auto flex items-center gap-4">
            <a href="javascript:history.length > 1 ? history.back() : window.location.href='index.html'" class="p-2 -ml-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors flex items-center justify-center shrink-0" title="Zurück">
                <i data-lucide="arrow-left" class="w-5 h-5"></i>
            </a>
            <a href="index.html" class="flex items-center gap-2 hover:opacity-80 transition">
                <img src="./icon.svg" class="w-8 h-8">
                <span class="font-bold text-xl">Metraxo</span>
            </a>
        </div>
    </nav>'''

files = ['faq.html', 'impressum.html', 'datenschutz.html', 'agb.html']
base_dir = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung"

for f in files:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, "r") as file:
            content = file.read()
        
        content = content.replace(old_nav, new_nav)
        
        with open(path, "w") as file:
            file.write(content)

print("done")
