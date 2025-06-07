import pandas as pd

# Load the laptop data globally to avoid repeated reads
#laptop_df = pd.read_csv("E:\python practice\Final year project\gadgetguru\gadgetguru\classified_laptops_improved.csv")

classified_laptops = pd.read_csv("classified_laptops_improved.csv")
# classified_laptops.columns = classified_laptops.columns.str.strip().str.replace(" ", "_").str.lower()


# def recommend_laptop(user_prefs):
#     budget = user_prefs.get("budget")
#     categories = user_prefs.get("category", [])
#     travel = user_prefs.get("travel")
#     battery = user_prefs.get("battery")
#     brand = user_prefs.get("brand")
    
#     df_filtered = laptop_df.copy()
    
#     # Filter based on budget
#     if budget:
#         df_filtered = df_filtered[df_filtered['price'] <= budget]
    
#     # Filter by brand (if not "Any")
#     if brand and brand.lower() != "any":
#         df_filtered = df_filtered[df_filtered['brand'].str.lower() == brand.lower()]
    
#     # Category matching (more matches = better score)
#     def score_category(row):
#         matches = sum([row.get(cat, 0) for cat in categories])
#         return matches
    
#     df_filtered['Category Score'] = df_filtered.apply(score_category, axis=1)
    
#     # Add travel/battery weightage
#     if travel:
#         df_filtered['Category Score'] += df_filtered.get('Portability', 0)
#     if battery:
#         df_filtered['Category Score'] += df_filtered.get('Battery Life', 0)
    
#     # Add price proximity score (higher is better)
#     # This rewards laptops closer to the budget
#     if budget:
#         df_filtered['Price Score'] = df_filtered['price'] / budget
#     else:
#         df_filtered['Price Score'] = 0
    
#     # Combined score with weights (adjust weights as needed)
#     category_weight = 0.7  # Category matching importance
#     price_weight = 0.3     # Budget utilization importance
    
#     df_filtered['Final Score'] = (df_filtered['Category Score'] * category_weight) + \
#                                  (df_filtered['Price Score'] * price_weight)
    
#     # Final score sorting
#     df_sorted = df_filtered.sort_values(by='Final Score', ascending=False)
    
#     # Return top 5 laptops as dictionaries
#     return df_sorted.head(5)


def recommend_laptop(user_prefs):
    budget = user_prefs.get("budget")
    categories = user_prefs.get("category", [])
    travel = user_prefs.get("travel")
    battery = user_prefs.get("battery")
    brand = user_prefs.get("brand",[])
    flag = "top"
    
    brand = [b.title() for b in brand]
    categories = [c.title() for c in categories]
    # First filter by budget
    budget_laptops = classified_laptops[classified_laptops["Price"] <= budget]
    
    # Apply brand filter if specified
    if "Any" not in brand:
        brand_laptops = budget_laptops[budget_laptops["Brand"].isin(brand)]
        
        # If brand laptops exist, use them as our primary dataset
        if not brand_laptops.empty:
            filtered_laptops = brand_laptops
        else:
            # No laptops of the requested brand within budget
            filtered_laptops = budget_laptops
            flag = "nobrand"
    else:
        # No brand preference specified
        filtered_laptops = budget_laptops

    
    # Now filter by categories
    filtered_laptops = filtered_laptops[
        filtered_laptops["Laptop Categories"].apply(
            lambda x: any(cat in eval(x) for cat in categories)
        )
    ]
    
    if not filtered_laptops.empty:
        # Apply combined scoring for remaining preferences
        filtered_laptops['combined_score'] = filtered_laptops['Laptop Score']
        
        # Adjust for travel preference (weight)
        if travel == 1:
            weight_max = filtered_laptops['weight'].max()
            weight_min = filtered_laptops['weight'].min()
            weight_range = weight_max - weight_min
            if weight_range > 0:
                filtered_laptops['weight_score'] = (weight_max - filtered_laptops['weight']) / weight_range
                filtered_laptops['combined_score'] += filtered_laptops['weight_score'] * 0.3
        
        # Adjust for battery preference
        if battery == 1:
            battery_max = filtered_laptops['battery capacity'].max()
            battery_min = filtered_laptops['battery capacity'].min()
            battery_range = battery_max - battery_min
            if battery_range > 0:
                filtered_laptops['battery_score'] = (filtered_laptops['battery capacity'] - battery_min) / battery_range
                filtered_laptops['combined_score'] += filtered_laptops['battery_score'] * 0.3
        
        # Get top recommendations
        top_laptops = filtered_laptops.sort_values(by=['combined_score'], ascending=False).head(5)
        return top_laptops, flag
    
    else:
        # No laptops match category criteria after brand/budget filtering
        flag = "alternative"
        
        # Check if there are any laptops of the requested brand within budget
        if "Any" not in brand and flag == "nobrand":
            brand_alternatives = budget_laptops[budget_laptops["Brand"].isin(brand)]
            if not brand_alternatives.empty:
                # Return both general alternatives and brand alternatives
                general_alternatives = budget_laptops.sort_values(by=["Laptop Score"], ascending=False).head(4)
                top_brand = brand_alternatives.sort_values(by=["Laptop Score"], ascending=False).head(1)
                general_alternatives.append(top_brand)
                return general_alternatives, "alternative_with_brand"
        
        # Just return general alternatives
        alternative_laptops = budget_laptops.sort_values(by=["Laptop Score"], ascending=False).head(5)
        if not alternative_laptops.empty:
            return alternative_laptops, flag
        else:
            return None, None


# def generate_explanation(user_prefs, df=laptop_df):
#     explanation = []
#     explanation.append(f"Budget: ₹{user_prefs['budget']}")
#     explanation.append(f"Categories: {', '.join(user_prefs['category'])}")
    
#     if user_prefs["travel"]:
#         explanation.append("You prefer portability for frequent travel.")
#     if user_prefs["battery"]:
#         explanation.append("You need long battery life.")
#     if user_prefs["brand"].lower() != "any":
#         explanation.append(f"You prefer laptops from {user_prefs['brand']}.")

#     return " ".join(explanation)

def generate_explanation(user_prefs, laptop_df):
    """Generate a user-friendly explanation of why the recommended laptops match the user's needs,
    with a clear HTML comparison table for better visualization."""
    
    if laptop_df is None or laptop_df.empty:
        return "I couldn't find laptops that perfectly match your requirements."
    
    # Extract key information
    budget = user_prefs.get("budget")
    categories = user_prefs.get("category", [])
    travel_priority = user_prefs.get("travel")
    battery_priority = user_prefs.get("battery")
    brand_preference = user_prefs.get("brand")
    
    # Start with a personalized greeting
    explanation = "I've selected these laptops specifically for you based on what you told me. Here's why they're a great match:\n\n"
    
    # General category explanation
    if "Gaming" in categories:
        explanation += "🎮 **For Gaming:** These laptops have powerful graphics cards and fast processors that can handle modern games. " 
        explanation += "The high refresh rate displays mean smoother gameplay with less motion blur.\n\n"
    
    if "Workstation" in categories:
        explanation += "💼 **For Professional Work:** These machines offer substantial processing power and RAM to handle demanding software. "
        explanation += "The storage options give you plenty of space for your projects.\n\n"
    
    if "Productivity" in categories:
        explanation += "📊 **For Productivity:** These laptops offer a balance of performance and portability. "
        explanation += "They have enough power to handle multitasking, office applications, and most productivity software.\n\n"
    
    if "Business" in categories:
        explanation += "🏢 **For Business Use:** These laptops offer reliability and performance in a professional package. "
        explanation += "They're built to handle daily business tasks efficiently with good security features.\n\n"
    
    if "Budget" in categories or "Basic Computing" in categories:
        explanation += "💰 **Value for Money:** These laptops offer good performance at reasonable price points, giving you the essential features without unnecessary extras.\n\n"
    
    # Number of laptops to compare
    num_laptops = min(len(laptop_df), 5)
    
    
    # Create rankings to determine strengths
    perf_ranking = laptop_df.iloc[:num_laptops].copy().sort_values('RAM', ascending=False)
    battery_ranking = laptop_df.iloc[:num_laptops].copy().sort_values('battery capacity', ascending=False)
    weight_ranking = laptop_df.iloc[:num_laptops].copy().sort_values('weight')
    price_ranking = laptop_df.iloc[:num_laptops].copy().sort_values('Price')
    
    for i in range(num_laptops):
        laptop = laptop_df.iloc[i]
        strengths = []
        
        # Determine laptop strengths based on rankings
        if laptop['Brand'] == perf_ranking.iloc[0]['Brand'] and laptop['Series'] == perf_ranking.iloc[0]['Series'] and laptop['Item model number'] == perf_ranking.iloc[0]['Item model number']:
            strengths.append("Performance")
            
        if laptop['Brand'] == battery_ranking.iloc[0]['Brand'] and laptop['Series'] == battery_ranking.iloc[0]['Series'] and laptop['Item model number'] == battery_ranking.iloc[0]['Item model number']:
            strengths.append("Battery Life")
            
        if laptop['Brand'] == weight_ranking.iloc[0]['Brand'] and laptop['Series'] == weight_ranking.iloc[0]['Series'] and laptop['Item model number'] == weight_ranking.iloc[0]['Item model number']:
            strengths.append("Portability")
            
        if laptop['Brand'] == price_ranking.iloc[0]['Brand'] and laptop['Series'] == price_ranking.iloc[0]['Series'] and laptop['Item model number'] == price_ranking.iloc[0]['Item model number']:
            strengths.append("Value")
        
        # If no special rankings, add a generic strength
        if not strengths:
            if "Gaming" in categories and ("GTX" in laptop['gpu'] or "RTX" in laptop['gpu']):
                strengths.append("Gaming")
            elif laptop['RAM'] >= 16:
                strengths.append("Multitasking")
            elif laptop['weight'] < 2.0:
                strengths.append("Travel")
            else:
                strengths.append("Everyday Use")

    # Add key strengths section highlighting each laptop's unique advantages
    explanation += "### 🌟 Key Strengths of Each Laptop\n\n"
    
    # For each laptop, highlight its main strengths
    for i in range(num_laptops):
        laptop = laptop_df.iloc[i]
        model_name = f"{laptop['Brand']} {laptop['Series']} {laptop['Item model number']}"
        explanation += f"##### {i+1}. {model_name}\n"
        
        strengths = []
        
        # Check if this laptop is best in any category
        if laptop['Brand'] == perf_ranking.iloc[0]['Brand'] and laptop['Series'] == perf_ranking.iloc[0]['Series'] and laptop['Item model number'] == perf_ranking.iloc[0]['Item model number']:
            strengths.append(f"🥇 **Best Performance:** Leads with {laptop['RAM']}GB RAM and {laptop['cpu']} processor")
            
        if laptop['Brand'] == battery_ranking.iloc[0]['Brand'] and laptop['Series'] == battery_ranking.iloc[0]['Series'] and laptop['Item model number'] == battery_ranking.iloc[0]['Item model number']:
            strengths.append(f"🥇 **Best Battery Life:** Top battery capacity at {laptop['battery capacity']}mAh")
            
        if laptop['Brand'] == weight_ranking.iloc[0]['Brand'] and laptop['Series'] == weight_ranking.iloc[0]['Series'] and laptop['Item model number'] == weight_ranking.iloc[0]['Item model number']:
            strengths.append(f"🥇 **Most Portable:** Lightest option at only {laptop['weight']} kg")
            
        if laptop['Brand'] == price_ranking.iloc[0]['Brand'] and laptop['Series'] == price_ranking.iloc[0]['Series'] and laptop['Item model number'] == price_ranking.iloc[0]['Item model number']:
            strengths.append(f"🥇 **Most Affordable:** Best price at ₹{laptop['Price']}")
        
        # Add second place mentions
        if len(perf_ranking) > 1 and laptop['Brand'] == perf_ranking.iloc[1]['Brand'] and laptop['Series'] == perf_ranking.iloc[1]['Series'] and laptop['Item model number'] == perf_ranking.iloc[1]['Item model number']:
            strengths.append(f"🥈 **Good Performance:** Second best with {laptop['RAM']}GB RAM")
            
        if len(battery_ranking) > 1 and laptop['Brand'] == battery_ranking.iloc[1]['Brand'] and laptop['Series'] == battery_ranking.iloc[1]['Series'] and laptop['Item model number'] == battery_ranking.iloc[1]['Item model number']:
            strengths.append(f"🥈 **Good Battery Life:** Second best with {laptop['battery capacity']}mAh capacity")
        
        # If no special rankings, add some generic strengths based on specs
        if not strengths:
            if laptop['RAM'] >= 16:
                strengths.append(f"✅ **High RAM:** {laptop['RAM']}GB for smooth multitasking")
            
            if "SSD" in laptop['Hard Disk Description']:
                strengths.append(f"✅ **Fast Storage:** {laptop['Hard Drive Size']} {laptop['Hard Disk Description']} for quick boot and load times")
            
            if laptop['refresh rate'] >= 120:
                strengths.append(f"✅ **Smooth Display:** {laptop['refresh rate']}Hz refresh rate for fluid visuals")
        
        # Add best use case recommendation
        if "Gaming" in categories and ("GTX" in laptop['gpu'] or "RTX" in laptop['gpu']):
            strengths.append(f"👍 **Ideal for:** Gaming, content creation, and demanding tasks")
        elif laptop['RAM'] >= 16 and ("Workstation" in categories or "Productivity" in categories):
            strengths.append(f"👍 **Ideal for:** Professional workloads and productivity")
        elif laptop['weight'] < 2.0 and travel_priority:
            strengths.append(f"👍 **Ideal for:** Frequent travelers and students on the go")
        else:
            strengths.append(f"👍 **Ideal for:** Everyday computing tasks with good overall performance")
        
        # Add the strengths as bullet points
        for strength in strengths:
            explanation += f"- {strength}\n"
        
        explanation += "\n"
    
    # Final recommendations based on user priorities
    explanation += "### 💯 Our Final Recommendations\n\n"
    
    if "Gaming" in categories:
        best_gaming = perf_ranking.iloc[0]
        explanation += f"- **If gaming is your top priority:** Choose the **{best_gaming['Brand']} {best_gaming['Series']} {best_gaming['Item model number']}**\n"
    
    if "Workstation" in categories:
        best_workstation = perf_ranking.iloc[0]
        explanation += f"- **If professional work is your top priority:** Choose the **{best_workstation['Brand']} {best_workstation['Series']} {best_workstation['Item model number']}**\n"
    
    if travel_priority:
        best_travel = weight_ranking.iloc[0]
        explanation += f"- **If portability is your top priority:** Choose the **{best_travel['Brand']} {best_travel['Series']} {best_travel['Item model number']}**\n"
    
    if battery_priority:
        best_battery = battery_ranking.iloc[0]
        explanation += f"- **If battery life is your top priority:** Choose the **{best_battery['Brand']} {best_battery['Series']} {best_battery['Item model number']}**\n"
    
    if "Budget" in categories or "Basic Computing" in categories:
        best_value = price_ranking.iloc[0]
        explanation += f"- **If budget is your top priority:** Choose the **{best_value['Brand']} {best_value['Series']} {best_value['Item model number']}**\n"
    
    # Close with a supportive message
    explanation += "\n🚀 **Bottom Line:** Each laptop has its own strengths that make it suitable for different needs. Use the comparison table and recommendations above to choose the one that best aligns with your most important requirements!"
    
    return explanation




#  const brandButtons = document.querySelectorAll('.brand-btn');
#             brandButtons.forEach(button => {
#                 const checkbox = button.querySelector('input[type="checkbox"]');
#                 button.classList.toggle('active', checkbox.checked);
#                 button.addEventListener('click', function() {
#                     checkbox.checked = !checkbox.checked;
#                     button.classList.toggle('active', checkbox.checked);
#                 });
#             });