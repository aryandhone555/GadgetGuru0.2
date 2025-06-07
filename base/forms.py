from django import forms

CATEGORY_CHOICES = [
    ("gaming", "Gaming"),
    ("productivity", "Productivity"),
    ("workstation", "Workstation"),
    ("basic computing", "Basic Computing"),
    ("business", "Business"),
]

BRAND_CHOICES = [
    ("any", "Any"),
    ("acer", "Acer"),
    ("apple", "Apple"),
    ("asus", "Asus"),
    ("avita", "Avita"),
    ("dell", "Dell"),
    ("gigabyte", "Gigabyte"),
    ("honor", "Honor"),
    ("hp", "Hp"),
    ("huawei", "Huawei"),
    ("jio", "Jio"),
    ("lenovo", "Lenovo"),
    ("microsoft", "Microsoft"),
    ("msi", "Msi"),
    ("samsung", "Samsung"),
    ("zebronics", "Zebronics"),
]


class ChatbotForm(forms.Form):
    budget = forms.IntegerField(label="Budget (₹)", min_value=10000, max_value=500000)
    category = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="What will you use the laptop for?",
    )
    travel = forms.BooleanField(label="Do you travel frequently?", required=False)
    battery = forms.BooleanField(label="Do you need long battery life?", required=False)
    brand = forms.MultipleChoiceField(choices=BRAND_CHOICES, widget=forms.CheckboxSelectMultiple, label="Preferred Brand")
