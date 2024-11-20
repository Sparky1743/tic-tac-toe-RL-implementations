// frontend/static/js/rewards.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('Rewards interface initialized');
    const agentSelect = document.getElementById('agent-select');
    const rewardsPlot = document.getElementById('rewards-plot');

    function updateRewardsPlot() {
        console.log('Updating rewards plot for agent:', agentSelect.value);
        fetch(`/get_rewards/${agentSelect.value}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Received rewards data:', data);
                if (data.error) {
                    console.warn('Rewards error:', data.error);
                    rewardsPlot.innerHTML = `<div class="alert alert-warning">${data.error}</div>`;
                } else {
                    rewardsPlot.innerHTML = `<img src="data:image/png;base64,${data.plot}" class="img-fluid">`;
                }
            })
            .catch(error => {
                console.error('Error fetching rewards:', error);
                rewardsPlot.innerHTML = `<div class="alert alert-danger">Error loading rewards: ${error.message}</div>`;
            });
    }

    agentSelect.addEventListener('change', updateRewardsPlot);
    updateRewardsPlot();
});