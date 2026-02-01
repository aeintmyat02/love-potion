from django.shortcuts import render, redirect
from .models import Ingredient, PotionResult
from .forms import PotionForm

# 🔐 CHANGE THIS PASSWORD TO ANYTHING YOU WANT
LOVE_LETTER_PASSWORD = "119"


def initial_page(request):
    error = None

    if request.method == "POST":
        password = request.POST.get("password")

        if password == LOVE_LETTER_PASSWORD:
            request.session["authenticated"] = True
            return redirect("mix_page")
        else:
            error = "💔 This envelope refuses to open… wrong password."

    return render(request, "potion/initial.html", {"error": error})


def mix_page(request):
    # 🚫 Prevent skipping the envelope page
    if not request.session.get("authenticated"):
        return redirect("initial_page")

    if request.method == "POST":
        form = PotionForm(request.POST)
        if form.is_valid():
            selected = list(form.cleaned_data["ingredients"])

            if len(selected) < 3 or len(selected) > 6:
                form.add_error(
                    "ingredients",
                    "Please choose between 3 and 6 ingredients 💕"
                )
            else:
                request.session["ingredient_ids"] = [i.id for i in selected]
                return redirect("result_page")
    else:
        form = PotionForm()

    return render(request, "potion/mix.html", {"form": form})


def result_page(request):
    ids = request.session.get("ingredient_ids")
    if not ids:
        return redirect("mix_page")

    selected = set(Ingredient.objects.filter(id__in=ids))

    best_score = -1
    best_result = None

    for potion in PotionResult.objects.prefetch_related("ingredients"):
        potion_ings = set(potion.ingredients.all())
        intersection = selected & potion_ings
        union = selected | potion_ings
        score = len(intersection) / len(union) if union else 0

        if score > best_score:
            best_score = score
            best_result = potion

    return render(request, "potion/result.html", {
        "ingredients": selected,
        "result": best_result
    })


def clear_session(request):
    request.session.flush()
    return redirect("initial_page")