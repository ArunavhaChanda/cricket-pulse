#!/usr/bin/env python3
"""
populate_locations.py - Populate Location table with data from simengine/locations.py
Usage: python populate_locations.py
"""

from app import create_app, db
from models import Location
from simengine.locations import get_all_locations

def populate_locations():
    """Populate Location table with data from simengine/locations.py"""
    
    # Create app instance
    app = create_app()
    
    with app.app_context():
        # Get location data from simengine
        locations_dict = get_all_locations()
        
        # Ground multipliers from locations.py (Aggression, Spin, Pace)
        ground_multipliers = {
            "NYC": (1.01, 1.02, 0.99),
            "MEL": (0.94, 0.95, 1.04),
            "LON": (0.95, 0.96, 1.03),
            "BKK": (1.00, 1.03, 0.97),
            "PAR": (1.03, 0.95, 1.00),
            "CHI": (0.99, 0.98, 1.02),
            "DUB": (0.97, 0.98, 1.00),
            "SIN": (1.05, 1.04, 0.98),
            "KOL": (0.99, 1.03, 0.97),
            "JOH": (1.00, 0.98, 1.02),
            "AUC": (1.03, 0.95, 1.00),
            "DHA": (1.01, 1.04, 0.99),
            "BRI": (1.06, 1.02, 0.98),
            "SEO": (1.01, 1.01, 1.01),
            "SAN": (1.03, 1.03, 0.97),
            "CAP": (1.00, 0.98, 1.02),
            "IST": (0.99, 1.01, 1.00),
            "LA": (1.10, 0.92, 0.93),
            "TOR": (0.87, 0.97, 0.98),
            "TOK": (0.76, 0.92, 0.93),
            "KAT": (0.55, 1.03, 1.01),
            "AHM": (0.99, 0.96, 0.98),
            "LAH": (0.95, 1.03, 0.99),
            "HYD": (1.05, 0.98, 1.00),
            "CHN": (1.02, 1.03, 0.97),
            "MUM": (0.97, 1.01, 1.02),
            "DEL": (0.98, 1.02, 0.99),
            "MOH": (1.00, 0.99, 1.00),
            "JAI": (0.99, 1.00, 1.00),
            "LUC": (1.00, 1.00, 1.00)
        }
        
        
        created_count = 0
        updated_count = 0
        
        for short_code, name in locations_dict.items():
            # Get multipliers (default to 1.0 if not found)
            multipliers = ground_multipliers.get(short_code, (1.0, 1.0, 1.0))
            aggression_mult, spin_mult, pace_mult = multipliers
            
            # Check if location already exists
            existing_location = Location.query.filter_by(short_code=short_code).first()
            
            if existing_location:
                # Update existing location
                existing_location.name = name
                existing_location.aggression_multiplier = aggression_mult
                existing_location.spin_multiplier = spin_mult
                existing_location.pace_multiplier = pace_mult
                updated_count += 1
                print(f"Updated: {short_code} - {name}")
            else:
                # Create new location
                location = Location(
                    name=name,
                    short_code=short_code,
                    aggression_multiplier=aggression_mult,
                    spin_multiplier=spin_mult,
                    pace_multiplier=pace_mult
                )
                db.session.add(location)
                created_count += 1
                print(f"Created: {short_code} - {name}")
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully populated locations!")
            print(f"   Created: {created_count} locations")
            print(f"   Updated: {updated_count} locations")
            return True
        except Exception as e:
            print(f"\n❌ Error committing locations: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    populate_locations()

