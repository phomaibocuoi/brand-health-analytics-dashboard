import pandas as pd
import numpy as np
import os
import re
import csv

print("=" * 80)
print("🚀 DATA ENGINEERING - Transforming survey dataset from Wide to Long Format")
print("=" * 80)

# Paths
PATH_BRAND = 'data_clean/output/Brandlist_cleaned.csv'
PATH_DATA = 'data_clean/output/Dataset_cleaned.csv'
PATH_MAPPING_OUT = 'data_clean/output/column_to_brand_mapping.csv'
PATH_LONG_OUT = 'data_clean/output/Dataset_long_format.csv'

# Step 1: Load files
print("\n📥 Step 1: Loading datasets...")
df_brand = pd.read_csv(PATH_BRAND)
df_data = pd.read_csv(PATH_DATA, low_memory=False)

print(f"   - Brandlist loaded: {len(df_brand)} brands")
print(f"   - Dataset loaded: {df_data.shape[0]:,} rows × {df_data.shape[1]:,} columns")

# Step 2: Sort brand names by length descending to prevent partial matching bugs
print("\n🏷️ Step 2: Preparing brand names list...")
brands = sorted(df_brand['brand_name'].dropna().unique(), key=len, reverse=True)
brand_to_id = dict(zip(df_brand['brand_name'], df_brand['brand_id']))

# Step 3: Match Dataset columns with brands and extract question code / attribute
print("\n🔍 Step 3: Scanning columns and mapping to brands...")
matched_cols = {}
unmatched_cols = []

# Demographic and general columns that should NOT be unpivoted
id_cols = ['serial', 'wave', 'region', 'gender', 'age_group', 'income']

# Also identify general columns that we should keep as index variables (e.g. S2, S3b, TOM, Bumo)
general_survey_cols = []

def extract_column_details(col, brand_name):
    # Split by brand name
    parts = re.split(re.escape(brand_name), col, flags=re.IGNORECASE)
    prefix = parts[0].strip(' -_')
    suffix = parts[1].strip(' -_') if len(parts) > 1 else ''
    
    prefix_lower = prefix.lower()
    
    if 'spontaneous' in prefix_lower:
        q_code = 'Q1.Spontaneous'
    elif 'aided awareness' in prefix_lower:
        q_code = 'Q1Q2.Aided'
    elif 'p3m' in prefix_lower:
        q_code = 'Q3.P3M'
    elif 'p4w' in prefix_lower:
        q_code = 'Q4.P4W'
    elif 'consideration' in prefix_lower or 'q4q8' in prefix_lower:
        q_code = 'Q4Q8.Consideration'
    elif 'qi' in prefix_lower:
        q_code = 'QI.Imagery'
    elif 'qme2' in prefix_lower:
        q_code = 'QME2.Barriers'
    elif 'q_tp1' in prefix_lower:
        q_code = 'Q_TP1.Touchpoints'
    else:
        q_code = prefix
        
    return q_code, suffix

for col in df_data.columns:
    if col in id_cols:
        continue
    
    # Try to match with any of the brand names
    matched_brand = None
    for b in brands:
        if b.lower() in col.lower():
            matched_brand = b
            break
            
    if matched_brand:
        q_code, suffix = extract_column_details(col, matched_brand)
        matched_cols[col] = {
            'brand_id': brand_to_id[matched_brand],
            'brand_name': matched_brand,
            'question_code': q_code,
            'attribute_name': suffix
        }
    else:
        unmatched_cols.append(col)

print(f"   - Matched brand columns: {len(matched_cols)}")
print(f"   - Unmatched/General columns: {len(unmatched_cols)}")

# Step 4: Write mapping table to CSV
print(f"\n📂 Step 4: Saving column-to-brand mapping to '{PATH_MAPPING_OUT}'...")
with open(PATH_MAPPING_OUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['column_name', 'brand_id', 'brand_name', 'question_code', 'attribute_name'])
    for col, info in matched_cols.items():
        writer.writerow([col, info['brand_id'], info['brand_name'], info['question_code'], info['attribute_name']])
print("   - Mapping saved successfully!")

# Step 5: Perform the high-performance Unpivot (Melt)
print("\n🌪️ Step 5: Performing Unpivot (Melt) on brand columns...")

# Demographics + unmatched general survey columns will be kept as ID vars
id_vars = id_cols + unmatched_cols

print(f"   - Index variables (ID vars): {len(id_vars)} columns")
print(f"   - Value variables (to Unpivot): {len(matched_cols)} columns")

# Perform melt
df_long = pd.melt(
    df_data,
    id_vars=id_vars,
    value_vars=list(matched_cols.keys()),
    var_name='column_name',
    value_name='value'
)

print(f"   - Unpivoted dataset shape: {df_long.shape[0]:,} rows × {df_long.shape[1]:,} columns")

# Step 6: Join with the mapping metadata to add brand_id, brand_name, etc.
print("\n🔄 Step 6: Merging with brand mapping metadata...")
df_mapping = pd.DataFrame.from_dict(matched_cols, orient='index').reset_index().rename(columns={'index': 'column_name'})
df_final = pd.merge(df_long, df_mapping, on='column_name', how='inner')

# Drop the messy 'column_name' to keep it extremely clean
df_final = df_final.drop(columns=['column_name'])

print(f"   - Final unpivoted dataset shape: {df_final.shape[0]:,} rows × {df_final.shape[1]:,} columns")
print(f"   - Columns in final dataset: {df_final.columns.tolist()}")

# Step 7: Save to CSV
print(f"\n💾 Step 7: Saving the unified unpivoted dataset to '{PATH_LONG_OUT}'...")
# Save with UTF-8 BOM so Excel/Power BI reads Vietnamese characters perfectly
df_final.to_csv(PATH_LONG_OUT, index=False, encoding='utf-8-sig')

print("=" * 80)
print("🎉 SUCCESS! DATA ENGINEERING COMPLETE!")
print(f"   Unified Fact table: {PATH_LONG_OUT}")
print(f"   Dimensions Mapping: {PATH_MAPPING_OUT}")
print("=" * 80)
