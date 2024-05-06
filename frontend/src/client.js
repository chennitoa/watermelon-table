// file for where the API calls will happen when linking the FastAPI backend to the frontend

// AUTH
async function createUser(profileData) {
  try {
    const response = await fetch("http://localhost:5001/auth/sign-up/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(profileData),
    });
    const data = await response.json();
    console.log("Profile creation response:", data);
    return data;
  } catch (error) {
    console.error("Error creating profile:", error);
    throw error;
  }
}

async function login(username, password) {
  try {
    const urlEncodedData = new URLSearchParams();
    urlEncodedData.append("username", username);
    urlEncodedData.append("password", password);

    const response = await fetch("http://localhost:5001/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: urlEncodedData,
    });

    const data = await response.json();
    if (response.ok) {
      console.log("Login successful:", data);
      return data;
    } else {
      throw new Error(data.message || "Failed to login");
    }
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
}

// PROFILES
async function updateProfile(updateData) {
  try {
    const response = await fetch(`http://localhost:5001/profiles/update/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    });
    const data = await response.json();
    console.log("Profile update response:", data);
    return data;
  } catch (error) {
    console.error("Error updating profile:", error);
    throw error;
  }
}

async function getProfile(username) {
  try {
    const response = await fetch(`http://localhost:5001/profiles/${username}`, {
      method: "GET",
    });
    const data = await response.json();
    console.log("Profile retrieval response:", data);
    return data;
  } catch (error) {
    console.error("Error retrieving profile:", error);
    throw error;
  }
}

// USER
async function updateUser(updateData) {
  try {
    const response = await fetch(`http://localhost:5001/user/update/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    });
    const data = await response.json();
    console.log("User update response:", data);
    return data;
  } catch (error) {
    console.error("Error updating profile:", error);
    throw error;
  }
}

async function getUserWithUsername(username) {
  try {
    const response = await fetch(
      `http://localhost:5001/user/usernameget/${username}`,
      {
        method: "GET",
      }
    );
    const data = await response.json();
    console.log("User retrieval response:", data);
    return data;
  } catch (error) {
    console.error("Error retrieving profile:", error);
    throw error;
  }
}

async function getUserWithUserId(user_id) {
  try {
    const response = await fetch(
      `http://localhost:5001/user/idget/${user_id}`,
      {
        method: "GET",
      }
    );
    const data = await response.json();
    console.log("User retrieval response:", data);
    return data;
  } catch (error) {
    console.error("Error retrieving profile:", error);
    throw error;
  }
}

async function getCurrentUser() {
  try {
    const token = localStorage.getItem("token"); // Assuming the token is stored in localStorage
    const response = await fetch("http://localhost:5001/user/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`, // Include the token in the Authorization header
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    console.log("Profile retrieval response:", data);
    return data;
  } catch (error) {
    console.error("Error retrieving profile:", error);
    throw error;
  }
}

// LISTINGS
async function createListing(listingData) {
  try {
    const response = await fetch("http://localhost:5001/listings/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(listingData),
    });
    const data = await response.json();
    console.log("Listing creation response:", data);
    return data;
  } catch (error) {
    console.error("Error creating listing:", error);
    throw error;
  }
}

async function updateListing(updateData) {
  try {
    const response = await fetch(`http://localhost:5001/listings/update/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    });
    const data = await response.json();
    console.log("Listing update response:", data);
    return data;
  } catch (error) {
    console.error("Error updating listing:", error);
    throw error;
  }
}

async function deleteListing(listingId) {
  try {
    const response = await fetch(
      `http://localhost:5001/listings/${listingId}`,
      {
        method: "DELETE",
      }
    );
    const data = await response.json();
    console.log("Listing deletion response:", data);
    return data;
  } catch (error) {
    console.error("Error deleting listing:", error);
    throw error;
  }
}

async function getListing(searchCriteria) {
  try {
    const response = await fetch("http://localhost:5001/listings/search/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(searchCriteria),
    });

    const data = await response.json();
    console.log("Listing retrieval response:", data);
    return data;
  } catch (error) {
    console.error("Error retrieving listing:", error);
    throw error;
  }
}

// RATINGS
async function rateProfile() {
  try {
    const token = localStorage.getItem("token"); // Assuming the token is stored in localStorage
    const response = await fetch("http://localhost:5001/ratings/rate/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`, // Include the token in the Authorization header
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    console.log("Profile retrieval response:", data);
    return data;
  } catch (error) {
    console.error("Error retrieving profile:", error);
    throw error;
  }
}

async function updateRating(updateData) {
  try {
    const response = await fetch(`http://localhost:5001/ratings/update/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updateData),
    });
    const data = await response.json();
    console.log("Listing update response:", data);
    return data;
  } catch (error) {
    console.error("Error updating listing:", error);
    throw error;
  }
}

async function getAllRatings(username) {
  try {
    const response = await fetch(`http://localhost:5001/listings/${username}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(username),
    });

    const data = await response.json();
    console.log("Listing retrieval response:", data);
    return data;
  } catch (error) {
    console.error("Error retrieving listing:", error);
    throw error;
  }
}

async function getSpecificRating(raterName, ratedName) {
  try {
    const response = await fetch(
      `http://localhost:5001/ratings/get/?rater_name=${raterName}&rated_name=${ratedName}`
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error getting specific rating:", error);
    throw error;
  }
}

async function getUserRating(username) {
  try {
    const response = await fetch(
      `http://localhost:5001/ratings/average/${username}`
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error getting user rating:", error);
    throw error;
  }
}

export {
  createUser,
  updateProfile,
  getProfile,
  updateUser,
  getUserWithUsername,
  getUserWithUserId,
  getCurrentUser,
  createListing,
  updateListing,
  deleteListing,
  getListing,
  login,
  rateProfile,
  updateRating,
  getAllRatings,
  getSpecificRating,
  getUserRating,
};
