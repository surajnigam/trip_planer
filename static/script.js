document.getElementById('userForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    try {
        const response = await fetch('/add_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email }),
        });

        const result = await response.json();
        if (result.status) {
            alert(result.status);
        } else if (result.error) {
            alert(result.error);
        }
        loadUsersData();
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding the user.');
    }
});

document.getElementById('tripForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const user_id = document.getElementById('user_id').value;
    const destination = document.getElementById('destination').value;
    const start_date = document.getElementById('start_date').value;
    const end_date = document.getElementById('end_date').value;
    const budget = document.getElementById('budget').value;

    try {
        const response = await fetch('/add_trip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id, destination, start_date, end_date, budget }),
        });

        const result = await response.json();
        if (result.status) {
            alert(result.status);
        } else if (result.error) {
            alert(result.error);
        }
        loadTripsData();
        loadPlacesData();
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding the trip.');
    }
});

document.getElementById('showDataButton').addEventListener('click', async () => {
    const dataTables = document.getElementById('dataTables');
    const showDataButton = document.getElementById('showDataButton');
    if (dataTables.style.display === 'none' || dataTables.style.display === '') {
        dataTables.style.display = 'block';
        showDataButton.textContent = 'HIDE DATA';
        await loadUsersData();
        await loadTripsData();
    } else {
        dataTables.style.display = 'none';
        showDataButton.textContent = 'SHOW DATA';
    }
});

async function loadUsersData() {
    try {
        const response = await fetch('/users');
        const users = await response.json();
        const usersTableBody = document.querySelector('#users tbody');
        usersTableBody.innerHTML = '';
        users.forEach(user => {
            usersTableBody.innerHTML += `
                <tr>
                    <td>${user.user_id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                </tr>
            `;
        });
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while loading users.');
    }
}

async function loadTripsData() {
    try {
        const response = await fetch('/trips');
        const trips = await response.json();
        const tripsTableBody = document.querySelector('#trips tbody');
        tripsTableBody.innerHTML = '';
        trips.forEach(trip => {
            tripsTableBody.innerHTML += `
                <tr>
                    <td>${trip.trip_id}</td>
                    <td>${trip.user_id}</td>
                    <td>${trip.destination}</td>
                    <td>${trip.start_date}</td>
                    <td>${trip.end_date}</td>
                    <td>${trip.budget}</td>
                </tr>
            `;
        });
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while loading trips.');
    }
}

async function loadPlacesData() {
    try {
        const response = await fetch('/places');
        const places = await response.json();
        const placesDiv = document.getElementById('places');
        placesDiv.innerHTML = '';
        places.forEach(place => {
            const placeDiv = document.createElement('div');
            placeDiv.className = 'place';
            placeDiv.textContent = `Destination: ${place.destination}, Place: ${place.place}, Category: ${place.category}, Cost: ${place.cost}`;
            placesDiv.appendChild(placeDiv);
        });
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while loading places.');
    }
}
