from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models
import random
import math


def alternatives(request):
    """Display all available laptop alternatives"""
    laptops = models.Laptops.objects.all()
    context = {
        'laptops': laptops,
    }
    return render(request, 'laptop_selection/alternatives.html', context)


def search(request):
    """Display search interface for laptop selection"""
    laptops = models.Laptops.objects.all()
    criteria = ['Default', 'Price', 'RAM', 'CPU', 'SSD', 'HDD']
    
    unique_brands = []
    brand_names = []
    for laptop in laptops:
        if laptop.company not in brand_names:
            unique_brands.append(laptop)
            brand_names.append(laptop.company)

    context = {
        'brands': unique_brands,
        'criterias': criteria,
        'search_data': laptops
    }

    return render(request, 'laptop_selection/search.html', context)


def results(request):
    """Process search criteria and display AHP results"""
    default_criteria = ['PRICE', 'RAM', 'SSD', 'HDD', 'CPU']
    search_data = {}
    
    if request.method == 'POST':
        search_data['brand'] = request.POST['brand']
        
        for i in range(5):
            priority_key = f'priority_{i+1}'
            if request.POST[priority_key] == 'empty':
                search_data[priority_key] = default_criteria[i]
            else:
                search_data[priority_key] = request.POST[priority_key]

        alternatives = models.Laptops.objects.all()
        context = {
            'search_data': search_data,
            'alternatives': alternatives
        }

        context = process_ahp(context)
        return render(request, 'laptop_selection/results.html', context)
    else:
        return HttpResponseRedirect('/laptop-selection/search/')


def process_ahp(context):
    """Main AHP processing function"""
    search_data = context.get("search_data")
    all_alternatives = context.get("alternatives")
    filtered_alternatives = []
    processed_alternatives = []

    filtered_alternatives = filter_alternatives_by_brand(
        search_data['brand'], all_alternatives
    )

    n = len(filtered_alternatives)
    
    # Check if we have alternatives to process
    if n == 0:
        context = {
            'search_data': search_data,
            'alternatives': [],
            'ranking': [],
            'ranking_alternatives': [],
            'error_message': 'No laptops found matching the selected criteria.'
        }
        return context
    
    processed_alternatives = initialize_alternatives_data(filtered_alternatives, n)

    processed_alternatives = calculate_alternatives_weights(
        processed_alternatives, n
    )

    criteria_data = process_criteria_weights(search_data)

    ranking_results = calculate_final_ranking(
        processed_alternatives, criteria_data, n
    )

    context = {
        'search_data': criteria_data,
        'alternatives': processed_alternatives,
        'ranking': ranking_results['criteria_ranking'],
        'ranking_alternatives': ranking_results['alternatives_ranking']
    }
    
    return context


def filter_alternatives_by_brand(brand_choice, all_alternatives):
    """Filter alternatives based on brand selection"""
    if brand_choice != 'Semua':
        brand_alternatives = [
            laptop for laptop in all_alternatives 
            if laptop.company == brand_choice
        ]
        
        if len(brand_alternatives) > 20:
            random_indices = random.sample(range(len(brand_alternatives)), 20)
            return [brand_alternatives[i] for i in random_indices]
        else:
            return brand_alternatives
    else:
        if len(all_alternatives) > 20:
            random_indices = random.sample(range(len(all_alternatives)), 20)
            return [all_alternatives[i] for i in random_indices]
        else:
            return all_alternatives


def initialize_alternatives_data(alternatives, n):
    """Initialize data structure for alternatives"""
    processed_data = []
    
    for i in range(n):
        processed_data.append({
            "obj": alternatives[i],
            "cpu": create_criteria_structure(n),
            "price": create_criteria_structure(n),
            "ram": create_criteria_structure(n),
            "ssd": create_criteria_structure(n),
            "hdd": create_criteria_structure(n)
        })
    
    return processed_data


def create_criteria_structure(n):
    """Create initial structure for criteria calculations"""
    return {
        "initial": [0] * n,
        "normalized": [0] * n,
        "weight": 0,
        "weighted": [0] * n,
        "wsv": 0,
        "cv": 0,
        "lambda_max": 0.0,
        "ci": 0,
        "cr": 0
    }


def calculate_alternatives_weights(alternatives, n):
    """Calculate weights for all criteria in alternatives"""
    criteria_list = ["cpu", "price", "ram", "ssd", "hdd"]
    
    for criteria in criteria_list:
        alternatives = calculate_criteria_weights(alternatives, criteria, n)
    
    return alternatives


def calculate_criteria_weights(alternatives, criteria, n):
    """Calculate weights for a specific criteria"""
    for i, alt in enumerate(alternatives):
        alt[criteria]["initial"][i] = 1

    unique_values = get_unique_criteria_values(alternatives, criteria)
    
    for i in range(n):
        for j in range(i + 1, n):
            importance = determine_importance_level(
                alternatives[i], alternatives[j], criteria, unique_values
            )
            alternatives[i][criteria]["initial"][j] = importance
            alternatives[j][criteria]["initial"][i] = 1 / importance

    while True:
        row_sums = calculate_row_sums(alternatives, criteria, n)
        
        for alt in alternatives:
            for i in range(n):
                alt[criteria]["normalized"][i] = (
                    alt[criteria]["initial"][i] / row_sums[i]
                )

        for alt in alternatives:
            alt[criteria]["weight"] = sum(alt[criteria]["normalized"]) / n

        for alt in alternatives:
            for i in range(n):
                alt[criteria]["weighted"][i] = (
                    alt[criteria]["initial"][i] * alt[criteria]["weight"]
                )

        for alt in alternatives:
            alt[criteria]["wsv"] = sum(alt[criteria]["weighted"])

        for alt in alternatives:
            alt[criteria]["cv"] = alt[criteria]["wsv"] / alt[criteria]["weight"]

        lambda_max = sum(alt[criteria]["cv"] for alt in alternatives) / n if n > 0 else 0
        
        for alt in alternatives:
            alt[criteria]["lambda_max"] = lambda_max
            alt[criteria]["ci"] = (lambda_max - n) / (n - 1) if n > 1 else 0

        ri_values = [0, 0, 0.58, 1.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 
                    1.51, 1.48, 1.56, 1.57, 1.59]
        
        cr_exceeded = 0
        for alt in alternatives:
            if n <= 15:
                alt[criteria]["cr"] = alt[criteria]["ci"] / ri_values[n-1]
            else:
                alt[criteria]["cr"] = alt[criteria]["ci"] / ri_values[14]
            
            if alt[criteria]["cr"] > 0.1:
                cr_exceeded += 1

        if cr_exceeded > 0:
            random_i = random.randint(0, n-1)
            random_j = random.randint(0, n-1)
            if alternatives[random_i][criteria]["initial"][random_j] > 1:
                alternatives[random_i][criteria]["initial"][random_j] -= 1
        else:
            break

    return alternatives


def get_unique_criteria_values(alternatives, criteria):
    """Get unique values for a specific criteria"""
    unique_values = []
    for alt in alternatives:
        value = getattr(alt["obj"], criteria)
        if value not in unique_values:
            unique_values.append(value)
    return sorted(unique_values)


def determine_importance_level(alt1, alt2, criteria, unique_values):
    """Determine importance level between two alternatives for a criteria"""
    value1 = getattr(alt1["obj"], criteria)
    value2 = getattr(alt2["obj"], criteria)
    
    if value1 == value2:
        return 1
    
    step = abs(unique_values.index(value1) - unique_values.index(value2))
    return get_importance_value(step, len(unique_values))


def get_importance_value(step, total_values):
    """Get importance value based on step and total values"""
    if total_values <= 5:
        return {1: 2, 2: 4, 3: 5, 4: 6}.get(step, 1)
    elif total_values <= 9:
        return {1: 2, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 8: 6, 9: 7}.get(step, 1)
    elif total_values <= 17:
        if step <= 2:
            return 2
        elif step <= 4:
            return 3
        elif step <= 6:
            return 3
        elif step <= 8:
            return 4
        elif step <= 10:
            return 4
        elif step <= 12:
            return 5
        elif step <= 14:
            return 6
        elif step <= 16:
            return 7
    elif total_values <= 33:
        if step <= 4:
            return 2
        elif step <= 8:
            return 3
        elif step <= 12:
            return 3
        elif step <= 16:
            return 4
        elif step <= 20:
            return 4
        elif step <= 24:
            return 5
        elif step <= 28:
            return 6
        elif step <= 32:
            return 7
    elif total_values <= 65:
        if step <= 8:
            return 2
        elif step <= 16:
            return 3
        elif step <= 24:
            return 3
        elif step <= 32:
            return 4
        elif step <= 40:
            return 4
        elif step <= 48:
            return 5
        elif step <= 56:
            return 6
        elif step <= 64:
            return 7
    else:
        if step <= 16:
            return 2
        elif step <= 32:
            return 3
        elif step <= 48:
            return 3
        elif step <= 64:
            return 4
        elif step <= 80:
            return 4
        elif step <= 96:
            return 5
        elif step <= 112:
            return 6
        elif step <= 128:
            return 7
    
    return 1


def calculate_row_sums(alternatives, criteria, n):
    """Calculate row sums for normalization"""
    row_sums = []
    for alt in alternatives:
        row_sum = sum(alt[criteria]["initial"])
        row_sums.append(row_sum)
    return row_sums


def process_criteria_weights(search_data):
    """Process criteria weights based on user preferences"""
    n = 5
    criteria_choices = []
    
    for i in range(5):
        priority_key = f'priority_{i+1}'
        criteria_choices.append(search_data[priority_key])

    criteria_data = []
    for i in range(5):
        criteria_data.append({
            "obj": {"choice": criteria_choices[i]},
            "cpu": create_criteria_structure(n),
            "price": create_criteria_structure(n),
            "ram": create_criteria_structure(n),
            "ssd": create_criteria_structure(n),
            "hdd": create_criteria_structure(n)
        })

    criteria_data = calculate_criteria_importance_weights(criteria_data, criteria_choices)
    return criteria_data


def calculate_criteria_importance_weights(criteria_data, choices):
    """Calculate importance weights between criteria"""
    n = 5
    
    for i, criteria in enumerate(criteria_data):
        choice = criteria["obj"]['choice'].lower()
        criteria[choice]["initial"][i] = 1

    for i in range(n):
        for j in range(i + 1, n):
            importance = determine_criteria_importance_level(
                criteria_data[i], criteria_data[j], choices
            )
            choice_i = criteria_data[i]["obj"]['choice'].lower()
            choice_j = criteria_data[j]["obj"]['choice'].lower()
            
            criteria_data[i][choice_i]["initial"][j] = importance
            criteria_data[j][choice_j]["initial"][i] = 1 / importance

    while True:
        row_sums = []
        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            row_sum = sum(criteria[choice]["initial"])
            row_sums.append(row_sum)

        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            for i in range(n):
                criteria[choice]["normalized"][i] = (
                    criteria[choice]["initial"][i] / row_sums[i]
                )

        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            criteria[choice]["weight"] = sum(criteria[choice]["normalized"]) / n

        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            for i in range(n):
                criteria[choice]["weighted"][i] = (
                    criteria[choice]["initial"][i] * criteria[choice]["weight"]
                )

        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            criteria[choice]["wsv"] = sum(criteria[choice]["weighted"])

        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            criteria[choice]["cv"] = criteria[choice]["wsv"] / criteria[choice]["weight"]

        lambda_max = sum(
            criteria[criteria["obj"]['choice'].lower()]["cv"] 
            for criteria in criteria_data
        ) / n
        
        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            criteria[choice]["lambda_max"] = lambda_max
            criteria[choice]["ci"] = (lambda_max - n) / (n - 1)

        ri_values = [0, 0, 0.58, 1.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 
                    1.51, 1.48, 1.56, 1.57, 1.59]
        
        cr_exceeded = 0
        for criteria in criteria_data:
            choice = criteria["obj"]['choice'].lower()
            if n <= 15:
                criteria[choice]["cr"] = criteria[choice]["ci"] / ri_values[n-1]
            else:
                criteria[choice]["cr"] = criteria[choice]["ci"] / ri_values[14]
            
            if criteria[choice]["cr"] > 0.1:
                cr_exceeded += 1
                
        if cr_exceeded > 0:
            random_i = random.randint(0, n-1)
            random_j = random.randint(0, n-1)
            choice = criteria_data[random_i]["obj"]['choice'].lower()
            if criteria_data[random_i][choice]["initial"][random_j] > 1:
                criteria_data[random_i][choice]["initial"][random_j] -= 1
        else:
            break

    return criteria_data


def determine_criteria_importance_level(criteria1, criteria2, choices):
    """Determine importance level between two criteria"""
    step = abs(
        choices.index(criteria1['obj']['choice']) - 
        choices.index(criteria2['obj']['choice'])
    )
    
    if step == 1:
        return 2
    elif step == 2:
        return 4
    elif step == 3:
        return 5
    elif step == 4:
        return 6
    else:
        return 1


def calculate_final_ranking(alternatives, criteria_data, n):
    """Calculate final ranking of alternatives"""
    criteria_ranking = []
    choices = []
    
    for i in range(5):
        choice = criteria_data[i]["obj"]['choice']
        choices.append(choice)
        criteria_ranking.append({
            "weight": {choice.lower(): [0] * n},
            "choice": choice,
            "weight_value": 0
        })

    for i in range(5):
        choice = choices[i].lower()
        criteria_ranking[i]["weight_value"] = criteria_data[i][choice]['weight']
        for j in range(n):
            criteria_ranking[i]["weight"][choice][j] = alternatives[j][choice]['weight']

    total_scores = []
    for i in range(n):
        alternative_score = 0
        criteria_score = 0
        for j in range(5):
            choice = choices[j].lower()
            criteria_score += criteria_ranking[j]["weight_value"]
            alternative_score += criteria_ranking[j]["weight"][choice][i]
        total_scores.append(alternative_score * criteria_score)

    alternatives_ranking = []
    for i in range(n):
        alternatives_ranking.append({
            "score": total_scores[i],
            "rank": 0,
            "obj": None
        })

    sorted_scores = sorted(total_scores, reverse=True)
    for i in range(n):
        alternatives_ranking[i]['rank'] = sorted_scores.index(alternatives_ranking[i]['score']) + 1
        alternatives_ranking[i]['obj'] = alternatives[i]['obj']

    return {
        'criteria_ranking': criteria_ranking,
        'alternatives_ranking': alternatives_ranking
    }