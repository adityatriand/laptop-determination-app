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
	"""Convert memory size to proper format (GB/TB)"""
	try:
		size = float(size)
		if size == 0:
			return "0 GB"
		elif size < 1024:
			return f"{int(size)} GB"
		else:
			return f"{size/1024:.1f} TB"
	except (ValueError, TypeError):
		return "0 GB"

@register.filter
def format_rupiah(value):
    """Format number as Indonesian Rupiah currency"""
    try:
        # Convert to float first
        num = float(value)
        
        # Format with thousand separators
        formatted = f"{num:,.0f}"
        
        # Add Rp prefix
        return f"Rp {formatted}"
    except (ValueError, TypeError):
        return "Rp 0"

@register.filter
def laptop_alias(value):
    """Generate a short alias for laptop names"""
    if not value:
        return ""
    
    # Convert to string and clean up
    name = str(value).strip()
    
    # If already short enough, return as is
    if len(name) <= 25:
        return name
    
    # Extract key components
    parts = name.split()
    if len(parts) < 2:
        return name[:25] + "..." if len(name) > 25 else name
    
    # Try to create meaningful alias
    brand = parts[0]
    
    # Look for model indicators
    model_indicators = ['IdeaPad', 'ThinkPad', 'Aspire', 'TravelMate', 'MacBook', 'Inspiron', 'Vostro', 'Latitude', 'Precision', 'EliteBook', 'ProBook', 'Pavilion', 'Envy', 'Spectre', 'Omen', 'ProBook', 'EliteBook', 'ZBook', 'ProBook', 'EliteBook', 'ZBook', 'ProBook', 'EliteBook', 'ZBook']
    
    model = ""
    for indicator in model_indicators:
        if indicator in name:
            model = indicator
            break
    
    if model:
        # Find model number/identifier
        model_start = name.find(model)
        model_part = name[model_start:model_start + 20]  # Take first 20 chars of model part
        return f"{brand} {model_part}"
    else:
        # Fallback: brand + first few words
        remaining = " ".join(parts[1:3])  # Take next 2 words
        return f"{brand} {remaining[:15]}" if remaining else brand

