from django.http import HttpResponse
from cook.models import Recipe
from cook.models import Ingredient
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

def recipies(request):
    recipies_list = Recipe.objects.all()
    recipies_json = serializers.serialize('json', recipies_list, fields=('name'))
    return HttpResponse(content=recipies_json)

def ingredients(request):
    recipe = request.GET.get('id')
    ingredients_list = Ingredient.objects.filter(recipe__id = recipe)
    return HttpResponse(content=serializers.serialize('json',ingredients_list))

def steps(request):
    recipe= Recipe.objects.filter(pk = request.GET.get('id'))
    steps = recipe[0].steps
    print steps
    steps = steps.split('|')
    
    steps_dict = {}
    steps_dict['steps'] = steps
    steps_json = json.dumps(steps_dict)
    return HttpResponse(steps_json)

def delete(request,type):
    id = request.GET.get('id')
    print type
    if 'recipe' in type:
        Recipe.objects.filter(pk = int(id)).delete()
    if 'ingredient' in type:
        Ingredient.objects.filter(pk = int(id)).delete()
    return HttpResponse(content = "done") 

@csrf_exempt
def ingest(request):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    ingredients = body['ingredients']
    steps = body['steps']
    recipe_name = body['name']
    step_string = ''
    for step in steps:
        step_string=step_string + '|'+step
    print step_string
    step_string = step_string[:-1]
    recipe,created = Recipe.objects.get_or_create(name = recipe_name)
    recipe.steps = steps
    for ingredient_name in ingredients:
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
        recipe.ingredients.add(ingredient)
    recipe.save()
    return HttpResponse(content = "done")
    