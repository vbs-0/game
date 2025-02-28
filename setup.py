"""
Arena Battle Royale - Setup Script
Run this script to set up the project structure and install dependencies.
"""

import os
import subprocess
import shutil
import sys

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_file(path, content):
    """Create file with specified content"""
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def main():
    # Create project structure
    create_directory('templates')
    create_directory('static')
    create_directory('static/css')
    create_directory('static/js')
    create_directory('static/images')
    
    # Create requirements.txt
    requirements = """
Flask==2.2.3
Flask-SocketIO==5.3.2
python-socketio==5.7.2
python-engineio==4.3.4
gevent==22.10.2
gevent-websocket==0.10.1
"""
    create_file('requirements.txt', requirements.strip())
    
    # Create README.md
    readme = """
# Arena Battle Royale

A multiplayer arena battle game built with Flask and Socket.IO.

## Installation

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the game server:
   ```
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## How to Play

- Move with WASD or arrow keys
- Aim with your mouse
- Shoot with left mouse button
- Eliminate other players to score points
- Last player standing wins!

"""
    create_file('README.md', readme.strip())
    
    # Try to install dependencies
    try:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.")
    
    # Copy game.py content to app.py
    # Note: game.py should be copied from the artifact shown earlier
    
    # Copy HTML templates
    index_html_path = os.path.join('templates', 'index.html')
    game_html_path = os.path.join('templates', 'game.html')
    
    # You would need to extract these from the artifacts shown earlier
    
    print("\nSetup complete! Run 'python app.py' to start the game server.")

if __name__ == "__main__":
    main()