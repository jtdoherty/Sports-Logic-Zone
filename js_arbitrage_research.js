// Function to fetch data from the specific JSON file
async function fetchArbitrageData() {
    try {
        const response = await fetch('filtered_arbitrage_data.json'); // Ensure this path is correct
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error loading arbitrage data:", error);
        return []; // Return an empty array in case of error
    }
}

// Function to populate the table with fetched data
function populateTable(bets) {
    const betBody = document.getElementById('bet-body');
    betBody.innerHTML = ''; // Clear any existing rows

    // Check if there are no bets
    if (bets.length === 0) {
        betBody.innerHTML = '<tr><td colspan="4" class="no-data">No Arbitrage opportunities found. Check back later!</td></tr>'; // Display message
        return; // Exit the function early
    }

    // Populate the table with bet data
    bets.forEach(bet => {
        // Ensure outcomes have at least two bets to show
        if (bet.outcomes.length >= 2) {
            const row = `
                <tr>
                    <td>
                        ${bet.event_name}<br>
                        <small>${bet.competition_name}</small><br>
                        <small>${new Date(bet.start_time).toLocaleString()}</small>
                    </td>
                    <td>
                        ${bet.outcomes[0].type}<br>
                        <strong>${bet.outcomes[0].payout}</strong><br>
                        <small>${bet.outcomes[0].source}</small>
                    </td>
                    <td>
                        ${bet.outcomes[1].type}<br>
                        <strong>${bet.outcomes[1].payout}</strong><br>
                        <small>${bet.outcomes[1].source}</small>
                    </td>
                    <td class="roi">${calculateROI(bet.outcomes)}</td>
                </tr>
            `;
            betBody.innerHTML += row; // Append the new row to the table body

            // Update the Last Found At information
            const lastFoundAtElement = document.getElementById('lastFoundAt');
            if (lastFoundAtElement) {
                lastFoundAtElement.innerHTML = `<small>Last Found At: ${new Date(bet.last_found_at).toLocaleString()}</small>`;
            }
        } else {
            console.warn("Not enough outcomes for:", bet.event_name); // Log a warning if data is missing
        }
    });
}

// Sample ROI calculation function
function calculateROI(outcomes) {
    // Assuming simple ROI calculation based on payouts
    const payout1 = outcomes[0].payout;
    const payout2 = outcomes[1].payout;
    return ((1 / payout1 + 1 / payout2) * 100 - 100).toFixed(2) + '%';
}

// Tab switching functionality
const preGameBtn = document.getElementById('pre-game-btn');

preGameBtn.addEventListener('click', function () {
    preGameBtn.classList.add('active');
    loadPreGameData(); // Load pre-game data if applicable
});



// Function to load pre-game data
async function loadPreGameData() {
    try {
        const bets = await fetchArbitrageData(); // Fetch the data
        populateTable(bets); // Populate the table with fetched data
    } catch (error) {
        console.error("Could not load arbitrage data:", error);
    }
}


// DOMContentLoaded to initialize page
document.addEventListener('DOMContentLoaded', async function () {
    preGameBtn.classList.add('active'); // Set Pre-Game as active on page load
    loadPreGameData(); // Load pre-game data initially
});
