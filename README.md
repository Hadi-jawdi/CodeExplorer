# VCode - A Comprehensive Developer Platform

VCode is a feature-rich web application built with Django that provides a platform for developers to explore, connect, and showcase their work. The platform includes user profiles, GitHub integration, and various social features.

## 🚀 Features

- **User Authentication & Profiles**
  - Secure user registration and login
  - Customizable user profiles
  - Profile photo management
  - Social authentication integration

- **GitHub Integration**
  - GitHub repository search and exploration
  - Repository statistics and information
  - Developer activity tracking

- **Social Features**
  - User connections and networking
  - Activity feed
  - Profile exploration

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.2.1
- **Database**: SQLite3
- **Authentication**: Social Auth App Django
- **Image Processing**: Pillow
- **HTTP Client**: Requests
- **Environment Management**: Python Decouple

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Vcode
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv virtual
   # On Windows
   virtual\Scripts\activate
   # On Unix or MacOS
   source virtual/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## 📁 Project Structure

```
Vcode/
├── account_app/         # User authentication and account management
├── core/               # Core project settings and configurations
├── explore_app/        # Exploration and discovery features
├── githubsearch/       # GitHub integration and search functionality
├── media/             # User-uploaded media files
├── profile_photos/    # User profile pictures
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── user_profile_app/  # User profile management
└── manage.py          # Django management script
```

## 🔧 Configuration

1. Create a `.env` file in the project root with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   ```

2. Configure social authentication credentials in the Django admin panel

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 👥 Authors

- Hadi Jawdi -

## 🙏 Acknowledgments

- Django Documentation
- GitHub API
- Social Auth App Django
- All contributors and supporters of the project 