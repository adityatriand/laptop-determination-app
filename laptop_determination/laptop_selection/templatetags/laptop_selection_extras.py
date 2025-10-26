from django import template

register = template.Library()

# @register.filter
# def format_price(price):
#   price_str = str(price)
#   result = ""
#   count = 0
#   for i in reversed(range(len(price_str))):
#     if count == 3:
#       result = "." + result
#       count = 0
#     count += 1
#     result = price_str[i] + result
#   return result

@register.filter
def format_criteria_0(data, criteria_type):
	return "%.3f" % data[data['obj']['choice'].lower()][criteria_type][0]
@register.filter
def format_criteria_1(data, criteria_type):
	return "%.3f" % data[data['obj']['choice'].lower()][criteria_type][1]
@register.filter
def format_criteria_2(data, criteria_type):
	return "%.3f" % data[data['obj']['choice'].lower()][criteria_type][2]
@register.filter
def format_criteria_3(data, criteria_type):
	return "%.3f" % data[data['obj']['choice'].lower()][criteria_type][3]
@register.filter
def format_criteria_4(data, criteria_type):
	return "%.3f" % data[data['obj']['choice'].lower()][criteria_type][4]

@register.filter
def format_criteria_variable(data, criteria_type):
	# For scalar values like lambda_max, ci, cr, access directly
	if criteria_type in ['lambda_max', 'ci', 'cr', 'weight', 'wsv', 'cv']:
		return data[data['obj']['choice'].lower()][criteria_type]
	# For array values, return the first element
	else:
		return data[data['obj']['choice'].lower()][criteria_type][0]

@register.filter
def format_float(number):
	try:
		# Convert to float if it's a string
		if isinstance(number, str):
			number = float(number)
		return "%.3f" % number
	except (ValueError, TypeError):
		return "0.000"

@register.filter
def format_float_precise(number):
	return "%.20f" % number

@register.filter
def format_weight(data, index):
	# Get the criteria choice from the data
	choice = data['choice'].lower()
	return "%.5f" % data["weight"][choice][int(index)]

@register.filter
def convert_memory(size):
	return int(size*1000)

