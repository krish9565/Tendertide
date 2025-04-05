git clone <repository-url>
cd tendertide
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install django>=5.1.6
pip install django-crispy-forms>=2.3
pip install crispy-bootstrap5>=2024.10
pip install pillow>=11.1.0
pip install python-dotenv>=1.0.1
pip install psycopg2-binary>=2.9.10
```

4. Create a `.env` file in the project root with the following variables:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DATABASE_URL=postgresql://user:password@localhost:5432/tendertide
PGDATABASE=tendertide
PGUSER=your_username
PGPASSWORD=your_password
PGHOST=localhost
PGPORT=5432
```

5. Create the PostgreSQL database:
```bash
createdb tendertide
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Project Structure
- `accounts/` - User authentication and profile management
- `tenders/` - Core tender management functionality
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)

### Available URLs
- Home: `/`
- Admin Dashboard: `/admin/`
- Login: `/accounts/login/`
- Register: `/accounts/register/`
- Tender List: `/tenders/`

### Development Guidelines
1. Always run migrations after modifying models
2. Use the Django admin interface for data management
3. Follow PEP 8 style guide for Python code
4. Test thoroughly before committing changes

## Troubleshooting

### Common Issues

1. PostgreSQL Connection Issues:
   - Verify PostgreSQL is running: 
     ```bash
     # Windows
     net start postgresql
     # macOS
     brew services list
     # Linux
     sudo systemctl status postgresql
     ```
   - Check connection settings in `.env` file
   - Ensure database user has proper permissions

2. Migration Issues:
   - If you get "relation does not exist" errors:
     ```bash
     python manage.py migrate --run-syncdb
     ```
   - For other migration issues:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. Static Files Not Loading:
   - Run collectstatic:
     ```bash
     python manage.py collectstatic
     ```
   - Verify STATIC_ROOT and STATIC_URL in settings.py

4. Dependencies Issues:
   - Update pip:
     ```bash
     python -m pip install --upgrade pip
     ```
   - Install all dependencies with specific versions:
     ```bash
     pip install -r requirements.txt