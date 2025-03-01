from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import uuid
import math
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

# Game state
players = {}
projectiles = {}
guns = {}  # Dictionary to hold guns
game_state = {
    "arena_size": 1000,
    "start_health": 100,
    "max_players": 10,
    "gun_spawn_rate": 5  # Time in seconds for gun spawn
}

# Player class to handle player state
class Player:
    def __init__(self, id, name, x=None, y=None):
        self.id = id
        self.name = name
        self.x = x if x is not None else random.randint(50, game_state["arena_size"] - 50)
        self.y = y if y is not None else random.randint(50, game_state["arena_size"] - 50)
        self.health = game_state["start_health"]
        self.angle = 0
        self.speed = 5
        self.score = 0
        self.color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.last_shot = datetime.now()
        self.alive = True
        self.inventory = []  # Player's gun inventory

# Gun class
class Gun:
    def __init__(self, id, name, damage, x, y):
        self.id = id
        self.name = name
        self.damage = damage
        self.x = x
        self.y = y

# Projectile class
class Projectile:
    def __init__(self, id, owner_id, x, y, angle):
        self.id = id
        self.owner_id = owner_id
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.damage = 10
        self.radius = 5
        self.alive = True

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Check if out of bounds
        if (self.x < 0 or self.x > game_state["arena_size"] or
            self.y < 0 or self.y > game_state["arena_size"]):
            self.alive = False
            return False

        # Check collisions with players
        for player_id, player in players.items():
            if player_id != self.owner_id and player.alive:
                # Simple collision detection
                dx = self.x - player.x
                dy = self.y - player.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < 30:  # Player radius + projectile radius
                    player.health -= self.damage
                    if player.health <= 0:
                        player.alive = False
                        if self.owner_id in players:
                            players[self.owner_id].score += 1
                    self.alive = False
                    return False

        return True

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/join', methods=['POST'])
def join():
    data = request.json
    player_name = data.get('name', 'Unknown')
    player_id = str(uuid.uuid4())

    session['player_id'] = player_id

    if len(players) >= game_state["max_players"]:
        return jsonify({"success": False, "message": "Game is full"})

    players[player_id] = Player(player_id, player_name)

    return jsonify({
        "success": True,
        "player_id": player_id,
        "game_state": game_state
    })

# Socket events
@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    player_id = session.get('player_id')
    if player_id and player_id in players:
        del players[player_id]
        emit('player_left', {"player_id": player_id}, broadcast=True)
    print("Client disconnected")

@socketio.on('join_game')
def handle_join_game(data):
    player_id = data.get('player_id')
    if player_id in players:
        join_room('game')
        emit('game_state', {
            "players": {pid: {
                "id": p.id,
                "name": p.name,
                "x": p.x,
                "y": p.y,
                "health": p.health,
                "angle": p.angle,
                "score": p.score,
                "color": p.color,
                "alive": p.alive,
                "inventory": p.inventory
            } for pid, p in players.items()},
            "projectiles": {pid: {
                "id": p.id,
                "x": p.x,
                "y": p.y,
                "angle": p.angle
            } for pid, p in projectiles.items()},
            "guns": {gid: {
                "id": g.id,
                "name": g.name,
                "damage": g.damage,
                "x": g.x,
                "y": g.y
            } for gid, g in guns.items()},
            "arena_size": game_state["arena_size"]
        }, room='game')

        emit('new_player', {
            "id": players[player_id].id,
            "name": players[player_id].name,
            "x": players[player_id].x,
            "y": players[player_id].y,
            "health": players[player_id].health,
            "angle": players[player_id].angle,
            "score": players[player_id].score,
            "color": players[player_id].color,
            "alive": players[player_id].alive,
            "inventory": players[player_id].inventory
        }, broadcast=True, include_self=False)

@socketio.on('player_update')
def handle_player_update(data):
    player_id = data.get('player_id')
    if player_id in players:
        player = players[player_id]

        if 'x' in data and 'y' in data:
            player.x = data['x']
            player.y = data['y']

        if 'angle' in data:
            player.angle = data['angle']

        emit('player_position', {
            "id": player.id,
            "x": player.x,
            "y": player.y,
            "angle": player.angle
        }, broadcast=True, include_self=False)

@socketio.on('shoot')
def handle_shoot(data):
    player_id = data.get('player_id')
    if player_id in players and players[player_id].alive:
        player = players[player_id]
        current_time = datetime.now()
        time_diff = (current_time - player.last_shot).total_seconds()

        # Rate limit shooting
        if time_diff >= 0.1:  # Can shoot every 0.1 seconds
            player.last_shot = current_time
            projectile_id = str(uuid.uuid4())
            angle = data.get('angle', player.angle)

            projectile = Projectile(
                projectile_id,
                player_id,
                player.x + math.cos(angle) * 30,  # Offset from player center
                player.y + math.sin(angle) * 30,
                angle
            )

            projectiles[projectile_id] = projectile

            emit('new_projectile', {
                "id": projectile.id,
                "x": projectile.x,
                "y": projectile.y,
                "angle": projectile.angle,
                "owner_id": projectile.owner_id
            }, broadcast=True)

@socketio.on('respawn')
def handle_respawn(data):
    player_id = data.get('player_id')
    if player_id in players:
        player = players[player_id]
        player.health = game_state["start_health"]
        player.alive = True
        player.x = random.randint(50, game_state["arena_size"] - 50)
        player.y = random.randint(50, game_state["arena_size"] - 50)

        emit('player_respawned', {
            "id": player.id,
            "x": player.x,
            "y": player.y,
            "health": player.health
        }, broadcast=True)

@socketio.on('collect_gun')
def handle_collect_gun(data):
    player_id = data.get('player_id')
    gun_id = data.get('gun_id')

    if player_id in players and gun_id in guns:
        player = players[player_id]
        gun = guns[gun_id]

        player.inventory.append(gun)  # Add gun to player's inventory
        del guns[gun_id]  # Remove gun from the game
        emit('gun_collected', {"player_id": player_id, "gun_id": gun_id}, broadcast=True)

def spawn_guns():
    """Spawn guns at random locations"""
    while True:
        gun_id = str(uuid.uuid4())
        gun_name = f"Gun-{gun_id[:5]}"  # Example gun name
        gun_damage = random.randint(5, 20)  # Random damage value
        x = random.randint(50, game_state["arena_size"] - 50)
        y = random.randint(50, game_state["arena_size"] - 50)

        gun = Gun(gun_id, gun_name, gun_damage, x, y)
        guns[gun_id] = gun

        # Emit gun spawn event
        socketio.emit('new_gun', {
            "id": gun.id,
            "name": gun.name,
            "damage": gun.damage,
            "x": gun.x,
            "y": gun.y
        }, broadcast=True)

        socketio.sleep(game_state["gun_spawn_rate"])  # Wait before spawning the next gun

def game_loop():
    """Update game state and broadcast changes"""
    # Update projectiles
    to_remove = []
    for projectile_id, projectile in projectiles.items():
        if not projectile.update():
            to_remove.append(projectile_id)

    # Remove dead projectiles
    for projectile_id in to_remove:
        if projectile_id in projectiles:
            del projectiles[projectile_id]

    # Broadcast updates
    if to_remove:
        socketio.emit('remove_projectiles', {"projectile_ids": to_remove}, to='game')

    # Update health and status of players
    player_updates = {}
    for player_id, player in players.items():
        player_updates[player_id] = {
            "health": player.health,
            "alive": player.alive,
            "score": player.score
        }

    if player_updates:
        socketio.emit('player_status_update', {"players": player_updates}, to='game')

if __name__ == '__main__':
    # Set up a background thread for the game loop
    from threading import Thread
    import time

    def run_game_loop():
        while True:
            game_loop()
            time.sleep(1/30)  # 30 fps

    def run_gun_spawner():
        spawn_guns()

    game_thread = Thread(target=run_game_loop)
    game_thread.daemon = True
    game_thread.start()

    gun_thread = Thread(target=run_gun_spawner)
    gun_thread.daemon = True
    gun_thread.start()

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
