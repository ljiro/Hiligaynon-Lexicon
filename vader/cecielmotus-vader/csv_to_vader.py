import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path

# Input/output paths
csv_input = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\output_parsed.csv")
lexicon_output = Path(r"C:\Users\CODE CLASSES\nlp\Hiligaynon-Lexicon\output\vader_hiligaynon_lexicon.txt")

# Load the parsed CSV
df = pd.read_csv(csv_input)

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

lexicon_entries = []

for _, row in df.iterrows():
    word = str(row["word"]).strip()
    meaning = str(row.get("meaning", "")).strip()

    if not word or not meaning:
        continue  # skip empty rows

    # Get sentiment score from the meaning column
    score = analyzer.polarity_scores(meaning)["compound"]

    # Format: word <tab> score <tab> 0.0 <tab> 0.0
    lexicon_entries.append(f"{word}\t{score:.3f}\t0.0\t0.0")

# Save custom lexicon
lexicon_output.parent.mkdir(parents=True, exist_ok=True)
with open(lexicon_output, "w", encoding="utf-8") as f:
    f.write("\n".join(lexicon_entries))

print(f"✅ Custom Hiligaynon VADER lexicon created: {lexicon_output}")
