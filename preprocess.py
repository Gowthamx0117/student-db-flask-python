import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Step 1: Load the dataset
df = pd.read_csv("students_data.csv")  # Make sure this CSV is in your working directory

# Step 2: Remove duplicates and missing values (if any)
df = df.drop_duplicates()
df = df.dropna()

# Step 3: Ensure proper data types
df['regno'] = df['regno'].astype(int)
df['cgpa'] = df['cgpa'].astype(float)

# Step 4: Encode categorical columns
le_dept = LabelEncoder()
le_arrear = LabelEncoder()

df['dept_encoded'] = le_dept.fit_transform(df['dept'])
df['hist_arrear_encoded'] = le_arrear.fit_transform(df['hist_arrear'])

# Show the encoding maps (optional)
print("Department Encoding Map:", dict(zip(le_dept.classes_, le_dept.transform(le_dept.classes_))))
print("Arrear Encoding Map:", dict(zip(le_arrear.classes_, le_arrear.transform(le_arrear.classes_))))

# Step 5: Feature Engineering
df['placement_eligible'] = (df['cgpa'] > 7.5) & (df['hist_arrear'] == 'No')
df['risk_group'] = df['cgpa'].apply(lambda x: 'High' if x < 6 else 'Low')

# Step 6: Save the cleaned and enriched dataset
df.to_csv("students_cleaned.csv", index=False)

print("✅ Preprocessing complete. File saved as students_cleaned.csv")