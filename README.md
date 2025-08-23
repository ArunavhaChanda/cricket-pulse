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


print("Flask application structure created!")
print("\\nNext steps:")
print("1. Create the directory structure as shown above")
print("2. Copy the code into appropriate files")
print("3. Install dependencies: pip install -r requirements.txt")
print("4. Run the application: python app.py")
print("5. Visit http://localhost:5000 to start using the cricket simulator")
