from rest_framework import serializers
from .models import Recipe, Ingredients, Steps, Comments


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "title"]


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ["id", "item", "quantity"]


class StepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = ["id", "description", "order"]


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "comment"]


class RecipeViewSerializer(serializers.ModelSerializer):
    ingredients_set = IngredientsSerializer(many=True)
    steps_set = StepsSerializer(many=True)
    comments_set = CommentsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ["id", "title", 'ingredients_set', 'steps_set', 'comments_set']


class CommentsCreateSerializer(serializers.ModelSerializer):
    recipe_id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(), write_only=True)

    class Meta:
        model = Comments
        fields = ["id", "comment", "recipe_id"]

    def create(self, validated_data):
        recipe = validated_data.pop('recipe_id')
        # recipe = Recipe.objects.get(id=recipe_id)
        comment = Comments.objects.create(recipe=recipe, **validated_data)
        return comment


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients_set = IngredientsSerializer(many=True, required=True)
    steps_set = StepsSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = ["id", "title", "ingredients_set", "steps_set"]

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_set')
        steps = validated_data.pop('steps_set')

        instance = super().create(validated_data)
        for ingredient in ingredients:
            Ingredients.objects.create(**ingredient, recipe=instance)

        for step in steps:
            Steps.objects.create(**step, recipe=instance)
        return instance
    '''
    {
            "title": "Boiled Eggs",
            "ingredients_set": [{"item": "Eggs", "quantity": "2"}, {"item": "water", "quantity": "2 cups"},
                                {"item": "Salt", "quantity": "2 tbs"}],
            "steps_set": [{"description": "Boil the water in a pan for 20 minutes", "order": 1},
                          {"description": "Take the eggs out and let them cool down", "order": 2},
                          {"description": "Remove the shell, sprinkle some salt and eat", "order": 3}]
        }
    '''
