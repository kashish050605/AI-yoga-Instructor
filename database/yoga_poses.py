import pandas as pd
import json
import os

CACHE_FILE = "database/yoga_cache.json"
CSV_FILE   = "database/yoga_poses.csv"

# Joint angle correction data for key poses
ANGLE_DATA = {
    "Warrior I": {
        "angles": {
            "right_knee":  {"points": (24,26,28), "target": 90,  "tolerance": 20},
            "left_knee":   {"points": (23,25,27), "target": 170, "tolerance": 20},
            "right_elbow": {"points": (12,14,16), "target": 170, "tolerance": 20},
            "left_elbow":  {"points": (11,13,15), "target": 170, "tolerance": 20},
        },
        "corrections": {
            "right_knee":  "Bend your front knee to 90 degrees",
            "left_knee":   "Keep your back leg straight",
            "right_elbow": "Straighten your right arm overhead",
            "left_elbow":  "Straighten your left arm overhead",
        },
        "search_tags": ["legs", "hips", "balance", "strength", "beginner"]
    },
    "Warrior II": {
        "angles": {
            "right_knee":  {"points": (24,26,28), "target": 90,  "tolerance": 20},
            "left_knee":   {"points": (23,25,27), "target": 170, "tolerance": 20},
            "right_elbow": {"points": (12,14,16), "target": 170, "tolerance": 20},
            "left_elbow":  {"points": (11,13,15), "target": 170, "tolerance": 20},
        },
        "corrections": {
            "right_knee":  "Bend your front knee to 90 degrees",
            "left_knee":   "Keep your back leg straight",
            "right_elbow": "Extend right arm straight out",
            "left_elbow":  "Extend left arm straight out",
        },
        "search_tags": ["legs", "arms", "strength", "stamina", "beginner"]
    },
    "Tree Pose": {
        "angles": {
            "right_knee":  {"points": (24,26,28), "target": 45,  "tolerance": 20},
            "left_knee":   {"points": (23,25,27), "target": 170, "tolerance": 15},
            "right_elbow": {"points": (12,14,16), "target": 45,  "tolerance": 20},
            "left_elbow":  {"points": (11,13,15), "target": 45,  "tolerance": 20},
        },
        "corrections": {
            "right_knee":  "Bend right knee, place foot on inner thigh",
            "left_knee":   "Keep standing leg straight",
            "right_elbow": "Bring hands together at chest",
            "left_elbow":  "Bring hands together at chest",
        },
        "search_tags": ["balance", "focus", "legs", "beginner", "stability"]
    },
    "Mountain Pose": {
        "angles": {
            "right_knee":  {"points": (24,26,28), "target": 175, "tolerance": 15},
            "left_knee":   {"points": (23,25,27), "target": 175, "tolerance": 15},
            "right_elbow": {"points": (12,14,16), "target": 175, "tolerance": 15},
            "left_elbow":  {"points": (11,13,15), "target": 175, "tolerance": 15},
        },
        "corrections": {
            "right_knee":  "Straighten your right leg completely",
            "left_knee":   "Straighten your left leg completely",
            "right_elbow": "Keep right arm straight at side",
            "left_elbow":  "Keep left arm straight at side",
        },
        "search_tags": ["posture", "beginner", "standing", "foundation"]
    },
    "Child Pose": {
        "angles": {
            "right_knee":  {"points": (24,26,28), "target": 45,  "tolerance": 25},
            "left_knee":   {"points": (23,25,27), "target": 45,  "tolerance": 25},
            "right_elbow": {"points": (12,14,16), "target": 170, "tolerance": 20},
            "left_elbow":  {"points": (11,13,15), "target": 170, "tolerance": 20},
        },
        "corrections": {
            "right_knee":  "Bend knees more, sit back on heels",
            "left_knee":   "Bend knees more, sit back on heels",
            "right_elbow": "Extend right arm fully forward",
            "left_elbow":  "Extend left arm fully forward",
        },
        "search_tags": ["back pain", "rest", "relaxation", "beginner"]
    },
}

DEFAULT_ANGLES = {
    "angles": {
        "right_knee":  {"points": (24,26,28), "target": 170, "tolerance": 25},
        "left_knee":   {"points": (23,25,27), "target": 170, "tolerance": 25},
        "right_elbow": {"points": (12,14,16), "target": 170, "tolerance": 25},
        "left_elbow":  {"points": (11,13,15), "target": 170, "tolerance": 25},
    },
    "corrections": {
        "right_knee":  "Adjust your right knee position",
        "left_knee":   "Adjust your left knee position",
        "right_elbow": "Adjust your right arm position",
        "left_elbow":  "Adjust your left arm position",
    },
    "search_tags": ["general", "yoga"]
}


def load_from_csv():
    """Load poses from downloaded CSV file"""
    print("📂 Loading poses from CSV...")
    all_poses = {}

    try:
        df = pd.read_csv(CSV_FILE)
        print(f"  Columns found: {list(df.columns)}")

        for _, row in df.iterrows():
            # Try common column names
            name = (row.get("name") or row.get("pose_name") or
                    row.get("Name") or row.get("english_name") or "")
            name = str(name).strip()
            if not name or name == "nan":
                continue

            description = str(row.get("description") or
                              row.get("sanskrit_name") or
                              row.get("benefits") or name)

            benefits = str(row.get("benefits") or
                           row.get("pose_benefits") or
                           "Improves flexibility and strength")

            steps = str(row.get("steps") or
                        row.get("instructions") or
                        row.get("pose_description") or
                        "Follow the pose carefully")

            difficulty = str(row.get("difficulty") or
                             row.get("difficulty_level") or
                             row.get("level") or "Beginner")

            category = str(row.get("category") or
                           row.get("pose_type") or
                           row.get("type") or "general")

            all_poses[name] = {
                "description": description,
                "benefits":    [b.strip() for b in benefits.split(",")],
                "steps":       [s.strip() for s in steps.split(".")
                                if s.strip()],
                "difficulty":  difficulty,
                "category":    category,
                **ANGLE_DATA.get(name, DEFAULT_ANGLES)
            }

        print(f"  ✅ Loaded {len(all_poses)} poses from CSV!")

    except Exception as e:
        print(f"  ❌ CSV error: {e}")

    # Always make sure our 5 key poses are included
    for name, data in ANGLE_DATA.items():
        if name not in all_poses:
            all_poses[name] = {
                "description": f"{name} yoga pose",
                "benefits":    ["Improves flexibility and strength"],
                "steps":       ["Follow the pose instructions carefully"],
                "difficulty":  "Beginner",
                "category":    "standing",
                **data
            }

    # Save to cache
    with open(CACHE_FILE, "w") as f:
        json.dump(all_poses, f, indent=2)
    print(f"✅ Total {len(all_poses)} poses saved to cache!")
    return all_poses


def load_poses():
    """Load from cache if exists, otherwise from CSV"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} poses from cache")
            return data
    return load_from_csv()


# Load on import
YOGA_POSES = load_poses()


def get_all_poses():
    return list(YOGA_POSES.keys())

def get_pose(name):
    return YOGA_POSES.get(name, None)

def search_poses(query):
    query = query.lower()
    results = []
    for pose_name, pose_data in YOGA_POSES.items():
        tags       = pose_data.get("search_tags", [])
        category   = pose_data.get("category", "")
        difficulty = pose_data.get("difficulty", "")
        if (any(query in tag for tag in tags) or
            query in pose_name.lower() or
            query in category.lower() or
            query in difficulty.lower()):
            results.append(pose_name)
    return results

def refresh_poses():
    global YOGA_POSES
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    YOGA_POSES = load_from_csv()
    return YOGA_POSES