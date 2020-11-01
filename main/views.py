import itertools

# https://coin-or.github.io/pulp/main/index.html
# https://realpython.com/linear-programming-python/
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from rest_framework.response import Response

from .forms import StatWeightForm
from .data import items


# pages that aren't part of dropdown
def index(request):
    if request.method == 'POST':
        print('here')
        form = StatWeightForm(request.POST)
        if form.is_valid():
            print('???')
            target_minimum_frost_resistance = int(form.cleaned_data['target_minimum_frost_resistance'])
            stat_weights = {
                'mp5': float(form.cleaned_data['mp5']),
                'spirit': float(form.cleaned_data['spirit']),
                'stamina': float(form.cleaned_data['stamina']),
                'intellect': float(form.cleaned_data['intellect']),
            }

            selected_items = itertools.chain(form.cleaned_data['neck_items'], form.cleaned_data['back_items'], form.cleaned_data['ring_items'],
                form.cleaned_data['trinket_items'], form.cleaned_data['wand_items'], form.cleaned_data['offhand_items'])
            
            # # creates a subset of items based on the gear user selected
            subset_items = create_copy_items(selected_items, float(form.cleaned_data['blue_dragon_mp5']))
            model = solve(subset_items, stat_weights, target_minimum_frost_resistance)

            # we want to return data to the user
            subset_item_map = {item['name']: item for item in itertools.chain(*subset_items)}
            
            results = {
                'items': [],
                'total_fr': 0,
            }

            for variable in model.variables():
                if variable.value() == 1:
                    name = ' '.join(variable.name.split('_'))
                    results['total_fr'] += subset_item_map[name]['frost_resistance']
                    results['items'].append(subset_item_map[name])

            return render(request, 'main/index.html', {
                'form': form,
                'results': results,
            })
        else:
            raise ValidationError('Form not Valid')
    else:
        return render(request, 'main/index.html', {
            'form': StatWeightForm(),
            'results': {},
        })

def results(request):
    return render(request, 'main/index.html', {'form': StatWeightForm})

# given selected items, create a 2D list (by item type, then item)
# also need to manually overwrite blue dragon value
def create_copy_items(selected_items, blue_dragon_mp5):
    print('here')
    item_map = {item['name']: item for item in itertools.chain(*items)}
    results = []

    current_item_type = ''
    for item in selected_items:
        print(item)
        entry = item_map[item]

        # every time there is a new item type, we create a new row
        if entry['type'] != current_item_type:
            results.append([])

        # append to latest row
        results[-1].append(entry)
        if entry['name'] == 'Blue Dragon':
            entry['mp5'] = blue_dragon_mp5
        current_item_type = entry['type']
    
    return results

def solve(subset_items, stat_weights, target_minimum_frost_resistance):
    model_fr = LpProblem(name='frost-resistance', sense=LpMaximize)

    objective_function = 0
    frost_resist_constraint = 0

    # creation of variables which follows the same 2d structure as "items" list
    # each item corresponds to a decison variable
    variables = []
    for index, row in enumerate(subset_items):
        variables.append([])
        for item in row:
            variables[index].append(LpVariable(name=item['name'], cat='Binary'))
            
            # calculates equivalent_healing for every item       
            item['equivalent_healing'] = item.get('mp5', 0) * stat_weights['mp5'] \
                + item.get('stamina', 0) * stat_weights['stamina'] \
                + item.get('spirit', 0) * stat_weights['spirit'] \
                + item.get('healing', 0) \
                + item.get('intellect', 0) * stat_weights['intellect']
                
            # for items without frost_resistance, add a default value         
            item.setdefault('frost_resistance', 0)
            
            # adds to objective function and frost_resist constraints        
            objective_function += variables[index][-1] * item['equivalent_healing']
            frost_resist_constraint += variables[index][-1] * item['frost_resistance']

    # constraint - can only equip one type of item (except for trinkets and rings)
    for index, row in enumerate(variables):
        is_ring_or_trinket = subset_items[index][0]['type'] in ['ring', 'trinket']
        model_fr += (lpSum(row) <= (2 if is_ring_or_trinket else 1), '{} slot constraint'.format(subset_items[index][0]['type']))

    model_fr += (frost_resist_constraint >= target_minimum_frost_resistance, 'Minimum Frost Resist')
    model_fr += objective_function
    model_fr.solve()

    return model_fr