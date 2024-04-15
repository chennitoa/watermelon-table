// file for where the API calls will happen when linking the FastAPI backend to the frontend

async function createProfile(profileData) {
    try {
        const response = await fetch('http://localhost:8000/auth/sign-up/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(profileData),
        });
        const data = await response.json();
        console.log('Profile creation response:', data);
        return data;
    } catch (error) {
        console.error('Error creating profile:', error);
        throw error;
    }
}



async function updateProfile(profileId, updateData) {
    try {
        const response = await fetch(`http://localhost:8000/profiles/${profileId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData),
        });
        const data = await response.json();
        console.log('Profile update response:', data);
        return data;
    } catch (error) {
        console.error('Error updating profile:', error);
        throw error;
    }
}

async function deleteProfile(profileId) {
    try {
        const response = await fetch(`http://localhost:8000/profiles/${profileId}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        console.log('Profile deletion response:', data);
        return data;
    } catch (error) {
        console.error('Error deleting profile:', error);
        throw error;
    }
}

async function getProfile(identifier) {
    try {
        const response = await fetch(`http://localhost:8000/profiles/${identifier}`, {
            method: 'GET',
        });
        const data = await response.json();
        console.log('Profile retrieval response:', data);
        return data;
    } catch (error) {
        console.error('Error retrieving profile:', error);
        throw error;
    }
}

async function createListing(listingData) {
    try {
        const response = await fetch('http://localhost:8000/listings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(listingData),
        });
        const data = await response.json();
        console.log('Listing creation response:', data);
        return data;
    } catch (error) {
        console.error('Error creating listing:', error);
        throw error;
    }
}

async function updateListing(listingId, updateData) {
    try {
        const response = await fetch(`http://localhost:8000/listings/${listingId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData),
        });
        const data = await response.json();
        console.log('Listing update response:', data);
        return data;
    } catch (error) {
        console.error('Error updating listing:', error);
        throw error;
    }
}

async function deleteListing(listingId) {
    try {
        const response = await fetch(`http://localhost:8000/listings/${listingId}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        console.log('Listing deletion response:', data);
        return data;
    } catch (error) {
        console.error('Error deleting listing:', error);
        throw error;
    }
}

async function getListing(listingId) {
    try {
        const response = await fetch(`http://localhost:8000/listings/${listingId}`, {
            method: 'GET',
        });
        const data = await response.json();
        console.log('Listing retrieval response:', data);
        return data;
    } catch (error) {
        console.error('Error retrieving listing:', error);
        throw error;
    }
}

async function login(username, password) {
    try {
        const urlEncodedData = new URLSearchParams();
        urlEncodedData.append('username', username);
        urlEncodedData.append('password', password);

        const response = await fetch('http://localhost:8000/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: urlEncodedData,
        });

        const data = await response.json();
        if (response.ok) {
            console.log('Login successful:', data);
            return data;
        } else {
            throw new Error(data.message || 'Failed to login');
        }
    } catch (error) {
        console.error('Error logging in:', error);
        throw error;
    }
}

export { createProfile, updateProfile, deleteProfile, getProfile, createListing, updateListing, deleteListing, getListing, login };
