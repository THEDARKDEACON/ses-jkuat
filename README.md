# SES JKUAT Website

A modern web application for the Society of Engineering Students at JKUAT.

## Features

- User authentication and authorization
- Event management
- News and blog system
- Photo gallery
- Member dashboard
- Responsive design

## Tech Stack

- Backend: Flask (Python)
- Frontend: HTML5, CSS3, JavaScript
- Database: PostgreSQL
- Authentication: Flask-Login
- Forms: Flask-WTF
- Email: Flask-Mail

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ses-jkuat.git
cd ses-jkuat
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application:
```bash
python run.py
```

## Development

- Backend runs on: http://localhost:5000
- Frontend runs on: http://localhost:8000

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 