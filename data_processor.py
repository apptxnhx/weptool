import json
import re
import os

def extract_json_from_rtf(rtf_content):
    """Extract JSON data from RTF content"""
    # Remove RTF formatting and extract JSON
    # Find the JSON array pattern by looking for [ and ]
    start_idx = rtf_content.find('[')
    end_idx = rtf_content.rfind(']')
    
    if start_idx == -1 or end_idx == -1:
        return []
    
    json_str = rtf_content[start_idx:end_idx + 1]
    
    # Clean up RTF escape characters
    json_str = json_str.replace('\\', '')
    json_str = re.sub(r'\s+', ' ', json_str)
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def load_weapon_files():
    """Load all weapon data from RTF files"""
    weapon_files = {
        'Assault Rifle': 'attached_assets/Assault Rifle_1750355328699.rtf',
        'Machine Gun': 'attached_assets/Machine Gun_1750355328701.rtf',
        'Melee': 'attached_assets/Melee_1750355328701.rtf',
        'Pistol': 'attached_assets/Pistol_1750355328701.rtf',
        'Prototype': 'attached_assets/Prototypes_1750355328701.rtf',
        'Shotgun': 'attached_assets/Shotgun_1750355328702.rtf',
        'SMG': 'attached_assets/SMG_1750355328702.rtf',
        'Sniper Rifle': 'attached_assets/Sniper Rifle_1750355328702.rtf'
    }
    
    weapons_data = {}
    
    for category, file_path in weapon_files.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    weapons = extract_json_from_rtf(content)
                    weapons_data[category] = weapons
                    print(f"Loaded {len(weapons)} weapons from {category}")
            except Exception as e:
                print(f"Error loading {category}: {e}")
                weapons_data[category] = []
        else:
            print(f"File not found: {file_path}")
            weapons_data[category] = []
    
    return weapons_data

def get_weapon_data():
    """Load and process all weapon data"""
    return load_weapon_files()

def get_rarity_color(rarity):
    """Get color for weapon rarity"""
    colors = {
        'Comum': '#808080',      # Gray
        'Incomum': '#0070f3',    # Blue
        'Raro': '#8b5cf6',       # Purple
        'Epico': '#ffd700'       # Gold
    }
    return colors.get(rarity, '#ffffff')

def format_stat_value(value):
    """Format stat values for display"""
    if value is None:
        return "N/A"
    return str(value)

def get_weapon_image_path(weapon_name, category):
    """Get the image path for a weapon"""
    # Clean weapon name for file matching
    clean_name = weapon_name.replace('/', ':')  # Handle special characters
    image_path = f"attached_assets/{category}/{clean_name}.png"
    
    # Check if file exists
    if os.path.exists(image_path):
        return image_path
    
    # Try alternative naming patterns
    alternatives = [
        f"attached_assets/{category}/{weapon_name.upper()}.png",
        f"attached_assets/{category}/{weapon_name.lower()}.png",
        f"attached_assets/{category}/{weapon_name.title()}.png"
    ]
    
    for alt_path in alternatives:
        if os.path.exists(alt_path):
            return alt_path
    
    return None