# SES JKUAT Backend

This is the backend API for the Society of Engineering Students (SES) JKUAT website.

## Features

- User authentication and authorization
- Event management
- Blog post management
- File upload handling
- Admin dashboard
- RESTful API endpoints

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
ADMIN_EMAIL=admin@sesjkuat.com
ADMIN_PASSWORD=your-admin-password
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

1. Start the development server:
```bash
python run.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Authentication
- POST `/api/register` - Register a new user
- POST `/api/login` - Login user
- GET `/api/profile` - Get user profile
- PUT `/api/profile` - Update user profile

### Events
- GET `/api/events` - Get all events
- GET `/api/events/<id>` - Get specific event
- GET `/api/events/categories` - Get event categories
- GET `/api/events/upcoming` - Get upcoming events
- GET `/api/events/past` - Get past events

### Blog
- GET `/api/blog` - Get all blog posts
- GET `/api/blog/<id>` - Get specific blog post
- GET `/api/blog/categories` - Get blog categories
- GET `/api/blog/tags` - Get blog tags
- GET `/api/blog/featured` - Get featured posts
- POST `/api/blog/<id>/like` - Like a blog post

### Admin
- GET `/api/admin/users` - Get all users
- PUT `/api/admin/users/<id>` - Update user
- POST `/api/admin/events` - Create event
- PUT `/api/admin/events/<id>` - Update event
- POST `/api/admin/blog` - Create blog post
- PUT `/api/admin/blog/<id>` - Update blog post

## Development

- The application uses Flask for the backend
- SQLAlchemy for database ORM
- JWT for authentication
- Flask-Migrate for database migrations
- Flask-CORS for handling CORS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 