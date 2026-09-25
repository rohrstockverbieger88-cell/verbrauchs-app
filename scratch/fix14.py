import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# Update showToast function definition
old_toast_func = '''        function showToast(message, type = 'info') {
            const c = document.getElementById('toastContainer');
            const t = document.createElement('div');
            let icon = type === 'success' ? 'check-circle' : (type === 'error' ? 'alert-triangle' : (type === 'loading' ? 'loader-2' : 'info'));
            let iColor = type === 'success' ? 'text-green-400' : (type === 'error' ? 'text-red-400' : 'text-blue-400');
            let extraClass = type === 'loading' ? 'animate-spin' : '';

            t.className = `flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg bg-gray-800 border border-gray-700 toast-enter pointer-events-auto`;
            t.innerHTML = `<i data-lucide="${icon}" class="w-5 h-5 ${iColor} ${extraClass}"></i><span class="text-sm font-medium text-white shadow-sm">${message}</span>`;
            c.appendChild(t); lucide.createIcons();

            // Return element if caller wants to dismiss it manually (e.g. loading toast)
            if (type !== 'loading') {
                setTimeout(() => dismissToast(t), 3000);
            }
            return t;
        }'''

new_toast_func = '''        function showToast(message, type = 'info', duration = 3000) {
            const c = document.getElementById('toastContainer');
            const t = document.createElement('div');
            let icon = type === 'success' ? 'check-circle' : (type === 'error' ? 'alert-triangle' : (type === 'loading' ? 'loader-2' : 'info'));
            let iColor = type === 'success' ? 'text-green-400' : (type === 'error' ? 'text-red-400' : 'text-blue-400');
            let extraClass = type === 'loading' ? 'animate-spin' : '';

            t.className = `flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg bg-gray-800 border border-gray-700 toast-enter pointer-events-auto`;
            t.innerHTML = `<i data-lucide="${icon}" class="w-5 h-5 ${iColor} ${extraClass}"></i><span class="text-sm font-medium text-white shadow-sm">${message}</span>`;
            c.appendChild(t); lucide.createIcons();

            // Return element if caller wants to dismiss it manually (e.g. loading toast)
            if (type !== 'loading') {
                setTimeout(() => dismissToast(t), duration);
            }
            return t;
        }'''

app_content = app_content.replace(old_toast_func, new_toast_func)

with open(app_path, "w") as f:
    f.write(app_content)

print("done")
