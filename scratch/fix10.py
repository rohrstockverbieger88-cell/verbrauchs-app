import os

app_path = "/Users/bjoern_heroldweb.de/Desktop/Verbrauchsüberwachung/app.html"
with open(app_path, "r") as f:
    app_content = f.read()

# Replace links to close menus
old_faq = '<a href="faq.html"'
new_faq = '<a href="faq.html" onclick="closeMobileMenuHack(); closeMobileMenuObjectHack();"'

old_amazon = '<a href="https://link.amazon/B0dveTLTp"'
new_amazon = '<a href="https://link.amazon/B0dveTLTp" onclick="closeMobileMenuHack(); closeMobileMenuObjectHack();"'

old_paypal = '<a href="https://paypal.me/DeinPayPalLink"'
new_paypal = '<a href="https://paypal.me/DeinPayPalLink" onclick="closeMobileMenuHack(); closeMobileMenuObjectHack();"'

app_content = app_content.replace(old_faq, new_faq)
app_content = app_content.replace(old_amazon, new_amazon)
app_content = app_content.replace(old_paypal, new_paypal)

with open(app_path, "w") as f:
    f.write(app_content)

print("done")
