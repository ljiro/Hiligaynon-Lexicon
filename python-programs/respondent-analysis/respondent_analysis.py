import pandas as pd

# === File path ===
file_path = r"/files/output-files/respondents/NLP Lexicon - lexicon_sample_with_response.csv"

# Load dataset
df = pd.read_csv(file_path)

# Inspect the column names
print("Columns:", df.columns.tolist())

# Assumptions:
# - `comparison` column contains boolean or string ("TRUE"/"FALSE") values
# - Last two columns are `mode` and `comparison`

# Standardize comparison values to Boolean
df['Comparison'] = df['Comparison'].astype(str).str.upper().map({'TRUE': True, 'FALSE': False})

# === Overall agreement rate ===
total = len(df)
matches = df['Comparison'].sum()
mismatches = total - matches
accuracy = matches / total * 100

print(f"\n=== Verification Summary ===")
print(f"Total rows evaluated: {total}")
print(f"Matches (mode == system sentiment): {matches}")
print(f"Mismatches (mode != system sentiment): {mismatches}")
print(f"Agreement rate: {accuracy:.2f}%")

# === Breakdown by sentiment (based on respondent basis) ===
if 'respondent basis' in df.columns:
    breakdown = df.groupby('respondent basis')['comparison'].agg(
        total='count',
        matches='sum'
    )
    breakdown['mismatches'] = breakdown['total'] - breakdown['matches']
    breakdown['accuracy (%)'] = (breakdown['matches'] / breakdown['total']) * 100

    print("\n=== Breakdown by Respondent Basis (system sentiment) ===")
    print(breakdown)

# === Optional: Save detailed mismatch cases for inspection ===
output_mismatches = r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\files\output-files\respondents\mismatches.csv"
df[df['Comparison'] == False].to_csv(output_mismatches, index=False)
print(f"\nMismatched rows saved to: {output_mismatches}")
