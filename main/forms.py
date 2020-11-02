import itertools

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Field
from crispy_forms.bootstrap import InlineCheckboxes

from .data import items

# we split items by slot
item_map_by_slot = {}
preselected = {}
for row in items:
    item_map_by_slot[row[0]['type']] = [(item['name'], item['name']) for item in row]
    preselected[row[0]['type']] = [item['name'] for item in row]

class StatWeightForm(forms.Form):
    is_dwarf = forms.BooleanField(required=False)
    frost_resist_cloak_enchant = forms.BooleanField(required=False)
    target_minimum_frost_resistance = forms.CharField(initial='80')
    mp5 = forms.CharField(initial='3')
    intellect = forms.CharField(initial='1.3')
    spirit = forms.CharField(initial='0.7')
    stamina = forms.CharField(initial='0.2')
    blue_dragon_mp5 = forms.CharField(initial='25')

    neck_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['neck'],
        initial=preselected['neck'],
        required=False
    )
    back_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['back'],
        initial=preselected['back'],
        required=False
    )
    head_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['head'],
        initial=preselected['head'],
        required=False
    )
    legs_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['legs'],
        initial=preselected['legs'],
        required=False
    )
    ring_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['ring'],
        initial=preselected['ring'],
        required=False
    )
    trinket_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['trinket'],
        initial=preselected['trinket'],
        required=False
    )
    wand_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['wand'],
        initial=preselected['wand'],
        required=False
    )
    offhand_items = forms.MultipleChoiceField(
        choices=item_map_by_slot['offhand'],
        initial=preselected['offhand'],
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
        HTML("""
            <p><b><i>Please enter character details.</i></b></p>
        """),
        Row(
            Column('target_minimum_frost_resistance', css_class='form-group col-md-4 mb-0'),
            Column('is_dwarf', css_class='form-group col-md-2 mb-0'),
            Column('frost_resist_cloak_enchant', css_class='form-group col-md-4 mb-0'),
        ),
        HTML("""
            <br><p><b><i>Please enter your desired stat weights.</i></b></p>
        """),
            Row(
                Column('mp5', css_class='form-group col-md-2 mb-0'),
                Column('intellect', css_class='form-group col-md-2 mb-0'),
                Column('spirit', css_class='form-group col-md-2 mb-0'),
                Column('stamina', css_class='form-group col-md-2 mb-0'),
                Column('blue_dragon_mp5', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
        HTML("""<br>
            <p><i><b>Please tick the items you have.</i></b></p>
        """),
        InlineCheckboxes('neck_items'),
        HTML("<br>"),
        InlineCheckboxes('back_items'),
        HTML("<br>"),
        InlineCheckboxes('head_items'),
        HTML("<br>"),
        InlineCheckboxes('legs_items'),
        HTML("<br>"),
        InlineCheckboxes('wand_items'),
        HTML("<br>"),
        InlineCheckboxes('offhand_items'),
        HTML("<br>"),
        HTML("""
            <p><b><i>Note: Possible to wear duplicate Green FR rings and frost reflector trinkets.</i></b></p>
        """),
        InlineCheckboxes('ring_items'),
        HTML("<br>"),
        InlineCheckboxes('trinket_items'),
        HTML("<br>"),
        Submit('submit', 'Optimise')
        )