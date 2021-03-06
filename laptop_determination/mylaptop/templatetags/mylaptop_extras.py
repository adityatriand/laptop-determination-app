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
def formatKriteria0(data, tipe):
	return "%.3f" % data[data['obj']['pilihan'].lower()][tipe][0]
@register.filter
def formatKriteria1(data, tipe):
	return "%.3f" % data[data['obj']['pilihan'].lower()][tipe][1]
@register.filter
def formatKriteria2(data, tipe):
	return "%.3f" % data[data['obj']['pilihan'].lower()][tipe][2]
@register.filter
def formatKriteria3(data, tipe):
	return "%.3f" % data[data['obj']['pilihan'].lower()][tipe][3]
@register.filter
def formatKriteria4(data, tipe):
	return "%.3f" % data[data['obj']['pilihan'].lower()][tipe][4]

@register.filter
def formatKriteriaVariabel(data, tipe):
	return data[data['obj']['pilihan'].lower()][tipe]

@register.filter
def formatFloat(angka):
	return "%.3f" % angka

@register.filter
def formatFloat2(angka):
	return "%.20f" % angka

@register.filter
def formatWeight(data,index):
	return "%.5f" % data["weight"][data['pilihan'].lower()][int(index)]

@register.filter
def konversiMemori(ukuran):
	return int(ukuran*1000)

