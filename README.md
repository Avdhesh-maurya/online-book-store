# OBS Project

This is a Django-based web application for managing books, categories, users, and admin functionalities. The project includes multiple apps (`adminapp`, `mainapp`, `userapp`) and supports media uploads, static files, and user authentication.

## Features
- Admin dashboard for managing books and categories
- User registration and login
- Book details and search functionality
- Media and static file support

## Project Structure
- `adminapp/` - Admin-related features
- `mainapp/` - Main application logic
- `userapp/` - User-related features
- `My_project/` - Django project settings and configuration
- `media/` - Uploaded files and images
- `static/` - Static assets (CSS, JS, images)

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```sh
   python manage.py migrate
   ```
4. Start the development server:
   ```sh
   python manage.py runserver
   ```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
For any inquiries, please contact the project maintainer.
