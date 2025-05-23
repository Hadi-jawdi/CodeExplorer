// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showFavoriteNotification(message, profileUrl = null) {
    const notification = document.getElementById('favoriteNotification');
    if (!notification) return;
    
    notification.textContent = message;
    notification.classList.add('show');
    notification.style.cursor = profileUrl ? 'pointer' : 'default';
    notification.dataset.profileUrl = profileUrl || '';
    
    // Clear any existing timeout
    if (notification.timeoutId) {
        clearTimeout(notification.timeoutId);
    }
    
    // Set new timeout
    notification.timeoutId = setTimeout(() => {
        notification.classList.remove('show');
        notification.dataset.profileUrl = '';
    }, 3000);
}

async function addToFavorite(repoData) {
    if (!repoData || typeof repoData !== 'object') {
        showFavoriteNotification('Invalid repository data');
        return;
    }

    const csrftoken = getCookie('csrftoken');
    if (!csrftoken) {
        showFavoriteNotification('Security token missing. Please refresh the page.');
        return;
    }

    try {
        // Format the data to match what the server expects
        const formattedData = {
            full_name: repoData.full_name || '',
            html_url: repoData.html_url || '',
            description: repoData.description || '',
            language: repoData.language || '',
            stars: parseInt(repoData.stars) || 0
        };

        const response = await fetch("/user_profile/favorites/add/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'Accept': 'application/json'
            },
            body: JSON.stringify(formattedData),
            credentials: 'same-origin'
        });

        // Check if the response is JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Server returned non-JSON response');
        }

        const data = await response.json();
        
        if (data.success) {
            showFavoriteNotification(
                `'${formattedData.full_name}' has been added to your favorites! Click here to view in your profile.`,
                '/user_profile/profile/'
            );
        } else {
            showFavoriteNotification('Failed to add to favorites: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error adding to favorites:', error);
        if (error.message === 'Server returned non-JSON response') {
            showFavoriteNotification('Please log in to add repositories to favorites');
        } else {
            showFavoriteNotification('Error adding to favorites. Please try again.');
        }
    }
}

// Add click event listener to notification for dismissal or redirect
document.addEventListener('DOMContentLoaded', function() {
    const notification = document.getElementById('favoriteNotification');
    if (notification) {
        notification.addEventListener('click', function() {
            const profileUrl = this.dataset.profileUrl;
            if (profileUrl) {
                window.location.href = profileUrl;
            } else {
                this.classList.remove('show');
            }
            if (this.timeoutId) {
                clearTimeout(this.timeoutId);
            }
        });
    }
}); 