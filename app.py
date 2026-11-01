import time
import joblib
import pandas as pd
import streamlit as st

from config import GROUPS, label, label_icon

st.set_page_config(page_title="Internship Recommender", page_icon="🎯", layout="wide")

# ============================================================
# Per-degree-field background theme: a soft gradient + a large
# faint watermark icon, so the page "feels" different per field
# without hotlinking external photos (broken links / copyright).
# ============================================================
FIELD_BG = {
    "cs_it":      {"icon": "💻⌨️", "from": "#EEF2FF", "to": "#FDF2F8"},
    "mech":       {"icon": "⚙️🏭", "from": "#FFF7ED", "to": "#F6F5FB"},
    "ece":        {"icon": "🔌⚡", "from": "#FEFCE8", "to": "#F6F5FB"},
    "civil":      {"icon": "🏗️👷", "from": "#F0F9FF", "to": "#F6F5FB"},
    "commerce":   {"icon": "💼 ", "from": "#ECFDF5", "to": "#F6F5FB"},
    "biotech":    {"icon": "🧬", "from": "#F0FDFA", "to": "#F6F5FB"},
}

# ============================================================
# BASE THEME — fonts, buttons, cards (same for every field)
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; }

    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; position: relative; z-index: 1;}

    h1, h2, h3, h4 { font-family: 'Plus Jakarta Sans', sans-serif; color: #1E1B2E; }
    h3 { font-weight: 700 !important; }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6D28D9, #DB2777);
        color: white; font-weight: 600; font-size: 16px; border-radius: 12px;
        padding: 12px 24px; border: none; transition: all 0.25s ease;
        box-shadow: 0 4px 14px rgba(109, 40, 217, 0.25);
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        background: linear-gradient(135deg, #5B21B6, #BE185D);
        box-shadow: 0 8px 20px rgba(109, 40, 217, 0.35); color: white;
    }

    div[data-testid="stSelectbox"], div[data-testid="stNumberInput"] {
        background: #FFFFFF; border-radius: 12px; padding: 2px 2px;
    }
    div[data-testid="stCheckbox"] label {
        background: #FFFFFF; border: 1px solid #E9E5F5; border-radius: 10px;
        padding: 8px 12px; width: 100%; transition: all .2s ease;
    }
    div[data-testid="stCheckbox"] label:hover { border-color: #C4B5FD; background: #FAF9FF; }

    hr { border-color: #E9E5F5 !important; }
    </style>
""", unsafe_allow_html=True)


# ---------- helpers ----------
@st.cache_resource(show_spinner=False)
def load_bundle(slug):
    try:
        return joblib.load(f"models/{slug}.pkl")
    except FileNotFoundError:
        return None


def reset_profile():
    for k in list(st.session_state.keys()):
        if k.startswith("w_") and k != "w_group":
            del st.session_state[k]
    st.session_state.pop("result", None)


def clear_result():
    st.session_state.pop("result", None)


def conf_bar(name, pct, top=False):
    fill = "linear-gradient(90deg,#6D28D9,#DB2777)" if top else "#C7C2DB"
    name_color = "#1E1B2E" if top else "#6B7280"
    return (
        '<div style="margin-bottom:16px">'
        f'<div style="display:flex;justify-content:space-between;font-weight:600;color:{name_color};margin-bottom:5px;font-size:14px">'
        f'<span>{name}</span><span>{pct}%</span></div>'
        '<div style="background:#EFEAFB;border-radius:999px;height:10px">'
        f'<div style="width:{pct}%;background:{fill};height:10px;border-radius:999px"></div>'
        '</div></div>'
    )


# ---------- header ----------
st.markdown("""
<div style="background: linear-gradient(135deg, #6D28D9 0%, #9333EA 55%, #DB2777 100%); padding: 38px 24px;
     border-radius: 20px; text-align: center; margin-bottom: 32px; position: relative; z-index: 1;
     box-shadow: 0 14px 30px rgba(109, 40, 217, 0.25);">
  <h1 style="color: white; font-size: 36px; margin: 0; font-weight: 800; letter-spacing: -0.5px;">
    🎯 Skill-Based Internship Recommendation System</h1>
  <p style="color: #F3E8FF; font-size: 17px; margin-top: 10px; font-weight: 500;">
    Discover suitable internship domains based on your skills and academic profile.</p>
</div>
""", unsafe_allow_html=True)

# ---------- academic profile ----------
st.markdown("### 🎓 Academic Profile")

group_name = st.selectbox("Select your degree field", list(GROUPS.keys()),
                          key="w_group", on_change=clear_result)
group = GROUPS[group_name]
slug = group["slug"]

# ---------- apply this field's background theme ----------
theme = FIELD_BG[slug]
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(160deg, {theme['from']} 0%, {theme['to']} 100%);
    }}
    .stApp::before {{
        content: "{theme['icon']}";
        position: fixed;
        font-size: 320px;
        line-height: 1;
        opacity: 0.07;
        right: -70px;
        bottom: -90px;
        white-space: nowrap;
        z-index: 0;
        pointer-events: none;
    }}
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    degree = st.selectbox("Select your degree", group["degrees"] + ["Other"], key=f"w_degree_{slug}")
    if degree == "Other":
        degree = st.text_input("Enter your degree", key=f"w_degree_other_{slug}") or "your degree"
    cgpa = st.number_input("Enter your CGPA", min_value=0.0, max_value=10.0, step=0.1, key="w_cgpa")

with col2:
    specialization = st.selectbox(
        "Select your specialization",
        ["No Specialization"] + list(group["domains"].keys()) + ["Other"],
        key=f"w_spec_{slug}")
    if specialization == "Other":
        specialization = st.text_input("Enter your specialization", key=f"w_spec_other_{slug}") or "No Specialization"
    projects = st.number_input("Enter number of projects", min_value=0, max_value=20, step=1, key="w_projects")

st.markdown("---")

# ---------- skills (dynamic per degree group) ----------
st.markdown("### 💻 Skills Known")
skills_all = list(dict.fromkeys(s for v in group["domains"].values() for s in v))
cols = st.columns(3)
selected = {}
for i, s in enumerate(skills_all):
    with cols[i % 3]:
        selected[s] = st.checkbox(label_icon(s), key=f"w_{slug}_{s}")

st.markdown("<br>", unsafe_allow_html=True)

# ---------- predict ----------
if st.button("✨ Recommend Internship Domain"):
    chosen = [s for s, v in selected.items() if v]
    bundle = load_bundle(slug)

    if bundle is None:
        st.error("Model not found. Run `python train_models.py` first.")
    elif not chosen:
        st.error("⚠️ Please select at least one skill.")
    elif cgpa <= 0:
        st.error("⚠️ Please enter your CGPA.")
    elif len(chosen) == 1:
        st.warning(f"⚠️ **{label(chosen[0])}** is useful across multiple domains. "
                   "Please select at least one more skill for a specific recommendation.")
    else:
        with st.spinner("🔍 Analyzing your skills and academic profile..."):
            time.sleep(1.5)
            row = {s: int(v) for s, v in selected.items()}
            row.update({"CGPA": cgpa, "Projects": projects,
                        "Project_Strength": int(projects >= 3),
                        "Academic_Strength": int(cgpa >= 8.0)})
            X = pd.DataFrame([row])[bundle["features"]]   # same column order as training
            model = bundle["model"]
            proba = model.predict_proba(X)[0]
            ranked = sorted(zip(model.classes_, proba), key=lambda t: t[1], reverse=True)

        st.session_state["result"] = {
            "group": group_name, "ranked": ranked[:3], "chosen": chosen,
            "degree": degree, "spec": specialization, "cgpa": cgpa, "projects": projects,
        }

# ---------- results ----------
res = st.session_state.get("result")
if res and res["group"] == group_name:
    ranked = res["ranked"]
    primary = ranked[0][0]
    core = group["domains"][primary]
    have = [label(s) for s in core if s in res["chosen"]]
    missing = [label(s) for s in core if s not in res["chosen"]]

    st.markdown("---")
    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#ECFDF5,#F0FDFA);border:1px solid #A7F3D0;'
            'padding:22px;border-radius:16px;margin-bottom:20px;box-shadow:0 4px 14px rgba(16,185,129,0.12);">'
            f'<h3 style="color:#065F46;margin:0;font-size:22px;">🎯 Recommended Domain: <strong>{primary}</strong></h3>'
            '</div>', unsafe_allow_html=True)

        st.markdown(f"#### 💡 Why {primary}?")

        if res["spec"] == "No Specialization":
            st.write(f"🎓 You are pursuing **{res['degree']}**.")
        else:
            st.write(f"🎓 You are pursuing **{res['degree']}** with **{res['spec']}** specialization.")

        total = len(core)
        if have:
            st.write(f"💻 You already know **{len(have)} of {total}** core skills for **{primary}**: "
                     f"{', '.join(have)}.")
        else:
            st.write(f"💻 None of the core skills for **{primary}** are selected yet, "
                     "so this is based on your overall skill combination.")

        spec = res["spec"]
        if spec in group["domains"]:
            if spec == primary:
                st.write(f"✅ This matches your **{spec}** specialization, so your studies and skills are aligned.")
            else:
                spec_missing = [label(s) for s in group["domains"][spec] if s not in res["chosen"]]
                msg = (f"ℹ️ Your specialization is **{spec}**, but your selected skills fit "
                       f"**{primary}** better right now.")
                if spec_missing:
                    msg += f" To move towards {spec}, add: **{', '.join(spec_missing)}**."
                st.write(msg)

        cg, pr = res["cgpa"], res["projects"]
        if cg >= 8:
            cg_text = "a strong academic record"
        elif cg >= 7:
            cg_text = "a good academic record"
        else:
            cg_text = "a developing academic record"

        if pr >= 3:
            pr_text = "solid practical experience"
        elif pr >= 1:
            pr_text = "some practical experience (a few more projects will help)"
        else:
            pr_text = "no projects yet (start with a small one)"

        st.write(f"📊 Your **{cg} CGPA** shows {cg_text}, and **{pr} projects** show {pr_text}.")

        if len(ranked) > 1:
            alt, alt_p = ranked[1]
            st.write(f"🔄 You can also consider **{alt}** ({int(round(alt_p * 100))}% match) as a backup option.")

        if missing:
            st.write(f"📚 To strengthen **{primary}**, learn: **{', '.join(missing)}**")

    with right:
        bars = "".join(conf_bar(n, int(round(p * 100)), i == 0) for i, (n, p) in enumerate(ranked))
        st.markdown(
            '<div style="background:#FFFFFF;border:1px solid #E9E5F5;padding:22px;border-radius:16px;'
            'box-shadow:0 4px 14px rgba(109,40,217,0.08);">'
            '<h4 style="color:#4C1D95;margin-top:0;">📊 Top Matches</h4>' + bars + '</div>',
            unsafe_allow_html=True)

    st.markdown(
        '<div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px;padding:14px 18px;'
        'margin-top:18px;color:#1E40AF;font-size:14.5px;">'
        '📝 NOTE: Recommendation is primarily based on skills, with CGPA and projects as supporting factors.</div>',
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🔄 Try Another Profile", key="try_another", on_click=reset_profile)
