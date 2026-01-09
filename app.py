import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="🧟 Zombie Escape Game - BFS & DFS",
    page_icon="🧟",
    layout="wide"
)

# Hide Streamlit default menu and footer for cleaner game view
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        }
    </style>
""", unsafe_allow_html=True)

# Game HTML, CSS, and JavaScript combined
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            margin-bottom: 20px;
        }

        header h1 {
            font-size: 2.2rem;
            text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            margin-bottom: 10px;
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
            to { text-shadow: 0 0 30px rgba(255, 0, 0, 0.8), 0 0 40px rgba(255, 0, 0, 0.5); }
        }

        .subtitle {
            color: #a0a0a0;
            font-size: 1rem;
        }

        .game-info {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .legend {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
        }

        .cell-demo {
            width: 22px;
            height: 22px;
            border-radius: 5px;
            display: inline-block;
        }

        .cell-demo.player { background: linear-gradient(135deg, #4CAF50, #45a049); box-shadow: 0 0 10px rgba(76, 175, 80, 0.7); }
        .cell-demo.zombie { background: linear-gradient(135deg, #f44336, #d32f2f); box-shadow: 0 0 10px rgba(244, 67, 54, 0.7); }
        .cell-demo.exit { background: linear-gradient(135deg, #FFD700, #FFA500); box-shadow: 0 0 10px rgba(255, 215, 0, 0.7); }
        .cell-demo.wall { background: linear-gradient(135deg, #333, #555); }
        .cell-demo.path { background: linear-gradient(135deg, #2196F3, #1976D2); box-shadow: 0 0 10px rgba(33, 150, 243, 0.7); }
        .cell-demo.infected { background: linear-gradient(135deg, #9C27B0, #7B1FA2); box-shadow: 0 0 10px rgba(156, 39, 176, 0.7); }

        .controls {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin-bottom: 15px;
        }

        .btn {
            padding: 12px 24px;
            font-size: 0.95rem;
            font-weight: bold;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn:hover { transform: translateY(-3px); box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3); }
        .btn:active { transform: translateY(0); }
        .btn-danger { background: linear-gradient(135deg, #f44336, #d32f2f); color: white; }
        .btn-danger:hover { background: linear-gradient(135deg, #ff5252, #f44336); box-shadow: 0 5px 20px rgba(244, 67, 54, 0.5); }
        .btn-success { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; }
        .btn-success:hover { background: linear-gradient(135deg, #66BB6A, #4CAF50); box-shadow: 0 5px 20px rgba(76, 175, 80, 0.5); }
        .btn-primary { background: linear-gradient(135deg, #2196F3, #1976D2); color: white; }
        .btn-primary:hover { background: linear-gradient(135deg, #42A5F5, #2196F3); box-shadow: 0 5px 20px rgba(33, 150, 243, 0.5); }
        .btn-secondary { background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white; }
        .btn-secondary:hover { background: linear-gradient(135deg, #AB47BC, #9C27B0); box-shadow: 0 5px 20px rgba(156, 39, 176, 0.5); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

        .speed-control {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            color: #a0a0a0;
        }

        .speed-control input[type="range"] { width: 150px; cursor: pointer; }

        .game-grid {
            display: grid;
            gap: 3px;
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 15px;
            margin: 0 auto 20px;
            width: fit-content;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        }

        .cell {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            font-weight: bold;
            transition: all 0.3s ease;
            cursor: pointer;
            background: linear-gradient(135deg, #2a2a4a, #1a1a3a);
            border: 2px solid rgba(255, 255, 255, 0.1);
        }

        .cell:hover { transform: scale(1.05); border-color: rgba(255, 255, 255, 0.3); }
        .cell.player { background: linear-gradient(135deg, #4CAF50, #45a049); box-shadow: 0 0 15px rgba(76, 175, 80, 0.8); animation: pulse 1s ease-in-out infinite; }
        
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 15px rgba(76, 175, 80, 0.8); }
            50% { box-shadow: 0 0 25px rgba(76, 175, 80, 1); }
        }

        .cell.zombie { background: linear-gradient(135deg, #f44336, #d32f2f); box-shadow: 0 0 15px rgba(244, 67, 54, 0.8); animation: zombiePulse 0.5s ease-in-out infinite; }
        
        @keyframes zombiePulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .cell.exit { background: linear-gradient(135deg, #FFD700, #FFA500); box-shadow: 0 0 20px rgba(255, 215, 0, 0.8); animation: exitGlow 1.5s ease-in-out infinite; }
        
        @keyframes exitGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.8); }
            50% { box-shadow: 0 0 35px rgba(255, 215, 0, 1); }
        }

        .cell.wall { background: linear-gradient(135deg, #333, #555); border-color: #666; }
        .cell.path { background: linear-gradient(135deg, #2196F3, #1976D2); box-shadow: 0 0 15px rgba(33, 150, 243, 0.8); }
        .cell.infected { background: linear-gradient(135deg, #9C27B0, #7B1FA2); box-shadow: 0 0 15px rgba(156, 39, 176, 0.8); animation: infect 0.3s ease-out; }
        
        @keyframes infect {
            0% { transform: scale(0.5); opacity: 0; }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); opacity: 1; }
        }

        .cell.visited { background: linear-gradient(135deg, #607D8B, #455A64); }
        .cell.current { background: linear-gradient(135deg, #FF9800, #F57C00); box-shadow: 0 0 20px rgba(255, 152, 0, 0.8); }

        .status {
            text-align: center;
            padding: 15px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 10px;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.1);
        }

        .status.win { background: linear-gradient(135deg, rgba(76, 175, 80, 0.3), rgba(69, 160, 73, 0.3)); color: #4CAF50; }
        .status.lose { background: linear-gradient(135deg, rgba(244, 67, 54, 0.3), rgba(211, 47, 47, 0.3)); color: #f44336; }

        .algorithm-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .algo-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            transition: transform 0.3s ease;
        }

        .algo-card:hover { transform: translateY(-5px); }
        .algo-card h3 { margin-bottom: 10px; font-size: 1.1rem; }
        .algo-card p { color: #a0a0a0; margin-bottom: 10px; line-height: 1.5; font-size: 0.9rem; }
        .algo-card code { display: block; background: rgba(0, 0, 0, 0.3); padding: 8px 12px; border-radius: 5px; font-size: 0.8rem; color: #4CAF50; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧟‍♂️ Zombie Escape Game</h1>
            <p class="subtitle">BFS = Zombie Spread | DFS = Player Escape Path</p>
        </header>

        <div class="game-info">
            <div class="legend">
                <div class="legend-item"><span class="cell-demo player"></span> Player (P)</div>
                <div class="legend-item"><span class="cell-demo zombie"></span> Zombie (Z)</div>
                <div class="legend-item"><span class="cell-demo exit"></span> Exit (E)</div>
                <div class="legend-item"><span class="cell-demo wall"></span> Wall</div>
                <div class="legend-item"><span class="cell-demo path"></span> Escape Path</div>
                <div class="legend-item"><span class="cell-demo infected"></span> Infected</div>
            </div>
        </div>

        <div class="controls">
            <button id="startZombies" class="btn btn-danger">🧟 Start Zombie Spread (BFS)</button>
            <button id="findEscape" class="btn btn-success">🏃 Find Escape Path (DFS)</button>
            <button id="resetGame" class="btn btn-primary">🔄 Reset Game</button>
            <button id="randomMap" class="btn btn-secondary">🎲 Random Map</button>
        </div>

        <div class="speed-control">
            <label for="speed">Animation Speed:</label>
            <input type="range" id="speed" min="50" max="500" value="200">
            <span id="speedValue">200ms</span>
        </div>

        <div id="gameGrid" class="game-grid"></div>

        <div id="status" class="status">
            Click "Start Zombie Spread" to see BFS in action, or "Find Escape Path" for DFS!
        </div>

        <div class="algorithm-info">
            <div class="algo-card">
                <h3>🔴 BFS - Breadth First Search</h3>
                <p>Zombies spread level by level, infecting all adjacent cells before moving further. This simulates realistic zombie spread!</p>
                <code>Queue-based | O(V + E) | Shortest path</code>
            </div>
            <div class="algo-card">
                <h3>🟢 DFS - Depth First Search</h3>
                <p>Player explores one path completely before backtracking. Goes deep in one direction before trying alternatives.</p>
                <code>Stack/Recursion | O(V + E) | Memory efficient</code>
            </div>
        </div>
    </div>

    <script>
        class ZombieEscapeGame {
            constructor() {
                this.rows = 10;
                this.cols = 12;
                this.EMPTY = 0;
                this.WALL = 1;
                this.PLAYER = 2;
                this.ZOMBIE = 3;
                this.EXIT = 4;
                this.PATH = 5;
                this.INFECTED = 6;
                this.VISITED = 7;
                this.grid = [];
                this.playerPos = null;
                this.zombiePositions = [];
                this.exitPos = null;
                this.isRunning = false;
                this.animationSpeed = 200;
                this.directions = [[-1, 0], [0, 1], [1, 0], [0, -1]];
                this.init();
            }

            init() {
                this.setupEventListeners();
                this.createDefaultMap();
                this.renderGrid();
            }

            setupEventListeners() {
                document.getElementById('startZombies').addEventListener('click', () => this.startZombieBFS());
                document.getElementById('findEscape').addEventListener('click', () => this.findEscapeDFS());
                document.getElementById('resetGame').addEventListener('click', () => this.resetGame());
                document.getElementById('randomMap').addEventListener('click', () => this.generateRandomMap());
                
                const speedSlider = document.getElementById('speed');
                speedSlider.addEventListener('input', (e) => {
                    this.animationSpeed = parseInt(e.target.value);
                    document.getElementById('speedValue').textContent = `${this.animationSpeed}ms`;
                });
            }

            createDefaultMap() {
                this.grid = Array(this.rows).fill(null).map(() => Array(this.cols).fill(this.EMPTY));
                this.playerPos = { row: 8, col: 1 };
                this.grid[8][1] = this.PLAYER;
                this.zombiePositions = [{ row: 1, col: 10 }, { row: 3, col: 8 }, { row: 5, col: 11 }];
                this.zombiePositions.forEach(pos => { this.grid[pos.row][pos.col] = this.ZOMBIE; });
                this.exitPos = { row: 0, col: 11 };
                this.grid[0][11] = this.EXIT;
                const walls = [[0, 3], [1, 3], [2, 3], [3, 3], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [2, 5], [3, 5], [4, 5], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7], [2, 7], [2, 8], [2, 9], [4, 9], [5, 9], [6, 9], [9, 5], [9, 6], [9, 7], [9, 8], [3, 1], [4, 1], [8, 9], [8, 10]];
                walls.forEach(([row, col]) => { if (this.grid[row][col] === this.EMPTY) this.grid[row][col] = this.WALL; });
            }

            generateRandomMap() {
                if (this.isRunning) return;
                this.grid = Array(this.rows).fill(null).map(() => Array(this.cols).fill(this.EMPTY));
                this.playerPos = { row: Math.floor(Math.random() * (this.rows - 2)) + 1, col: Math.floor(Math.random() * 3) };
                this.grid[this.playerPos.row][this.playerPos.col] = this.PLAYER;
                this.exitPos = { row: Math.floor(Math.random() * (this.rows - 2)) + 1, col: this.cols - 1 - Math.floor(Math.random() * 2) };
                this.grid[this.exitPos.row][this.exitPos.col] = this.EXIT;
                const numZombies = Math.floor(Math.random() * 3) + 2;
                this.zombiePositions = [];
                for (let i = 0; i < numZombies; i++) {
                    let pos;
                    do { pos = { row: Math.floor(Math.random() * this.rows), col: Math.floor(Math.random() * (this.cols - 4)) + 4 }; } while (this.grid[pos.row][pos.col] !== this.EMPTY);
                    this.zombiePositions.push(pos);
                    this.grid[pos.row][pos.col] = this.ZOMBIE;
                }
                const wallPercentage = 0.2 + Math.random() * 0.15;
                const numWalls = Math.floor(this.rows * this.cols * wallPercentage);
                for (let i = 0; i < numWalls; i++) {
                    const row = Math.floor(Math.random() * this.rows);
                    const col = Math.floor(Math.random() * this.cols);
                    if (this.grid[row][col] === this.EMPTY) this.grid[row][col] = this.WALL;
                }
                this.clearPathAround(this.playerPos);
                this.clearPathAround(this.exitPos);
                this.renderGrid();
                this.updateStatus("🎲 New random map generated! Try to escape!");
            }

            clearPathAround(pos) {
                for (const [dr, dc] of this.directions) {
                    const newRow = pos.row + dr;
                    const newCol = pos.col + dc;
                    if (this.isValid(newRow, newCol) && this.grid[newRow][newCol] === this.WALL) this.grid[newRow][newCol] = this.EMPTY;
                }
            }

            renderGrid() {
                const gameGrid = document.getElementById('gameGrid');
                gameGrid.innerHTML = '';
                gameGrid.style.gridTemplateColumns = `repeat(${this.cols}, 40px)`;
                for (let row = 0; row < this.rows; row++) {
                    for (let col = 0; col < this.cols; col++) {
                        const cell = document.createElement('div');
                        cell.className = 'cell';
                        cell.dataset.row = row;
                        cell.dataset.col = col;
                        this.updateCellAppearance(cell, this.grid[row][col]);
                        cell.addEventListener('click', () => this.toggleCell(row, col));
                        gameGrid.appendChild(cell);
                    }
                }
            }

            updateCellAppearance(cell, type) {
                cell.classList.remove('player', 'zombie', 'exit', 'wall', 'path', 'infected', 'visited', 'current');
                cell.textContent = '';
                switch (type) {
                    case this.PLAYER: cell.classList.add('player'); cell.textContent = '🧍'; break;
                    case this.ZOMBIE: cell.classList.add('zombie'); cell.textContent = '🧟'; break;
                    case this.EXIT: cell.classList.add('exit'); cell.textContent = '🏁'; break;
                    case this.WALL: cell.classList.add('wall'); cell.textContent = '⬛'; break;
                    case this.PATH: cell.classList.add('path'); cell.textContent = '👣'; break;
                    case this.INFECTED: cell.classList.add('infected'); cell.textContent = '☠️'; break;
                    case this.VISITED: cell.classList.add('visited'); break;
                }
            }

            toggleCell(row, col) {
                if (this.isRunning) return;
                const currentType = this.grid[row][col];
                if (currentType === this.PLAYER || currentType === this.ZOMBIE || currentType === this.EXIT) return;
                this.grid[row][col] = currentType === this.WALL ? this.EMPTY : this.WALL;
                const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
                this.updateCellAppearance(cell, this.grid[row][col]);
            }

            getCell(row, col) { return document.querySelector(`[data-row="${row}"][data-col="${col}"]`); }
            isValid(row, col) { return row >= 0 && row < this.rows && col >= 0 && col < this.cols; }
            isWalkable(row, col) { return this.isValid(row, col) && this.grid[row][col] !== this.WALL; }
            updateStatus(message, type = '') { const status = document.getElementById('status'); status.textContent = message; status.className = 'status ' + type; }
            setButtonsEnabled(enabled) { document.getElementById('startZombies').disabled = !enabled; document.getElementById('findEscape').disabled = !enabled; document.getElementById('randomMap').disabled = !enabled; }
            sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

            async startZombieBFS() {
                if (this.isRunning) return;
                this.isRunning = true;
                this.setButtonsEnabled(false);
                this.updateStatus("🧟 Zombies spreading using BFS... Watch out!");
                const queue = [...this.zombiePositions.map(pos => ({ ...pos, distance: 0 }))];
                const visited = new Set();
                this.zombiePositions.forEach(pos => { visited.add(`${pos.row},${pos.col}`); });
                let playerCaught = false;

                while (queue.length > 0 && !playerCaught) {
                    const current = queue.shift();
                    if (current.row === this.playerPos.row && current.col === this.playerPos.col) {
                        playerCaught = true;
                        this.grid[current.row][current.col] = this.INFECTED;
                        const cell = this.getCell(current.row, current.col);
                        this.updateCellAppearance(cell, this.INFECTED);
                        break;
                    }
                    for (const [dr, dc] of this.directions) {
                        const newRow = current.row + dr;
                        const newCol = current.col + dc;
                        const key = `${newRow},${newCol}`;
                        if (this.isWalkable(newRow, newCol) && !visited.has(key)) {
                            visited.add(key);
                            if (newRow === this.exitPos.row && newCol === this.exitPos.col) continue;
                            if (newRow === this.playerPos.row && newCol === this.playerPos.col) {
                                playerCaught = true;
                                this.grid[newRow][newCol] = this.INFECTED;
                                const cell = this.getCell(newRow, newCol);
                                this.updateCellAppearance(cell, this.INFECTED);
                                cell.textContent = '💀';
                                break;
                            }
                            if (this.grid[newRow][newCol] === this.EMPTY || this.grid[newRow][newCol] === this.PATH || this.grid[newRow][newCol] === this.VISITED) {
                                this.grid[newRow][newCol] = this.INFECTED;
                                const cell = this.getCell(newRow, newCol);
                                this.updateCellAppearance(cell, this.INFECTED);
                                queue.push({ row: newRow, col: newCol, distance: current.distance + 1 });
                                await this.sleep(this.animationSpeed);
                            }
                        }
                    }
                    if (playerCaught) break;
                }
                if (playerCaught) this.updateStatus("💀 GAME OVER! The zombies caught you!", "lose");
                else this.updateStatus("🧟 Zombie spread complete! Some areas are still safe.", "");
                this.isRunning = false;
                this.setButtonsEnabled(true);
            }

            async findEscapeDFS() {
                if (this.isRunning) return;
                this.isRunning = true;
                this.setButtonsEnabled(false);
                this.updateStatus("🏃 Searching for escape route using DFS...");
                this.clearPathVisualization();
                const visited = new Set();
                const path = [];
                const found = await this.dfsSearch(this.playerPos.row, this.playerPos.col, visited, path);
                if (found) {
                    this.updateStatus("✅ ESCAPE ROUTE FOUND! Follow the blue path to safety!", "win");
                    await this.highlightEscapePath(path);
                } else {
                    this.updateStatus("❌ NO ESCAPE! All paths are blocked!", "lose");
                }
                this.isRunning = false;
                this.setButtonsEnabled(true);
            }

            async dfsSearch(row, col, visited, path) {
                if (row === this.exitPos.row && col === this.exitPos.col) { path.push({ row, col }); return true; }
                const key = `${row},${col}`;
                if (visited.has(key)) return false;
                visited.add(key);
                if (this.grid[row][col] === this.WALL || this.grid[row][col] === this.INFECTED) return false;
                if (this.grid[row][col] !== this.PLAYER && this.grid[row][col] !== this.EXIT) {
                    const cell = this.getCell(row, col);
                    cell.classList.add('current');
                    await this.sleep(this.animationSpeed / 2);
                    cell.classList.remove('current');
                    cell.classList.add('visited');
                }
                path.push({ row, col });
                const prioritizedDirections = [[0, 1], [1, 0], [0, -1], [-1, 0]];
                for (const [dr, dc] of prioritizedDirections) {
                    const newRow = row + dr;
                    const newCol = col + dc;
                    if (this.isValid(newRow, newCol)) {
                        const newKey = `${newRow},${newCol}`;
                        if (!visited.has(newKey) && this.grid[newRow][newCol] !== this.WALL && this.grid[newRow][newCol] !== this.INFECTED && this.grid[newRow][newCol] !== this.ZOMBIE) {
                            if (await this.dfsSearch(newRow, newCol, visited, path)) return true;
                        }
                    }
                }
                path.pop();
                return false;
            }

            async highlightEscapePath(path) {
                for (const pos of path) {
                    if (this.grid[pos.row][pos.col] !== this.PLAYER && this.grid[pos.row][pos.col] !== this.EXIT) {
                        this.grid[pos.row][pos.col] = this.PATH;
                        const cell = this.getCell(pos.row, pos.col);
                        this.updateCellAppearance(cell, this.PATH);
                        await this.sleep(this.animationSpeed / 3);
                    }
                }
            }

            clearPathVisualization() {
                for (let row = 0; row < this.rows; row++) {
                    for (let col = 0; col < this.cols; col++) {
                        if (this.grid[row][col] === this.PATH || this.grid[row][col] === this.VISITED) {
                            this.grid[row][col] = this.EMPTY;
                            const cell = this.getCell(row, col);
                            cell.classList.remove('path', 'visited', 'current');
                            this.updateCellAppearance(cell, this.EMPTY);
                        }
                    }
                }
            }

            resetGame() {
                if (this.isRunning) return;
                this.createDefaultMap();
                this.renderGrid();
                this.updateStatus("🔄 Game reset! Click buttons to start algorithms.");
            }
        }

        document.addEventListener('DOMContentLoaded', () => { window.game = new ZombieEscapeGame(); });
    </script>
</body>
</html>
"""

# Render the game
st.title("🧟‍♂️ Zombie Escape Game")
st.caption("Demonstrating BFS (Zombie Spread) & DFS (Player Escape) Algorithms")

# Embed the HTML game
components.html(game_html, height=950, scrolling=True)
