import csv
import json

def csv_to_json(csv_file, json_file):
    novels = []
    
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            novel = {
                "title": row["novel_titles"].strip(),
                "url": row["url"],
                "rating": int(round(float(row["review_ratings"]))),
                "chapters": int(row["num_chapters"]),
                "author": row["author"].strip(),
                "translator": row["translator"].strip(),
                "genres": [g.strip() for g in row["genres"].split(";")],
            }
            novels.append(novel)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(novels, f, indent=2, ensure_ascii=False)

csv_to_json("data/complete_data.csv", "novels.json")
