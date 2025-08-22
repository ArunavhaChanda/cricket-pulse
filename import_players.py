#!/usr/bin/env python3
"""
import_players.py - Import players from CSV to database (Fixed Version)
Usage: python import_players.py <csv_file_path>
"""

import sys
import csv
import os

def import_players_from_csv(csv_file_path):
    """Import players from CSV file into database using existing app structure"""
    
    # Import your existing app structure
    try:
        from app import create_app, db
        print("✅ Using existing app structure")
    except ImportError:
        print("❌ Error: Could not import app.py")
        print("Make sure app.py exists and has create_app() and db defined")
        return False
    
    # Import models
    try:
        from models import Team, Player
        print("✅ Models imported successfully")
    except ImportError:
        print("❌ Error: Could not import models.py")
        print("Make sure models.py exists in the same directory")
        return False
    
    # Create app instance
    app = create_app()
    
    with app.app_context():
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                imported_count = 0
                errors = []
                created_teams = set()
                
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        # Extract team and player data
                        team_name = row.get('team_name', '').strip()
                        team_short = row.get('team_short', '').strip()
                        player_name = row.get('name', '').strip()
                        
                        if not team_name or not team_short or not player_name:
                            errors.append(f"Row {row_num}: Missing required fields (team_name, team_short, name)")
                            continue
                        
                        # Validate team_short length
                        if len(team_short) > 4:
                            errors.append(f"Row {row_num}: team_short must be less than 5 characters")
                            continue
                        
                        # Find or create team
                        team = Team.query.filter_by(short_name=team_short.upper()).first()
                        if not team:
                            team = Team(
                                full_name=team_name,
                                short_name=team_short.upper()
                            )
                            db.session.add(team)
                            db.session.flush()  # Get the team ID
                            created_teams.add(f"{team_name} ({team_short.upper()})")
                        
                        # Check if team already has 11 players
                        current_player_count = Player.query.filter_by(team_id=team.id).count()
                        if current_player_count >= 11:
                            errors.append(f"Row {row_num}: Team {team_short} already has 11 players")
                            continue
                        
                        # Check if player already exists in team
                        existing_player = Player.query.filter_by(
                            team_id=team.id, 
                            name=player_name
                        ).first()
                        
                        if existing_player:
                            errors.append(f"Row {row_num}: Player {player_name} already exists in {team_short}")
                            continue
                        
                        # Parse player attributes with validation
                        try:
                            batting_vs_pace = float(row.get('batting_vs_pace', 50.0))
                            batting_vs_spin = float(row.get('batting_vs_spin', 50.0))
                            batting_aggression = float(row.get('batting_aggression', 50.0))
                            bowling_skill = float(row.get('bowling_skill', 50.0))
                            fielding_skill = float(row.get('fielding_skill', 50.0))
                        except ValueError as e:
                            errors.append(f"Row {row_num}: Invalid number format - {str(e)}")
                            continue
                        
                        # Validate attribute ranges
                        attributes = {
                            'batting_vs_pace': batting_vs_pace,
                            'batting_vs_spin': batting_vs_spin,
                            'batting_aggression': batting_aggression,
                            'bowling_skill': bowling_skill,
                            'fielding_skill': fielding_skill
                        }
                        
                        valid_attributes = True
                        for attr_name, attr_value in attributes.items():
                            if not (0 <= attr_value <= 100):
                                errors.append(f"Row {row_num}: {attr_name} must be between 0 and 100 (got {attr_value})")
                                valid_attributes = False
                        
                        if not valid_attributes:
                            continue
                        
                        # Parse boolean fields
                        bowling_type = row.get('bowling_type', 'pace').lower()
                        if bowling_type not in ['pace', 'spin']:
                            bowling_type = 'pace'
                        
                        is_captain = row.get('is_captain', '').lower() in ['true', '1', 'yes', 'y']
                        is_wicketkeeper = row.get('is_wicketkeeper', '').lower() in ['true', '1', 'yes', 'y']
                        
                        # Handle captain constraint (only one per team)
                        if is_captain:
                            existing_captain = Player.query.filter_by(team_id=team.id, is_captain=True).first()
                            if existing_captain:
                                existing_captain.is_captain = False
                                print(f"  ↻ Removed captain status from {existing_captain.name}")
                        
                        # Handle wicketkeeper constraint (only one per team)
                        if is_wicketkeeper:
                            existing_wk = Player.query.filter_by(team_id=team.id, is_wicketkeeper=True).first()
                            if existing_wk:
                                existing_wk.is_wicketkeeper = False
                                print(f"  ↻ Removed wicketkeeper status from {existing_wk.name}")
                        
                        # Create player
                        player = Player(
                            name=player_name,
                            team_id=team.id,
                            batting_vs_pace=batting_vs_pace,
                            batting_vs_spin=batting_vs_spin,
                            batting_aggression=batting_aggression,
                            bowling_skill=bowling_skill,
                            fielding_skill=fielding_skill,
                            bowling_type=bowling_type,
                            is_captain=is_captain,
                            is_wicketkeeper=is_wicketkeeper
                        )
                        
                        db.session.add(player)
                        imported_count += 1
                        
                        # Show progress
                        role_indicators = []
                        if is_captain:
                            role_indicators.append("👑")
                        if is_wicketkeeper:
                            role_indicators.append("🧤")
                        if bowling_type == "spin":
                            role_indicators.append("🌀")
                        else:
                            role_indicators.append("⚡")
                        
                        roles = " ".join(role_indicators)
                        print(f"✅ Added: {player_name} to {team_short} {roles}")
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: Unexpected error - {str(e)}")
                
                # Commit all changes
                if imported_count > 0:
                    db.session.commit()
                    print(f"\n💾 Database updated successfully")
                else:
                    db.session.rollback()
                    print(f"\n❌ No players imported, rolling back")
                
                # Print summary
                print(f"\n🏏 Import Summary:")
                print(f"✅ Successfully imported: {imported_count} players")
                
                if created_teams:
                    print(f"🆕 Created teams: {', '.join(created_teams)}")
                
                if errors:
                    print(f"⚠️  Errors encountered: {len(errors)}")
                    for i, error in enumerate(errors[:10]):  # Show first 10 errors
                        print(f"   {i+1}. {error}")
                    if len(errors) > 10:
                        print(f"   ... and {len(errors) - 10} more errors")
                
                # Show team status
                print(f"\n📊 Team Summary:")
                teams = Team.query.all()
                for team in teams:
                    player_count = len(team.players)
                    status = "✅ Complete" if player_count == 11 else f"⚠️  {player_count}/11 players"
                    captain = next((p.name for p in team.players if p.is_captain), "No captain")
                    wk = next((p.name for p in team.players if p.is_wicketkeeper), "No wicketkeeper")
                    print(f"   {team.short_name}: {status} | Captain: {captain} | WK: {wk}")
                
                return imported_count > 0
                
        except FileNotFoundError:
            print(f"❌ Error: File '{csv_file_path}' not found")
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            db.session.rollback()
            return False

def create_sample_csv():
    """Create a sample CSV file with default cricket teams"""
    csv_content = """team_name,team_short,name,batting_vs_pace,batting_vs_spin,batting_aggression,bowling_skill,fielding_skill,bowling_type,is_captain,is_wicketkeeper
India,IND,Virat Kohli,85,80,75,20,85,pace,true,false
India,IND,Rohit Sharma,80,75,70,30,75,pace,false,false
India,IND,KL Rahul,75,70,65,25,80,pace,false,true
India,IND,Hardik Pandya,70,65,80,75,85,pace,false,false
India,IND,Ravindra Jadeja,65,85,70,80,95,spin,false,false
India,IND,Rishabh Pant,70,75,85,15,75,pace,false,false
India,IND,Jasprit Bumrah,25,20,40,95,70,pace,false,false
India,IND,Mohammed Shami,30,25,45,90,65,pace,false,false
India,IND,Yuzvendra Chahal,35,30,50,85,60,spin,false,false
India,IND,Bhuvneshwar Kumar,40,35,50,85,70,pace,false,false
India,IND,Shikhar Dhawan,75,70,70,20,75,pace,false,false
Australia,AUS,Steve Smith,80,85,65,30,85,pace,true,false
Australia,AUS,David Warner,85,70,80,25,80,pace,false,false
Australia,AUS,Alex Carey,65,60,70,20,85,pace,false,true
Australia,AUS,Glenn Maxwell,70,75,85,70,80,spin,false,false
Australia,AUS,Marcus Stoinis,70,65,75,70,80,pace,false,false
Australia,AUS,Pat Cummins,35,30,50,95,75,pace,false,false
Australia,AUS,Mitchell Starc,30,25,45,90,70,pace,false,false
Australia,AUS,Adam Zampa,40,35,55,85,65,spin,false,false
Australia,AUS,Josh Hazlewood,25,20,40,90,70,pace,false,false
Australia,AUS,Aaron Finch,75,70,75,25,75,pace,false,false
Australia,AUS,Marnus Labuschagne,75,80,60,35,85,pace,false,false"""
    
    with open('default_players.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    print("✅ Created default_players.csv with sample cricket teams")
    return 'default_players.csv'

def validate_csv_format(csv_file_path):
    """Validate CSV format before processing"""
    required_columns = [
        'team_name', 'team_short', 'name', 'batting_vs_pace', 'batting_vs_spin',
        'batting_aggression', 'bowling_skill', 'fielding_skill', 'bowling_type',
        'is_captain', 'is_wicketkeeper'
    ]
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Check if all required columns are present
            missing_columns = set(required_columns) - set(csv_reader.fieldnames)
            if missing_columns:
                print(f"❌ Error: Missing required columns: {', '.join(missing_columns)}")
                print(f"Required columns: {', '.join(required_columns)}")
                return False
            
            # Check if file has data
            first_row = next(csv_reader, None)
            if first_row is None:
                print("❌ Error: CSV file appears to be empty")
                return False
            
            print("✅ CSV format validation passed")
            return True
            
    except Exception as e:
        print(f"❌ Error validating CSV: {str(e)}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("🏏 Cricket Simulator - Player Import Tool")
        print("\nUsage:")
        print("  python import_players.py <csv_file_path>")
        print("  python import_players.py --create-sample")
        print("  python import_players.py --validate <csv_file_path>")
        print("\nExamples:")
        print("  python import_players.py players.csv")
        print("  python import_players.py --create-sample")
        print("  python import_players.py --validate my_players.csv")
        print("\nCSV Format Required:")
        print("  team_name,team_short,name,batting_vs_pace,batting_vs_spin,batting_aggression,bowling_skill,fielding_skill,bowling_type,is_captain,is_wicketkeeper")
        return
    
    if sys.argv[1] == '--create-sample':
        csv_file = create_sample_csv()
        print(f"\n🚀 Now run: python import_players.py {csv_file}")
        return
    
    if sys.argv[1] == '--validate':
        if len(sys.argv) < 3:
            print("❌ Error: Please specify CSV file to validate")
            return
        csv_file_path = sys.argv[2]
        if validate_csv_format(csv_file_path):
            print("🎉 Your CSV file is valid and ready for import!")
        return
    
    csv_file_path = sys.argv[1]
    
    if not os.path.exists(csv_file_path):
        print(f"❌ Error: File '{csv_file_path}' does not exist")
        print("\n💡 Tip: Run 'python import_players.py --create-sample' to create a sample CSV")
        return
    
    # Validate CSV format first
    if not validate_csv_format(csv_file_path):
        return
    
    print(f"🏏 Importing players from: {csv_file_path}")
    success = import_players_from_csv(csv_file_path)
    
    if success:
        print("\n🎉 Import completed successfully!")
        print("🚀 You can now run your Flask app: python app.py")
    else:
        print("\n❌ Import failed. Please check the errors above.")

if __name__ == '__main__':
    main()