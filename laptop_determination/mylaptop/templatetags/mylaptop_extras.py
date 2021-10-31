from django import template

register = template.Library()

# @register.filter
# def ubahFormat(harga):
#   harga_str = str(harga)
#   hasil = ""
#   count = 0
#   for i in reversed(range(len(harga_str))):
#     if count == 3:
#       hasil = "." + hasil
#       count = 0
#     count += 1
#     hasil = harga_str[i] + hasil
#   return hasil

@register.filter
def konversiMemori(ukuran):
	return int(ukuran*1000)