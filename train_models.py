import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from config import GROUPS, group_skills

np.random.seed(42)  # same dataset every run
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)


def make_data(group, n=800):
    domains = list(group["domains"])
    skills = group_skills(group)
    rows = []
    for i in range(n):
        target = domains[i % len(domains)]      # balanced classes
        core = group["domains"][target]

        # random background skills + most of the target domain's core skills
        row = {s: int(np.random.rand() < 0.25) for s in skills}
        for s in core:
            if np.random.rand() < 0.85:
                row[s] = 1
        if sum(row[s] for s in core) < 2:       # at least 2 core skills
            for s in np.random.choice(core, 2, replace=False):
                row[s] = 1

        cgpa = round(np.random.uniform(6.0, 10.0), 2)
        projects = int(np.random.randint(0, 6))
        row["CGPA"] = cgpa
        row["Projects"] = projects
        row["Project_Strength"] = int(projects >= 3)
        row["Academic_Strength"] = int(cgpa >= 8.0)
        row["Internship_Domain"] = target
        rows.append(row)
    return pd.DataFrame(rows)


for name, group in GROUPS.items():
    df = make_data(group)
    features = group_skills(group) + ["CGPA", "Projects", "Project_Strength", "Academic_Strength"]
    X, y = df[features], df["Internship_Domain"]

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
    model.fit(X_tr, y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))

    # save model together with its feature order
    joblib.dump({"model": model, "features": features}, f"models/{group['slug']}.pkl")
    df.to_csv(f"data/{group['slug']}_dataset.csv", index=False)
    print(f"{name:28s} accuracy = {acc:.2f}  -> models/{group['slug']}.pkl")