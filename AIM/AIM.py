import pandas as pd
from dowhy import CausalModel
import matplotlib.pyplot as plt
import networkx as nx

# ==================== 1. Loading the Data ====================
print("Loading cleaned data...")

df = pd.read_csv("nhanes_cleaned.csv")
print(f"Dataset shape: {df.shape}")
print("\nChecking missing values:")
print(df.isnull().sum())

# ==================== 2. Convert BMI to binary treatment (Obese) ====================
df["Obese"] = (df["BMI"] >= 30).astype(int)   # 1 = obese, 0 = not obese
print(f"Obesity rate in sample: {df['Obese'].mean():.1%}")
print(f"T2D rate in sample: {df['T2D'].mean():.1%}")



# ==================== 3. Define the Causal Graph ====================
print("\nCreating causal graph...")

causal_graph = """
digraph {
    Obese -> T2D;
    Age -> Obese; Age -> T2D;
    Sex -> Obese; Sex -> T2D;
    PA -> Obese; PA -> T2D;
    Diet -> Obese; Diet -> T2D;
}
"""

model = CausalModel(
    data=df,
    treatment="Obese",
    outcome="T2D",
    graph=causal_graph
)

# ==================== 4. Draw nice DAG with fixed positions (NetworkX) ====================
print("\nDrawing nice DAG with fixed layout...")

G = nx.DiGraph()
edges = [
    ("Obese", "T2D"),
    ("Age", "Obese"), ("Age", "T2D"),
    ("Sex", "Obese"), ("Sex", "T2D"),
    ("PA", "Obese"), ("PA", "T2D"),
    ("Diet", "Obese"), ("Diet", "T2D")
]
G.add_edges_from(edges)

# Fixed nice positions (left = confounders, middle = Obese, right = T2D)
pos = {
    "Age":  (0, 3),
    "Sex":  (0, 2),
    "PA":   (0, 1),
    "Diet": (0, 0),
    "Obese":(2, 2),
    "T2D":  (2, 1)
}

plt.figure(figsize=(11, 8))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3500,
    node_color="lightblue",
    font_size=13,
    font_weight="bold",
    arrows=True,
    arrowsize=28,
    edge_color="gray",
    linewidths=2
)

plt.title("Causal DAG - Does Obesity Cause Type 2 Diabetes?", fontsize=16, pad=20)
plt.axis("off")
plt.tight_layout()

# Save the image automatically (high quality)
plt.savefig("causal_dag.png", dpi=300, bbox_inches="tight")
print(" Nice DAG saved successfully as: causal_dag.png")

plt.show()

# ==================== 5. Estimate Causal Effect (ATE) ====================
print("\nEstimating causal effect (Average Treatment Effect)...")

identified_estimand = model.identify_effect()
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.propensity_score_weighting",
    target_units="ate"
)

print("\n" + "=" * 70)
print(" Causal Effect Result:")
print(estimate)
print("=" * 70)

print(f"\nInterpretation: Obesity increases T2D probability by approx. {estimate.value:.2%}")

# ==================== 6. Refutation Test ====================
print("\nRunning refutation test (Placebo Treatment)...")

refutation = model.refute_estimate(
    identified_estimand,
    estimate,
    method_name="placebo_treatment_refuter",
    placebo_type="permute"
)
print(refutation)

# ==================== 7. Save Results ====================
with open("causal_results.txt", "w", encoding="utf-8") as f:
    f.write(str(estimate))
    f.write("\n\nRefutation Result:\n")
    f.write(str(refutation))

print("\n Results saved to file: causal_results.txt")
