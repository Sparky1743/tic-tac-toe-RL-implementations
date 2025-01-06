// frontend/static/js/rewards.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('Rewards interface initialized');
    const agentSelect = document.getElementById('agent-select');
    const rewardsPlot = document.getElementById('rewards-plot');

    function updateRewardsPlot() {
        console.log('Updating rewards plot for agent:', agentSelect.value);
        rewardsPlot.innerHTML = `
            <div class="text-center">
                <span>Loading rewards plot...</span>
            </div>
        `;
        
        // Set image source directly to the backend endpoint
        const imgUrl = `/get_rewards/${agentSelect.value}`;
        rewardsPlot.innerHTML = `
            <img src="${imgUrl}" class="img-fluid" alt="Rewards Plot">
        `;
    }

    agentSelect.addEventListener('change', updateRewardsPlot);
    updateRewardsPlot();
});
