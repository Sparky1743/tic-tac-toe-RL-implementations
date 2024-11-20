// frontend/static/js/game.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('Game interface initialized');
    const socket = io();
    const gameBoard = document.querySelector('.game-board');
    const cells = document.querySelectorAll('.cell');
    const gameStatus = document.querySelector('.game-status');
    const newGameBtn = document.getElementById('new-game');
    const agentSelect = document.getElementById('agent-select');
    
    let gameActive = true;
    
    socket.on('connect', () => {
        console.log('Socket connected');
    });

    socket.on('error', (data) => {
        console.error('Server error:', data.message);
        gameStatus.textContent = 'Error: ' + data.message;
        gameStatus.className = 'alert alert-danger';
    });

    // Handle cell clicks
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            if (cell.textContent === '-' && gameActive) {
                makeMove(cell);
            }
        });
    });

    function makeMove(cell) {
        try {
            const [row, col] = cell.dataset.pos.split(',');
            console.log(`Making move at ${row},${col}`);
            
            cell.textContent = 'X';
            cell.classList.add('x');
            cell.disabled = true;

            socket.emit('player_move', {
                row: parseInt(row),
                col: parseInt(col),
                agent: agentSelect.value
            });
        } catch (error) {
            console.error('Error making move:', error);
        }
    }

    // Handle agent's move
    socket.on('agent_move', (data) => {
        try {
            console.log('Agent move received:', data);
            const cell = document.querySelector(`[data-pos="${data.row},${data.col}"]`);
            cell.textContent = 'O';
            cell.classList.add('o');
            cell.disabled = true;
            
            if (data.game_over) {
                gameActive = false;
                gameStatus.textContent = data.message;
                gameStatus.className = `alert ${data.winner === 'O' ? 'alert-danger' : 'alert-success'}`;
            }
        } catch (error) {
            console.error('Error handling agent move:', error);
        }
    });

    // New game button
    newGameBtn.addEventListener('click', () => {
        cells.forEach(cell => {
            cell.textContent = '-';
            cell.className = 'cell';
            cell.disabled = false;
        });
        gameActive = true;
        gameStatus.textContent = "Your turn! Select a cell to place 'X'";
        gameStatus.className = 'alert alert-info';
        
        socket.emit('new_game', {
            agent: agentSelect.value
        });
    });
});