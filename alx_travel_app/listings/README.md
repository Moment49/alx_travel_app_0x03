# ALX Travel App

ALX Travel App is a Django-based web application designed to help users find, list, and manage travel destinations and experiences. The app provides a platform for users to explore listings, add new destinations, and manage their travel plans efficiently.

## Features

- User authentication and registration
- Add, edit, and delete travel listings
- Browse and search for destinations
- Admin dashboard for managing listings
- Responsive and user-friendly interface

## Project Structure

```
alx_travel_app/
    manage.py
    requirements.txt
    alx_travel_app/
        settings.py
        urls.py
        ...
    listings/
        models.py
        views.py
        admin.py
        ...
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtualenv (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x00
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your browser and go to `http://127.0.0.1:8000/`.
2. Register a new account or log in.
3. Browse, add, or manage travel listings.

## Running Tests

To run tests:
```bash
python manage.py test
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- ALX Africa
- Django Documentation
