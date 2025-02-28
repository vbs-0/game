# Arena Battle Royale

A real-time multiplayer arena battle game where players compete in fast-paced combat. This game uses Flask for the backend and Socket.IO for real-time communication.

![Arena Battle Royale Game](https://via.placeholder.com/800x400?text=Arena+Battle+Royale)

## Features

- **Real-time Multiplayer**: Battle with multiple players simultaneously
- **Smooth Animations**: Enjoy fluid gameplay with canvas-based rendering
- **Interactive UI**: Beautiful user interface with health bars, scoreboard, and kill notifications
- **Simple Controls**: Easy to learn, hard to master gameplay
- **Instant Join**: Just enter your name and jump into the action

## Requirements

- Python 3.7+
- Flask
- Flask-SocketIO
- Modern web browser with JavaScript enabled

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/arena-battle-royale.git
   cd arena-battle-royale
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the game server:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## How to Play

1. **Join**: Enter your name on the welcome screen
2. **Move**: Use WASD or arrow keys
3. **Aim**: Move your mouse to aim
4. **Shoot**: Click left mouse button to fire
5. **Respawn**: Click the respawn button after being eliminated
6. **Win**: Score the most points by eliminating other players

## Game Mechanics

- Each player starts with 100 health points
- Projectiles deal 10 damage points
- Players can shoot once every 0.5 seconds
- Eliminated players can respawn immediately
- The arena has boundaries that players and projectiles cannot cross

## Project Structure

```
arena-battle-royale/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── index.html      # Welcome screen
│   └── game.html       # Game interface
├── static/             # Static assets
│   ├── css/            # CSS stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Game images
└── requirements.txt    # Python dependencies
```

## Technical Details

- **Backend**: Flask + Socket.IO for real-time communication
- **Frontend**: HTML5 Canvas for rendering, JavaScript for game logic
- **Communication**: WebSockets for bidirectional real-time updates
- **Game Loop**: Server-side physics and collision detection
- **State Management**: Server as the source of truth for game state

## Customization

You can customize various aspects of the game by modifying the following variables in `app.py`:

- `game_state["arena_size"]`: Size of the game arena
- `game_state["start_health"]`: Initial player health
- `game_state["max_players"]`: Maximum number of players allowed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Flask and Flask-SocketIO for the backend framework
- Socket.IO for real-time communication
- HTML5 Canvas for rendering
- All the awesome contributors and players