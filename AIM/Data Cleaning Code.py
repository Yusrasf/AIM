import pandas as pd

print("Loading original NHANES files...")

# 1. Load the seven original files
demo = pd.read_sas('DEMO_L.xpt', format='xport')
bmx  = pd.read_sas('BMX_L.xpt', format='xport')
diq  = pd.read_sas('DIQ_L.xpt', format='xport')
paq  = pd.read_sas('PAQ_L.xpt', format='xport')
ghb  = pd.read_sas('GHB_L.xpt', format='xport')
glu  = pd.read_sas('GLU_L.xpt', format='xport')
dr1  = pd.read_sas('DR1TOT_L.xpt', format='xport')

print("All files loaded successfully!")

# 2. Merge all files
df = (demo.merge(bmx[['SEQN', 'BMXBMI']], on='SEQN', how='inner')
         .merge(diq[['SEQN', 'DIQ010']], on='SEQN', how='inner')
         .merge(paq[['SEQN', 'PAD800']], on='SEQN', how='inner')
         .merge(ghb[['SEQN', 'LBXGH']], on='SEQN', how='inner')
         .merge(glu[['SEQN', 'LBXGLU']], on='SEQN', how='inner')
         .merge(dr1[['SEQN', 'DR1TKCAL']], on='SEQN', how='inner'))

print(f"Number of rows after merging: {df.shape[0]:,}")

# 3. Create the important variables
df['BMI']   = df['BMXBMI']
df['Obese'] = (df['BMI'] >= 30).astype(int)      # Treatment variable
df['Age']   = df['RIDAGEYR']
df['Sex']   = df['RIAGENDR']
df['PA']    = df['PAD800']
df['Diet']  = df['DR1TKCAL']

# Define the outcome variable (T2D)
df['T2D'] = ((df['DIQ010'] == 1) |
             (df['LBXGH'] >= 6.5) |
             (df['LBXGLU'] >= 126)).astype(int)

# 4. Final cleaning (remove rows with missing values in important columns)
df = df.dropna(subset=['BMI', 'T2D', 'Age', 'Sex', 'PA', 'Diet'])

print(f"Number of rows after cleaning: {df.shape[0]:,}")
print(f"Obesity rate: {df['Obese'].mean():.1%}")
print(f"T2D rate: {df['T2D'].mean():.1%}")

# 5. Save the cleaned dataset
df.to_csv('nhanes_cleaned.csv', index=False)
print("Cleaned dataset saved successfully as: nhanes_cleaned.csv")