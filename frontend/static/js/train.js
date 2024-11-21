// frontend/static/js/train.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('Training interface initialized');
    const socket = io();
    const trainForm = document.getElementById('train-form');
    const progressBar = document.querySelector('.progress-bar');
    const trainStatus = document.getElementById('training-status');
    const agentTypeSelect = document.getElementById('agent-type');
    const trainMethodGroup = document.getElementById('train-method-group');
    const episodesGroup = document.getElementById('episodes-group');

    socket.on('connect', () => {
        console.log('Socket connected');
    });

    agentTypeSelect.addEventListener('change', () => {
        const agentType = agentTypeSelect.value;
        if (agentType === 'q' || agentType === 's') {
            trainMethodGroup.style.display = 'block';
            episodesGroup.style.display = 'block';
        } else {
            trainMethodGroup.style.display = 'none';
            episodesGroup.style.display = 'none';
        }
    });

    trainForm.addEventListener('submit', (e) => {
        try {
            e.preventDefault();
            const data = {
                agent_type: agentTypeSelect.value,
                method: agentTypeSelect.value === 'q' || agentTypeSelect.value === 's' ? document.getElementById('train-method').value : null,
                episodes: agentTypeSelect.value === 'q' || agentTypeSelect.value === 's' ? parseInt(document.getElementById('episodes').value) : null,
                load_existing: document.getElementById('load-existing').checked
            };
            console.log('Starting training with params:', data);
            
            progressBar.style.width = '0%';
            trainStatus.textContent = 'Training started...';
            socket.emit('start_training', data);
        } catch (error) {
            console.error('Error starting training:', error);
        }
    });

    socket.on('training_progress', (data) => {
        progressBar.style.width = `${data.progress}%`;
        trainStatus.textContent = data.message;
    });

    socket.on('training_complete', () => {
        trainStatus.textContent = 'Training complete!';
        progressBar.style.width = '100%';
    });

    socket.on('training_error', (data) => {
        console.error('Training error:', data.message);
        trainStatus.textContent = 'Error: ' + data.message;
        trainStatus.classList.add('text-danger');
    });
});