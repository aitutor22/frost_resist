import itertools

# https://coin-or.github.io/pulp/main/index.html
# https://realpython.com/linear-programming-python/
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

from django.shortcuts import render

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from .forms import StatWeightForm

# USER INPUTS
minimum_frost_resistance = 80
stat_weights = {
    'mp5': 3,
    'spirit': 0.7,
    'stamina': 0.5,
    'intellect': 1.3,
    'healing': 1,
}

# need to assign a stat weight to blue dragon to simulate properly
blue_dragon_mp5 = 25


# The goal is to maximize "Effective Healing" while maintaing a minimum amount of Frost Resistance
# Effective Healing is calculated based of the following stat weights
# Only Back, Wand, Offhand, Ring, and Trinket spots are considered (as well as ZG vs Ice guards for legs/helm)
# As it is expected priests will use 8/8


# pages that aren't part of dropdown
def index(request):
    return render(request, 'main/index.html', {'form': StatWeightForm})

@api_view(('POST',))
@renderer_classes((JSONRenderer, ))
def optimise(request):
    if request.method == 'POST':
        # form = EnquiryForm(request.POST)
        # if form.is_valid():
        #     enquiry = form.save(commit=False)

        #     message = 'Parent Name: {}\nEmail: {}\nContact Number: {}\nPreferred Outlet: {}\nLevel: {}\n'.format(
        #         enquiry.parent_name, enquiry.email, enquiry.contact_number, enquiry.preferred_outlet, enquiry.level)            
        #     r = send_email(message)
        #     if r.status_code != 200:
        #         return redirect('website:error_enquiry')
            
        #     enquiry.save()
        #     return redirect('website:thank_you')
        return redirect('main:results')
    else:
        return redirect('main:index')
