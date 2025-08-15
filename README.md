# 🏏 Cricket Simulator

A comprehensive cricket match simulation application with realistic gameplay, team management, and live match tracking.

## Features

- 👥 **Team Management**: Create and customize cricket teams with detailed player attributes
- ⚡ **Realistic Simulation**: Advanced probability-based cricket simulation engine
- 📊 **Live Statistics**: Real-time match statistics and player performance tracking
- 🎯 **Multiple Formats**: Support for T20 and ODI matches
- 🌍 **Location Effects**: Different grounds affect player performance
- 📱 **Live Updates**: Real-time match updates with beautiful UI

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd cricsim2
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python run.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:5000`

## Usage

1. **Create Teams**: Go to "Teams" and create your cricket teams (11 players each)
2. **Start Match**: Create a new match by selecting two teams and match format
3. **Play**: Conduct toss, make decisions, and simulate the match ball by ball
4. **Enjoy**: Watch realistic cricket unfold with live statistics and commentary

## File Structure

```
cricsim2/
├── run.py              # Main application runner
├── app.py              # Flask application factory
├── models.py           # Database models
├── routes.py           # API routes
├── cricket_engine.py   # Cricket simulation engine
├── config.py           # Configuration settings
├── templates/          # HTML templates
├── static/             # CSS and JavaScript files
└── instance/           # Database and instance files
```

## Integration with Your Cricket Logic

The application is designed to integrate with your existing Python cricket simulation logic. 

**Key Integration Points**:

1. **`cricket_engine.py`** - Replace the `simulate_delivery()` method with your actual cricket simulation logic
2. **Probability Matrices** - Import and use your existing probability matrices for realistic outcomes
3. **Player Attributes** - Your 5 numerical attributes are already integrated into the database models
4. **Location Effects** - Your location-based multipliers are implemented and ready to use

**To Integrate Your Logic**:

```python
# In cricket_engine.py, replace the simulate_delivery method:
def simulate_delivery(self, bowler_id, striker_id, non_striker_id, current_over, ball_in_over):
    # Import your existing cricket simulation classes
    from your_cricket_logic import YourCricketSimulator
    
    # Get player attributes from database
    bowler = Player.query.get(bowler_id)
    striker = Player.query.get(striker_id)
    
    # Apply location adjustments
    adjusted_bowler_attrs = self.apply_location_adjustments({
        'bowling_skill': bowler.bowling_skill,
        'bowling_type': bowler.bowling_type
    })
    
    # Use your existing simulation logic
    simulator = YourCricketSimulator()
    outcome = simulator.simulate_ball(adjusted_bowler_attrs, striker_attrs, your_probability_matrices)
    
    # Return result in our format
    return DeliveryResult(
        delivery_type=outcome.delivery_type,
        stroke_type=outcome.stroke_type,
        runs_scored=outcome.runs,
        extras=outcome.extras,
        is_wicket=outcome.is_wicket,
        dismissal_type=outcome.dismissal_type
    )
```

## Development

- **Database**: SQLite (automatically created)
- **Frontend**: HTML5, CSS3, JavaScript with WebSocket support
- **Backend**: Flask with SQLAlchemy ORM
- **Real-time**: WebSocket connections for live match updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
EOF

echo "✅ Project structure created successfully!"
echo ""
echo "🏏 Next Steps:"
echo "1. cd cricsim2"
echo "2. pip install -r requirements.txt"
echo "3. Copy the provided Python code into the respective files:"
echo "   - app.py (Flask application)"
echo "   - models.py (Database models)"
echo "   - routes.py (API routes)"
echo "   - cricket_engine.py (Game engine)"
echo "   - templates/ (HTML templates)"
echo "4. python run.py"
echo "5. Open http://localhost:5000 in your browser"
echo ""
echo "🎯 IMPORTANT: Replace the mock simulation logic in cricket_engine.py"
echo "   with your actual Python cricket game logic for realistic gameplay!"
echo ""
echo "📁 Files to create manually:"
echo "cricsim2/"
echo "├── app.py"
echo "├── models.py" 
echo "├── routes.py"
echo "├── cricket_engine.py"
echo "├── templates/"
echo "│   ├── base.html"
echo "│   ├── index.html"
echo "│   ├── teams.html"
echo "│   └── match.html"
echo "└── static/ (optional additional CSS/JS)"




# Your existing Python cricket logic integration points:
'''
INTEGRATION CHECKLIST:

1. Replace the simulate_delivery method in CricketGameEngine with calls to your existing:
   - Delivery type probability matrix
   - Stroke type determination
   - Miss/Hit/Slog result calculation
   - Caught/Dropped/Dot logic
   - All your probability matrices and random number generation

2. Import your existing classes/functions and use them in:
   - CricketGameEngine.simulate_delivery()
   - Location-based attribute adjustments
   - Player skill calculations

3. Map your existing data structures to the database models:
   - Team lineups -> Team and Player models
   - Match state -> Match, Innings, Delivery models
   - Player stats -> BattingStats, BowlingStats models

4. Add API endpoints for:
   - Player selection (bowler change, new batsman)
   - Match state queries
   - Statistics retrieval

Example integration:
```python
# In your simulate_delivery method:
from your_cricket_logic import CricketSimulator, DeliveryOutcome

def simulate_delivery(self, bowler_id, striker_id, non_striker_id, current_over, ball_in_over):
    # Get your existing player objects/attributes
    bowler_attrs = self.get_adjusted_player_attributes(bowler_id)
    striker_attrs = self.get_adjusted_player_attributes(striker_id)
    
    # Use your existing simulation logic
    your_simulator = CricketSimulator()
    outcome = your_simulator.simulate_single_delivery(
        bowler_attrs, striker_attrs, your_probability_matrices
    )
    
    # Convert to our DeliveryResult format
    return DeliveryResult(
        delivery_type=outcome.delivery_type,
        stroke_type=outcome.stroke_type,
        runs_scored=outcome.runs,
        extras=outcome.extras,
        is_wicket=outcome.is_wicket,
        dismissal_type=outcome.dismissal_type
    )
```
'''

print("Flask application structure created!")
print("\\nNext steps:")
print("1. Create the directory structure as shown above")
print("2. Copy the code into appropriate files")
print("3. Install dependencies: pip install -r requirements.txt")
print("4. Run the application: python app.py")
print("5. Visit http://localhost:5000 to start using the cricket simulator")
print("\\nIMPORTANT: Replace the mock simulation logic in cricket_engine.py with your actual Python cricket game logic!")# cricket-pulse
