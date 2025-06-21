import streamlit as st
import base64
from data_processor import get_rarity_color, format_stat_value, get_weapon_image_path
from database import initialize_database, get_weapons_from_db, get_categories_from_db, get_rarities_from_db, get_weapon_stats_from_db

def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Configure page
st.set_page_config(
    page_title="Tacticool 5v5 - Weapon Stats",
    page_icon="🔫",
    layout="wide"
)

# Initialize database on first run
@st.cache_data
def init_db():
    initialize_database()
    return True

# Load weapon data from database
@st.cache_data
def load_data():
    return get_categories_from_db()

init_db()
categories = load_data()

# App title and description
st.title("🔫 Tacticool 5v5 - Weapon Stats")
st.markdown("**Visualize and organize weapon statistics by category and rarity**")

# Sidebar for category selection
st.sidebar.title("Weapon Categories")
selected_category = st.sidebar.selectbox("Select Category", categories)

# Sidebar for rarity filter
st.sidebar.subheader("Filter by Rarity")
all_rarities = get_rarities_from_db()
rarity_options = ["All"] + sorted(all_rarities)
selected_rarity = st.sidebar.selectbox("Select Rarity", rarity_options)

# Search functionality
st.sidebar.subheader("Search Weapons")
search_term = st.sidebar.text_input("Search by weapon name", "")

# Main content
st.header(f"📂 {selected_category}")

# Filter weapons based on selected category and rarity
filtered_weapons = get_weapons_from_db(
    category=selected_category,
    rarity=selected_rarity if selected_rarity != "All" else None,
    search_term=search_term if search_term else None
)

# Display weapons count
st.markdown(f"**Showing {len(filtered_weapons)} weapons**")

if not filtered_weapons:
    st.warning("No weapons found matching your criteria.")
else:
    # Group weapons by rarity for better organization
    weapons_by_rarity = {}
    for weapon in filtered_weapons:
        rarity = weapon['raridade']
        if rarity not in weapons_by_rarity:
            weapons_by_rarity[rarity] = []
        weapons_by_rarity[rarity].append(weapon)
    
    # Display weapons by rarity
    rarity_order = ["Comum", "Incomum", "Raro", "Epico"]
    
    for rarity in rarity_order:
        if rarity in weapons_by_rarity:
            st.subheader(f"🎯 {rarity} ({len(weapons_by_rarity[rarity])} weapons)")
            
            # Create columns for weapon cards
            cols = st.columns(2)
            
            for idx, weapon in enumerate(weapons_by_rarity[rarity]):
                col = cols[idx % 2]
                
                with col:
                    # Create weapon card
                    rarity_color = get_rarity_color(weapon['raridade'])
                    
                    with st.container():
                        # Check for weapon image
                        image_path = get_weapon_image_path(weapon['nome'], weapon['categoria'])
                        
                        # Display weapon header with rarity
                        st.markdown(f"""
                        <div style="
                            border: 2px solid {rarity_color};
                            border-radius: 10px;
                            padding: 15px;
                            margin: 10px 0;
                            background-color: rgba(255,255,255,0.05);
                        ">
                            <h3 style="color: {rarity_color}; margin: 0 0 10px 0;">{weapon['nome']}</h3>
                            <p style="margin: 5px 0; color: {rarity_color}; font-size: 16px;">🏆 {weapon['raridade']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display large weapon image
                        if image_path:
                            st.markdown(f"""
                            <div style="display: flex; justify-content: center; margin: 20px 0;">
                                <div style="width: 250px; height: 250px; border-radius: 10px; overflow: hidden; border: 3px solid {rarity_color};">
                                    <img src="data:image/png;base64,{get_base64_image(image_path)}" 
                                         style="width: 100%; height: 100%; object-fit: cover;" 
                                         alt="{weapon['nome']}">
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="display: flex; justify-content: center; margin: 20px 0;">
                                <div style='width: 250px; height: 250px; background-color: {rarity_color}; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 24px;'>{weapon['nome'][:2]}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Display weapon stats
                        stats = weapon['stats']
                        
                        # Create two columns for stats
                        stat_col1, stat_col2 = st.columns(2)
                        
                        with stat_col1:
                            st.markdown("**🔥 Combat Stats**")
                            st.write(f"• **Damage:** {format_stat_value(stats.get('dano'))}")
                            if stats.get('dano_melee') is not None:
                                st.write(f"• **Melee Damage:** {format_stat_value(stats.get('dano_melee'))}")
                            if stats.get('municao') is not None:
                                st.write(f"• **Ammo:** {format_stat_value(stats.get('municao'))}")
                            if stats.get('cadencia_de_tiro') is not None:
                                st.write(f"• **Fire Rate:** {format_stat_value(stats.get('cadencia_de_tiro'))}")
                        
                        with stat_col2:
                            st.markdown("**🎯 Performance Stats**")
                            if stats.get('precisao') is not None:
                                st.write(f"• **Accuracy:** {format_stat_value(stats.get('precisao'))}")
                            st.write(f"• **Range:** {format_stat_value(stats.get('alcance'))}")
                            st.write(f"• **Speed:** {format_stat_value(stats.get('velocidade_personagem'))}")
                            if stats.get('tempo_recarga') is not None:
                                st.write(f"• **Reload Time:** {format_stat_value(stats.get('tempo_recarga'))}s")
                        
                        # Display special stats if available
                        special_stats = []
                        if stats.get('bleed') is not None:
                            special_stats.append(f"🩸 Bleed: {format_stat_value(stats.get('bleed'))}")
                        if stats.get('burn') is not None:
                            special_stats.append(f"🔥 Burn: {format_stat_value(stats.get('burn'))}")
                        if stats.get('fuel') is not None:
                            special_stats.append(f"⛽ Fuel: {format_stat_value(stats.get('fuel'))}")
                        
                        if special_stats:
                            st.markdown("**✨ Special Effects**")
                            for special in special_stats:
                                st.write(f"• {special}")
                        
                        st.markdown("---")

# Statistics section
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Category Stats")

category_stats = get_weapon_stats_from_db()

# Display category stats
if selected_category in category_stats:
    stats = category_stats[selected_category]
    st.sidebar.markdown(f"**{selected_category}**: {stats['total']} weapons")
    for rarity, count in stats['rarities'].items():
        color = get_rarity_color(rarity)
        st.sidebar.markdown(f"<span style='color: {color}'>• {rarity}: {count}</span>", 
                          unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**Tacticool 5v5 Weapon Database** | Data extracted from game files")
