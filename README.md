# 🧟‍♂️ Zombie Escape Game - BFS & DFS Visualization

An interactive web-based game that demonstrates **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** algorithms through a zombie apocalypse escape scenario.

![Game Preview](https://img.shields.io/badge/Game-Zombie%20Escape-red?style=for-the-badge)
![Algorithms](https://img.shields.io/badge/Algorithms-BFS%20%26%20DFS-blue?style=for-the-badge)
![Tech](https://img.shields.io/badge/Tech-HTML%20%7C%20CSS%20%7C%20JS-green?style=for-the-badge)

## 🎮 Game Concept

| Element | Description |
|---------|-------------|
| 🧍 **Player** | Starts at position P - trying to escape |
| 🧟 **Zombies** | Start at positions Z - spreading infection |
| 🏁 **Exit** | The escape destination E |
| ⬛ **Walls** | Block movement for both player and zombies |

### Algorithm Implementation

- **🔴 BFS (Breadth-First Search)** → Zombies spread step-by-step, infecting all adjacent cells before moving further (realistic zombie spread simulation)
- **🟢 DFS (Depth-First Search)** → Player searches for an escape path by exploring one direction completely before backtracking

### Win/Lose Conditions

- ✅ **WIN** - Player finds a path to the exit before zombies block it
- ❌ **LOSE** - Zombies reach the player or block all escape routes

## 🚀 Features

- 📊 **Real-time algorithm visualization** - Watch BFS and DFS execute step by step
- 🎨 **Color-coded paths** - Easy to understand visual feedback
- 🖱️ **Interactive grid** - Click to add/remove walls
- 🎲 **Random map generator** - Create new challenges instantly
- ⚡ **Adjustable speed** - Control animation speed with slider
- 📱 **Responsive design** - Works on desktop and mobile

## 🛠️ Tech Stack

- **HTML5** - Structure
- **CSS3** - Styling & Animations
- **JavaScript** - Core game logic & algorithms
- **Streamlit** - Python web deployment (optional)

## 📁 Project Structure

```
📦 Zombie-Escape-Game-BFS-DFS
├── 📄 index.html        # Main HTML file
├── 🎨 styles.css        # Styling and animations
├── ⚙️ game.js           # Game logic with BFS & DFS
├── 🐍 app.py            # Streamlit deployment version
├── 📋 requirements.txt  # Python dependencies
└── 📖 README.md         # Documentation
```

## 🎯 How to Run

### Option 1: Static HTML (Recommended)
Simply open `index.html` in any modern web browser.

```bash
# Clone the repository
git clone https://github.com/rithika5656/Zombie-Escape-Game-BFS-DFS.git

# Open in browser
start index.html  # Windows
open index.html   # macOS
```

### Option 2: Streamlit App
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🎮 How to Play

1. **Start the game** - The grid shows player (🧍), zombies (🧟), exit (🏁), and walls (⬛)
2. **Click "Start Zombie Spread (BFS)"** - Watch zombies infect adjacent cells level by level
3. **Click "Find Escape Path (DFS)"** - Watch the algorithm search for an escape route
4. **Customize the map** - Click on empty cells to add/remove walls
5. **Generate new maps** - Click "Random Map" for new challenges
6. **Adjust speed** - Use the slider to control animation speed

## 📚 Algorithm Details

### BFS (Breadth-First Search)
```
Time Complexity: O(V + E)
Space Complexity: O(V)
Data Structure: Queue (FIFO)
```
- Explores all neighbors at current depth before moving deeper
- Guarantees shortest path in unweighted graphs
- Perfect for simulating spread/infection patterns

### DFS (Depth-First Search)
```
Time Complexity: O(V + E)
Space Complexity: O(V)
Data Structure: Stack/Recursion
```
- Explores as far as possible along each branch before backtracking
- Memory efficient for deep graphs
- Good for pathfinding and maze solving

## 🖼️ Screenshots

### Game Grid
- 🟢 Green cells = Player position
- 🔴 Red cells = Zombie positions
- 🟡 Gold cells = Exit
- 🔵 Blue cells = Escape path (DFS result)
- 🟣 Purple cells = Infected areas (BFS result)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Rithika** - [GitHub Profile](https://github.com/rithika5656)

---

⭐ **Star this repo if you found it helpful!** ⭐

*Made with ❤️ to demonstrate Graph Algorithms*