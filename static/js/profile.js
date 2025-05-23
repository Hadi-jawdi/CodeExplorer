document.addEventListener('DOMContentLoaded', function() {
    // GitHub username form handling
    const editBtn = document.getElementById('edit-github-username-btn');
    const form = document.getElementById('github-username-form');
    const container = document.getElementById('github-username-container');

    if (editBtn) {
        editBtn.addEventListener('click', function() {
            // Show form and hide username display
            container.innerHTML = `
                <form method="post" action="" id="github-username-form">
                    {% csrf_token %}
                    <div class="input-group mb-3">
                        <input type="text" name="github_username" class="form-control" placeholder="Enter GitHub username" value="{{ github_username }}">
                        <button class="btn btn-outline-info" type="submit">Save</button>
                    </div>
                </form>
            `;
        });
    }

    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.profile-sidebar .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Delete favorite confirmation
    const deleteButtons = document.querySelectorAll('.delete-favorite');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to remove this repository from your favorites?')) {
                e.preventDefault();
            }
        });
    });
}); 