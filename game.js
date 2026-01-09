// ==========================================
// 🧟 ZOMBIE ESCAPE GAME - BFS & DFS Demo
// ==========================================

class ZombieEscapeGame {
    constructor() {
        // Grid configuration
        this.rows = 10;
        this.cols = 12;
        
        // Cell types
        this.EMPTY = 0;
        this.WALL = 1;
        this.PLAYER = 2;
        this.ZOMBIE = 3;
        this.EXIT = 4;
        this.PATH = 5;
        this.INFECTED = 6;
        this.VISITED = 7;

        // Game state
        this.grid = [];
        this.playerPos = null;
        this.zombiePositions = [];
        this.exitPos = null;
        this.isRunning = false;
        this.animationSpeed = 200;

        // Direction vectors (up, right, down, left)
        this.directions = [
            [-1, 0], [0, 1], [1, 0], [0, -1]
        ];

        // Initialize game
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
        // Initialize empty grid
        this.grid = Array(this.rows).fill(null).map(() => Array(this.cols).fill(this.EMPTY));
        
        // Set player position (bottom-left area)
        this.playerPos = { row: 8, col: 1 };
        this.grid[8][1] = this.PLAYER;

        // Set zombie positions
        this.zombiePositions = [
            { row: 1, col: 10 },
            { row: 3, col: 8 },
            { row: 5, col: 11 }
        ];
        this.zombiePositions.forEach(pos => {
            this.grid[pos.row][pos.col] = this.ZOMBIE;
        });

        // Set exit position (top-right area)
        this.exitPos = { row: 0, col: 11 };
        this.grid[0][11] = this.EXIT;

        // Add walls to create maze-like structure
        const walls = [
            [0, 3], [1, 3], [2, 3], [3, 3],
            [5, 0], [5, 1], [5, 2], [5, 3], [5, 4],
            [2, 5], [3, 5], [4, 5],
            [7, 3], [7, 4], [7, 5], [7, 6], [7, 7],
            [2, 7], [2, 8], [2, 9],
            [4, 9], [5, 9], [6, 9],
            [9, 5], [9, 6], [9, 7], [9, 8],
            [3, 1], [4, 1],
            [8, 9], [8, 10]
        ];

        walls.forEach(([row, col]) => {
            if (this.grid[row][col] === this.EMPTY) {
                this.grid[row][col] = this.WALL;
            }
        });
    }

    generateRandomMap() {
        if (this.isRunning) return;

        // Initialize empty grid
        this.grid = Array(this.rows).fill(null).map(() => Array(this.cols).fill(this.EMPTY));
        
        // Random player position (left side)
        this.playerPos = {
            row: Math.floor(Math.random() * (this.rows - 2)) + 1,
            col: Math.floor(Math.random() * 3)
        };
        this.grid[this.playerPos.row][this.playerPos.col] = this.PLAYER;

        // Random exit position (right side)
        this.exitPos = {
            row: Math.floor(Math.random() * (this.rows - 2)) + 1,
            col: this.cols - 1 - Math.floor(Math.random() * 2)
        };
        this.grid[this.exitPos.row][this.exitPos.col] = this.EXIT;

        // Random zombie positions (2-4 zombies)
        const numZombies = Math.floor(Math.random() * 3) + 2;
        this.zombiePositions = [];
        
        for (let i = 0; i < numZombies; i++) {
            let pos;
            do {
                pos = {
                    row: Math.floor(Math.random() * this.rows),
                    col: Math.floor(Math.random() * (this.cols - 4)) + 4
                };
            } while (this.grid[pos.row][pos.col] !== this.EMPTY);
            
            this.zombiePositions.push(pos);
            this.grid[pos.row][pos.col] = this.ZOMBIE;
        }

        // Add random walls (20-35% of empty cells)
        const wallPercentage = 0.2 + Math.random() * 0.15;
        const totalCells = this.rows * this.cols;
        const numWalls = Math.floor(totalCells * wallPercentage);

        for (let i = 0; i < numWalls; i++) {
            const row = Math.floor(Math.random() * this.rows);
            const col = Math.floor(Math.random() * this.cols);
            
            if (this.grid[row][col] === this.EMPTY) {
                this.grid[row][col] = this.WALL;
            }
        }

        // Ensure path exists (basic check - remove some walls near player and exit)
        this.clearPathAround(this.playerPos);
        this.clearPathAround(this.exitPos);

        this.renderGrid();
        this.updateStatus("🎲 New random map generated! Try to escape!");
    }

    clearPathAround(pos) {
        for (const [dr, dc] of this.directions) {
            const newRow = pos.row + dr;
            const newCol = pos.col + dc;
            if (this.isValid(newRow, newCol) && this.grid[newRow][newCol] === this.WALL) {
                this.grid[newRow][newCol] = this.EMPTY;
            }
        }
    }

    renderGrid() {
        const gameGrid = document.getElementById('gameGrid');
        gameGrid.innerHTML = '';
        gameGrid.style.gridTemplateColumns = `repeat(${this.cols}, 45px)`;

        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = row;
                cell.dataset.col = col;
                
                this.updateCellAppearance(cell, this.grid[row][col]);
                
                // Add click listener for wall toggling
                cell.addEventListener('click', () => this.toggleCell(row, col));
                
                gameGrid.appendChild(cell);
            }
        }
    }

    updateCellAppearance(cell, type) {
        // Remove all type classes
        cell.classList.remove('player', 'zombie', 'exit', 'wall', 'path', 'infected', 'visited', 'current');
        cell.textContent = '';

        switch (type) {
            case this.PLAYER:
                cell.classList.add('player');
                cell.textContent = '🧍';
                break;
            case this.ZOMBIE:
                cell.classList.add('zombie');
                cell.textContent = '🧟';
                break;
            case this.EXIT:
                cell.classList.add('exit');
                cell.textContent = '🏁';
                break;
            case this.WALL:
                cell.classList.add('wall');
                cell.textContent = '⬛';
                break;
            case this.PATH:
                cell.classList.add('path');
                cell.textContent = '👣';
                break;
            case this.INFECTED:
                cell.classList.add('infected');
                cell.textContent = '☠️';
                break;
            case this.VISITED:
                cell.classList.add('visited');
                break;
        }
    }

    toggleCell(row, col) {
        if (this.isRunning) return;
        
        const currentType = this.grid[row][col];
        
        // Don't allow modifying player, zombies, or exit
        if (currentType === this.PLAYER || currentType === this.ZOMBIE || currentType === this.EXIT) {
            return;
        }

        // Toggle between empty and wall
        this.grid[row][col] = currentType === this.WALL ? this.EMPTY : this.WALL;
        
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        this.updateCellAppearance(cell, this.grid[row][col]);
    }

    getCell(row, col) {
        return document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    }

    isValid(row, col) {
        return row >= 0 && row < this.rows && col >= 0 && col < this.cols;
    }

    isWalkable(row, col, grid = this.grid) {
        return this.isValid(row, col) && grid[row][col] !== this.WALL;
    }

    updateStatus(message, type = '') {
        const status = document.getElementById('status');
        status.textContent = message;
        status.className = 'status ' + type;
    }

    setButtonsEnabled(enabled) {
        document.getElementById('startZombies').disabled = !enabled;
        document.getElementById('findEscape').disabled = !enabled;
        document.getElementById('randomMap').disabled = !enabled;
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // ==========================================
    // 🔴 BFS - ZOMBIE SPREAD ALGORITHM
    // ==========================================
    async startZombieBFS() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.setButtonsEnabled(false);
        
        this.updateStatus("🧟 Zombies spreading using BFS... Watch out!");

        // Create a copy of zombie positions for BFS
        const queue = [...this.zombiePositions.map(pos => ({ ...pos, distance: 0 }))];
        const visited = new Set();
        
        // Mark initial zombie positions as visited
        this.zombiePositions.forEach(pos => {
            visited.add(`${pos.row},${pos.col}`);
        });

        let playerCaught = false;
        let step = 0;

        while (queue.length > 0 && !playerCaught) {
            const current = queue.shift();
            step++;

            // Check if zombie reached player
            if (current.row === this.playerPos.row && current.col === this.playerPos.col) {
                playerCaught = true;
                this.grid[current.row][current.col] = this.INFECTED;
                const cell = this.getCell(current.row, current.col);
                this.updateCellAppearance(cell, this.INFECTED);
                break;
            }

            // Spread to adjacent cells
            for (const [dr, dc] of this.directions) {
                const newRow = current.row + dr;
                const newCol = current.col + dc;
                const key = `${newRow},${newCol}`;

                if (this.isWalkable(newRow, newCol) && !visited.has(key)) {
                    visited.add(key);

                    // Check if this cell is the exit - zombies can't enter exit
                    if (newRow === this.exitPos.row && newCol === this.exitPos.col) {
                        continue;
                    }

                    // Check if caught player
                    if (newRow === this.playerPos.row && newCol === this.playerPos.col) {
                        playerCaught = true;
                        this.grid[newRow][newCol] = this.INFECTED;
                        const cell = this.getCell(newRow, newCol);
                        this.updateCellAppearance(cell, this.INFECTED);
                        cell.textContent = '💀';
                        break;
                    }

                    // Infect the cell
                    if (this.grid[newRow][newCol] === this.EMPTY || 
                        this.grid[newRow][newCol] === this.PATH ||
                        this.grid[newRow][newCol] === this.VISITED) {
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

        if (playerCaught) {
            this.updateStatus("💀 GAME OVER! The zombies caught you!", "lose");
        } else {
            this.updateStatus("🧟 Zombie spread complete! Some areas are still safe.", "");
        }

        this.isRunning = false;
        this.setButtonsEnabled(true);
    }

    // ==========================================
    // 🟢 DFS - PLAYER ESCAPE ALGORITHM
    // ==========================================
    async findEscapeDFS() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.setButtonsEnabled(false);

        this.updateStatus("🏃 Searching for escape route using DFS...");

        // Clear previous path visualization
        this.clearPathVisualization();

        const visited = new Set();
        const path = [];
        
        const found = await this.dfsSearch(
            this.playerPos.row, 
            this.playerPos.col, 
            visited, 
            path
        );

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
        // Base case: reached exit
        if (row === this.exitPos.row && col === this.exitPos.col) {
            path.push({ row, col });
            return true;
        }

        // Mark as visited
        const key = `${row},${col}`;
        if (visited.has(key)) return false;
        visited.add(key);

        // Check if cell is blocked (wall or infected)
        if (this.grid[row][col] === this.WALL || this.grid[row][col] === this.INFECTED) {
            return false;
        }

        // Visualize current exploration
        if (this.grid[row][col] !== this.PLAYER && this.grid[row][col] !== this.EXIT) {
            const cell = this.getCell(row, col);
            cell.classList.add('current');
            await this.sleep(this.animationSpeed / 2);
            cell.classList.remove('current');
            cell.classList.add('visited');
        }

        // Add to current path
        path.push({ row, col });

        // Try all four directions (prioritize: right, down, left, up for interesting visualization)
        const prioritizedDirections = [[0, 1], [1, 0], [0, -1], [-1, 0]];

        for (const [dr, dc] of prioritizedDirections) {
            const newRow = row + dr;
            const newCol = col + dc;

            if (this.isValid(newRow, newCol)) {
                const newKey = `${newRow},${newCol}`;
                
                if (!visited.has(newKey) && 
                    this.grid[newRow][newCol] !== this.WALL && 
                    this.grid[newRow][newCol] !== this.INFECTED &&
                    this.grid[newRow][newCol] !== this.ZOMBIE) {
                    
                    if (await this.dfsSearch(newRow, newCol, visited, path)) {
                        return true;
                    }
                }
            }
        }

        // Backtrack - remove from path
        path.pop();
        return false;
    }

    async highlightEscapePath(path) {
        for (const pos of path) {
            if (this.grid[pos.row][pos.col] !== this.PLAYER && 
                this.grid[pos.row][pos.col] !== this.EXIT) {
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
        
        // Clear all visualizations and reset to default map
        this.createDefaultMap();
        this.renderGrid();
        this.updateStatus("🔄 Game reset! Click buttons to start algorithms.");
    }
}

// ==========================================
// 🎮 INITIALIZE GAME ON PAGE LOAD
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    window.game = new ZombieEscapeGame();
    console.log('🧟‍♂️ Zombie Escape Game initialized!');
    console.log('📚 BFS = Zombie Spread | DFS = Player Escape');
});
