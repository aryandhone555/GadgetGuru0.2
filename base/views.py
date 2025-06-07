from django.shortcuts import render, redirect
from .forms import ChatbotForm
from .logic import recommend_laptop, generate_explanation
import markdown

def chatbot_view(request):
    # When the page is refreshed, treat it as a new session
    if request.method == 'GET':
        form = ChatbotForm()
        return render(request, 'index.html', {
            'form': form,
            'recommendations': [],
            'explanation': ''
        })

    # When form is submitted
    elif request.method == 'POST':
        form = ChatbotForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data
            user_input['category'] = [cat.lower() for cat in user_input['category']]

            recommendations, flag  = recommend_laptop(user_input)
            explanation = generate_explanation(user_input, recommendations)
            expalination_html = markdown.markdown(explanation)
            
            recommendations.columns = recommendations.columns.str.strip().str.replace(" ", "_").str.lower()

            return render(request, 'index.html', {
                'form': form,
                'recommendations': recommendations.to_dict(orient='records'),
                'explanation': expalination_html,
                'tag': flag
            })

    return redirect('/')

def step1_budget(request):
    if request.method == 'POST':
        budget = request.POST.get('budget')
        request.session['budget'] = budget
        return redirect('step2_category')
    return render(request, 'steps/step1_budget.html')


def about_page(request):
    return render(request, 'about.html')



