import re

with open("index.html", "r") as f:
    content = f.read()

# Match the Admin Dashboard View block
admin_pattern = re.compile(r'(\s*<!-- ================== ADMIN DASHBOARD VIEW ================== -->\s*<div id="adminDashboardView".*?</div>\s*)(?=<!-- Create User Modal -->)', re.DOTALL)
match = admin_pattern.search(content)

if not match:
    print("Could not find adminDashboardView block")
    exit(1)

admin_block = match.group(1)

# Remove it from the original location
content = content[:match.start()] + content[match.end():]

# Insert it before </main>
main_close_idx = content.find("</main>")
if main_close_idx == -1:
    print("Could not find </main>")
    exit(1)

content = content[:main_close_idx] + admin_block + content[main_close_idx:]

with open("index.html", "w") as f:
    f.write(content)
print("Successfully moved adminDashboardView into <main>")
