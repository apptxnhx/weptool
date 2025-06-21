import os
import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create database tables"""
    with engine.connect() as conn:
        # Create weapons table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weapons (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                raridade VARCHAR(50) NOT NULL,
                dano INTEGER,
                dano_melee INTEGER,
                municao INTEGER,
                cadencia_de_tiro VARCHAR(100),
                precisao VARCHAR(100),
                alcance DECIMAL(5,2),
                velocidade_personagem INTEGER,
                tempo_recarga VARCHAR(50),
                bleed INTEGER,
                burn INTEGER,
                fuel INTEGER,
                image_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create index for faster queries
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_weapons_categoria ON weapons(categoria);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_weapons_raridade ON weapons(raridade);
        """))
        
        conn.commit()

def insert_weapon_data(weapons_data):
    """Insert weapon data into database"""
    with engine.connect() as conn:
        # Clear existing data
        conn.execute(text("DELETE FROM weapons"))
        
        for category, weapons in weapons_data.items():
            for weapon in weapons:
                stats = weapon.get('stats', {})
                
                # Insert weapon
                conn.execute(text("""
                    INSERT INTO weapons (
                        nome, categoria, raridade, dano, dano_melee, municao,
                        cadencia_de_tiro, precisao, alcance, velocidade_personagem,
                        tempo_recarga, bleed, burn, fuel, image_path
                    ) VALUES (
                        :nome, :categoria, :raridade, :dano, :dano_melee, :municao,
                        :cadencia_de_tiro, :precisao, :alcance, :velocidade_personagem,
                        :tempo_recarga, :bleed, :burn, :fuel, :image_path
                    )
                """), {
                    'nome': weapon['nome'],
                    'categoria': weapon['categoria'],
                    'raridade': weapon['raridade'],
                    'dano': stats.get('dano'),
                    'dano_melee': stats.get('dano_melee'),
                    'municao': stats.get('municao'),
                    'cadencia_de_tiro': str(stats.get('cadencia_de_tiro')) if stats.get('cadencia_de_tiro') is not None else None,
                    'precisao': str(stats.get('precisao')) if stats.get('precisao') is not None else None,
                    'alcance': stats.get('alcance'),
                    'velocidade_personagem': stats.get('velocidade_personagem'),
                    'tempo_recarga': str(stats.get('tempo_recarga')) if stats.get('tempo_recarga') is not None else None,
                    'bleed': stats.get('bleed'),
                    'burn': stats.get('burn'),
                    'fuel': stats.get('fuel'),
                    'image_path': f"attached_assets/{category}/{weapon['nome']}.png"
                })
        
        conn.commit()

def get_weapons_from_db(category=None, rarity=None, search_term=None):
    """Get weapons from database with filters"""
    with engine.connect() as conn:
        query = "SELECT * FROM weapons WHERE 1=1"
        params = {}
        
        if category:
            query += " AND categoria = :category"
            params['category'] = category
        
        if rarity:
            query += " AND raridade = :rarity"
            params['rarity'] = rarity
        
        if search_term:
            query += " AND LOWER(nome) LIKE :search_term"
            params['search_term'] = f"%{search_term.lower()}%"
        
        query += " ORDER BY categoria, raridade, nome"
        
        result = conn.execute(text(query), params)
        weapons = []
        
        for row in result:
            weapon = {
                'id': row.id,
                'nome': row.nome,
                'categoria': row.categoria,
                'raridade': row.raridade,
                'stats': {
                    'dano': row.dano,
                    'dano_melee': row.dano_melee,
                    'municao': row.municao,
                    'cadencia_de_tiro': row.cadencia_de_tiro,
                    'precisao': row.precisao,
                    'alcance': row.alcance,
                    'velocidade_personagem': row.velocidade_personagem,
                    'tempo_recarga': row.tempo_recarga,
                    'bleed': row.bleed,
                    'burn': row.burn,
                    'fuel': row.fuel
                },
                'image_path': row.image_path
            }
            weapons.append(weapon)
        
        return weapons

def get_categories_from_db():
    """Get all weapon categories from database"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT categoria FROM weapons ORDER BY categoria"))
        return [row.categoria for row in result]

def get_rarities_from_db():
    """Get all weapon rarities from database"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT raridade FROM weapons ORDER BY raridade"))
        return [row.raridade for row in result]

def get_weapon_stats_from_db():
    """Get weapon statistics from database"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                categoria,
                raridade,
                COUNT(*) as count
            FROM weapons 
            GROUP BY categoria, raridade 
            ORDER BY categoria, raridade
        """))
        
        stats = {}
        for row in result:
            if row.categoria not in stats:
                stats[row.categoria] = {'total': 0, 'rarities': {}}
            
            stats[row.categoria]['rarities'][row.raridade] = row.count
            stats[row.categoria]['total'] += row.count
        
        return stats

def initialize_database():
    """Initialize database with weapon data"""
    from data_processor import get_weapon_data
    
    # Create tables
    create_tables()
    
    # Load and insert weapon data
    weapons_data = get_weapon_data()
    insert_weapon_data(weapons_data)
    
    print("Database initialized with weapon data")