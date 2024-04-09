// file for where the API calls will happen when linking the FastAPI backend to the frontend

// client/client.js

async function createProfile(profileData) {
    try {
        const response = await fetch('http://localhost:8000/profiles/', {
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

export { createProfile, updateProfile, deleteProfile, createListing, updateListing, deleteListing };
