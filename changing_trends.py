import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

file_path = r"C:/Users/mattc/Downloads/fav_nuclear_and_nucfav_combined_labeled_gpss.csv"
df = pd.read_csv(file_path, low_memory=False)
valid_responses = ['Favor', 'Oppose']
df_clean = df[df['fav_nuclear'].isin(valid_responses)].copy()
df_clean['favor_nuclear_bin'] = df_clean['fav_nuclear'].apply(lambda x: 1 if x == 'Favor' else 0)
df_clean = df_clean.dropna(subset=['age', 'educ', 'party', 'yr'])
df_clean = df_clean[(df_clean['educ'] != 'DK/REF') & (df_clean['party'] != 'DK')]
bins = [0, 30, 45, 60, 150]
labels = ['18-29', '30-44', '45-59', '60+']
df_clean['age_group'] = pd.cut(df_clean['age'], bins=bins, labels=labels, right=False)

df_clean['age_18_29'] = (df_clean['age_group'] == '18-29').astype(int)
df_clean['age_30_44'] = (df_clean['age_group'] == '30-44').astype(int)
df_clean['age_45_59'] = (df_clean['age_group'] == '45-59').astype(int)

def map_party(p):
    if p in ['Democrat', 'Lean Democratic']: return 'Democrat'
    elif p in ['Republican', 'Lean Republican']: return 'Republican'
    else: return 'Independent'
df_clean['party_grouped'] = df_clean['party'].apply(map_party)

df_clean['educ_Some_college'] = (df_clean['educ'] == 'Some college').astype(int)
df_clean['educ_College_Grad'] = (df_clean['educ'] == 'College Grad only').astype(int)
df_clean['educ_Post_grad'] = (df_clean['educ'] == 'Post-grad').astype(int)

df_clean['party_Democrat'] = (df_clean['party_grouped'] == 'Democrat').astype(int)
df_clean['party_Republican'] = (df_clean['party_grouped'] == 'Republican').astype(int)

predictors = [
    'age_18_29', 'age_30_44', 'age_45_59', 
    'educ_Some_college', 'educ_College_Grad', 'educ_Post_grad',
    'party_Democrat', 'party_Republican'
]


train_pool, _ = train_test_split(df_clean, test_size=0.2, random_state=42, stratify=df_clean['yr'])

eras = {
    "2000-2010": train_pool[(train_pool['yr'] >= 2000) & (train_pool['yr'] <= 2010)],
    "2011-2017": train_pool[(train_pool['yr'] >= 2011) & (train_pool['yr'] <= 2017)],
    "2018-2025": train_pool[(train_pool['yr'] >= 2018) & (train_pool['yr'] <= 2025)]
}

importance_data = []

for era_label, era_df in eras.items():
    if len(era_df) > 0:
        model = LogisticRegression(max_iter=1000, class_weight='balanced').fit(era_df[predictors], era_df['favor_nuclear_bin'])
        coefs = model.coef_[0]
        
        for i, feature in enumerate(predictors):
            importance_data.append({
                'Era': era_label,
                'Factor': feature,
                'Impact': coefs[i]
            })

df_results = pd.DataFrame(importance_data)
plt.figure(figsize=(14, 8))
sns.barplot(data=df_results, x='Factor', y='Impact', hue='Era')
plt.axhline(0, color='black', linewidth=1.5, linestyle='-')
plt.title("Evolution of Factors Influencing Nuclear Favorability (2000-2025)", fontsize=16)
plt.ylabel("Strength of Impact (Coefficient vs. Ref: 60+, HS or Less, Independent)", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend(title="Era")
plt.tight_layout()
plt.savefig("factor_importance_trends_updated.png", dpi=300)
plt.show()