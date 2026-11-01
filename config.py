# Shared by train_models.py and app.py
# To add a new degree group: add one block here, then run train_models.py again.

GROUPS = {
    "Computer / IT": {
        "slug": "cs_it",
        "degrees": [
            "B.Sc Computer Science", "BCA", "B.Sc Information Technology",
            "B.Sc Data Science", "B.Tech CSE", "B.Tech IT", "B.Tech AI & DS",
            "B.E CSE", "B.E IT", "MCA", "M.Sc Computer Science", "M.Tech CSE",
        ],
        "domains": {
            "Web Development": ["HTML_CSS", "JavaScript", "Java"],
            "Data Science": ["Python", "SQL", "Cpp"],
            "Artificial Intelligence": ["Python", "Machine_Learning", "Cpp"],
            "Cloud Computing": ["Cloud", "Linux", "Java", "Python"],
        },
    },
    "Mechanical / Manufacturing": {
        "slug": "mech",
        "degrees": ["B.E Mechanical", "B.E Automobile","B.Sc Manufacturing Science", "B.E Mechatronics",
                    "B.E Production", "B.Tech Mechanical", "M.E Mechanical"],
        "domains": {
            "Design Engineering": ["AutoCAD", "SolidWorks", "CATIA"],
            "Manufacturing & Production": ["CNC", "Manufacturing", "ThreeD_Printing"],
            "Thermal Engineering": ["Thermodynamics", "Ansys", "MATLAB"],
            "Automotive Engineering": ["CATIA", "Ansys", "Manufacturing", "Thermodynamics"],
        },
    },
    "Electrical / Electronics": {
        "slug": "ece",
        "degrees": ["B.E ECE", "B.E EEE", "B.E E&I", "B.E Biomedical",
                    "B.Tech ECE", "B.Tech EEE", "M.E VLSI / Embedded"],
        "domains": {
            "Embedded Systems": ["Embedded_C", "Arduino", "IoT"],
            "Industrial Automation": ["PLC", "MATLAB", "Circuit_Design"],
            "VLSI Design": ["VLSI", "Circuit_Design", "PCB_Design"],
            "IoT & Robotics": ["IoT", "Arduino", "Python"],
        },
    },
    "Civil / Architecture": {
        "slug": "civil",
        "degrees": ["B.E Civil", "B.Tech Civil", "B.Arch", "M.E Structural Engg"],
        "domains": {
            "Structural Design": ["STAAD_Pro", "AutoCAD", "Concrete_Tech"],
            "Construction Management": ["Project_Planning", "Primavera", "Estimation"],
            "BIM & Architecture": ["Revit", "AutoCAD", "Project_Planning"],
            "Surveying & GIS": ["Surveying", "GIS", "AutoCAD"],
        },
    },
    "Commerce / Business": {
        "slug": "commerce",
        "degrees": ["B.Com", "B.Com CA", "BBA", "B.A Economics", "M.Com", "MBA"],
        "domains": {
            "Accounting & Taxation": ["Tally", "Accounting", "Taxation"],
            "Financial Analysis": ["Excel", "Finance", "Data_Analysis"],
            "Digital Marketing": ["Digital_Marketing", "SEO", "Communication"],
            "Business Analytics": ["Excel", "Data_Analysis", "Communication"],
        },
    },
    "Science / Biotech": {
        "slug": "biotech",
        "degrees": ["B.Sc Biotechnology", "B.Tech Biotechnology", "B.Sc Microbiology",
                    "B.Sc Chemistry", "B.Sc Biochemistry", "M.Sc Biotechnology"],
        "domains": {
            "Molecular Biology": ["PCR", "Lab_Techniques", "Cell_Culture"],
            "Bioinformatics": ["Bioinformatics", "Python", "R"],
            "Microbiology & Quality Control": ["Microbiology", "Lab_Techniques", "Research_Writing"],
            "Clinical Research": ["Research_Writing", "Data_Analysis", "Lab_Techniques"],
        },
    },
}

LABELS = {"Cpp": "C++", "HTML_CSS": "HTML/CSS", "ThreeD_Printing": "3D Printing",
          "Embedded_C": "Embedded C", "STAAD_Pro": "STAAD Pro"}

ICONS = {
    # CS / IT
    "Python": "🐍", "Java": "☕", "Cpp": "⚡", "SQL": "🗄️", "HTML_CSS": "🌐",
    "JavaScript": "📜", "Cloud": "☁️", "Linux": "🐧", "Machine_Learning": "🤖",
    # Mechanical
    "AutoCAD": "📐", "SolidWorks": "🧊", "CATIA": "✈️", "CNC": "⚙️",
    "Manufacturing": "🏭", "ThreeD_Printing": "🖨️", "Thermodynamics": "🔥",
    "Ansys": "📊", "MATLAB": "🧮",
    # Electrical / Electronics
    "Embedded_C": "💾", "Arduino": "🔌", "IoT": "📡", "PLC": "🎛️",
    "VLSI": "🔬", "Circuit_Design": "🔧", "PCB_Design": "🟩",
    # Civil
    "STAAD_Pro": "🏗️", "Revit": "🏢", "Surveying": "🧭", "Estimation": "🧾",
    "Project_Planning": "🗓️", "Primavera": "📅", "Concrete_Tech": "🧱", "GIS": "🗺️",
    # Commerce
    "Excel": "📗", "Tally": "📒", "Accounting": "💰", "Finance": "💹",
    "Digital_Marketing": "📣", "SEO": "🔍", "Communication": "💬",
    "Taxation": "🏛️", "Data_Analysis": "📈",
    # Biotech
    "PCR": "🧪", "Lab_Techniques": "🥼", "Bioinformatics": "🧬", "R": "📉",
    "Cell_Culture": "🧫", "Research_Writing": "📝", "Microbiology": "🦠",
}


def label_icon(skill):
    return f"{ICONS.get(skill, '🔹')} {label(skill)}"


def label(skill):
    return LABELS.get(skill, skill.replace("_", " "))


def group_skills(group):
    """Ordered unique skills of a group."""
    seen = []
    for skills in group["domains"].values():
        for s in skills:
            if s not in seen:
                seen.append(s)
    return seen