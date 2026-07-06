"""
Show comparison: Current index price vs PDF-verified price
So user can confirm before applying
"""
import json

INDEX_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\search_index_v2.json'
CORRECT_PATH = r'C:\Movies\quotation-ai\quotation-ai\backend\finish_prices_correct.json'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)
with open(CORRECT_PATH, 'r', encoding='utf-8') as f:
    pdf = json.load(f)

products = data['stored_items']

SPECIAL = {'BRG','BG','GG','MB','RG'}

print(f"{'BASE':<8} {'FIN':<5} {'CURRENT':>12} {'PDF_CORRECT':>12} {'STATUS'}")
print("-" * 60)

all_ok = True
for base in sorted(pdf.keys()):
    info = pdf[base]
    special_mrp = info.get('special_finish_mrp')
    cp_mrp = info.get('cp_mrp')

    for p in products:
        if str(p.get('base_code','')) != base:
            continue
        finish = str(p.get('variant_code','')).upper()
        current = str(p.get('price',''))

        if finish in SPECIAL and special_mrp:
            correct = str(special_mrp)
        elif finish == 'CP' and cp_mrp:
            correct = str(cp_mrp)
        else:
            continue

        status = "OK" if current == correct else f"WRONG (diff: {int(correct)-int(current):+,})"
        if current != correct:
            all_ok = False
            print(f"{base:<8} {finish:<5} {current:>12} {correct:>12}   {status}")

if all_ok:
    print("All prices already correct!")
else:
    print()
    print("=" * 60)
    print("Above are ALL the corrections needed.")
    print("Confirm these are correct before applying.")
