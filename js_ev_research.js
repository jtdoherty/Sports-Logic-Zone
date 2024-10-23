// Function to fetch data from the specific JSON file
async function fetchArbitrageData() {
    try {
        const response = await fetch("output7.json"); // Ensure this path is correct
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

    // Get the current date and the date 7 days from now
    const currentDate = new Date();
    const sevenDaysFromNow = new Date(currentDate);
    sevenDaysFromNow.setDate(currentDate.getDate() + 7);

    // Filter bets to only include those within the next 7 days
    const filteredBets = bets.filter(bet => {
        const eventDate = new Date(bet.event_start_time);
        return eventDate >= currentDate && eventDate <= sevenDaysFromNow;
    });

    // Sort filtered bets by ROI (EV) from highest to lowest
    filteredBets.sort((a, b) => b.EV - a.EV); // Sort by EV

    // Check if there are no bets
    if (filteredBets.length === 0) {
        betBody.innerHTML = '<tr><td colspan="4" class="no-data">No Arbitrage opportunities found in the next 7 days. Check back later!</td></tr>'; // Display message
        return; // Exit the function early
    }

    // Populate the table with filtered bet data
    filteredBets.forEach(bet => {
        // Ensure participants and payout exist for the bet
        if (bet.participants.length > 0) {
            const row = `
                <tr>
                    <td>
                        <strong>${bet.market_name}</strong><br>
                        <small>${bet.competition_instance_name}</small><br>
                        <small>${new Date(bet.event_start_time).toLocaleString('en-US', { weekday: 'long', hour: 'numeric', minute: 'numeric', hour12: true, timeZone: 'America/New_York', month: 'short', day: 'numeric' })} ET</small><br>
                        <small>${bet.sport}</small>
                    </td>
                    <td>
                        <strong>${bet.participants[0]}</strong><br>
                        <small>${bet.type}</small><br>
                        <small>${bet.source}</small>
                    </td>
                    <td class="centered">
                        <strong>${bet.implied_probability.toFixed(2)}%</strong><br>
                    </td>
                    <td class="centered">
                        <strong>${bet.outcome_payout}</strong><br>
                    </td>
                    <td class="roi centered">${bet.EV.toFixed(2)}%</td>
                </tr>
            `;
            betBody.innerHTML += row; // Append the new row to the table body

            // Update the Last Found At information
            const lastFoundAtElement = document.getElementById('lastFoundAt');
            if (lastFoundAtElement) {
                const lastFoundDate = new Date(bet.lastFoundAt); // Use lastFoundAt with a capital "A"
                if (!isNaN(lastFoundDate)) { // Check if the date is valid
                    lastFoundAtElement.innerHTML = `<small>Last Found At: ${lastFoundDate.toLocaleString()}</small>`;
                } else {
                    lastFoundAtElement.innerHTML = '<small>Last Found At: N/A</small>'; // Handle invalid date
                }
            }
        } else {
            console.warn("Missing participants for:", bet.market_name); // Log a warning if data is missing
        }
    });
}

// Sample ROI calculation (if needed for future modifications)
function calculateROI(outcome_payout) {
    return (outcome_payout * 100).toFixed(2) + '%'; // Simple ROI placeholder logic
}

// Tab switching functionality (unchanged)
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
