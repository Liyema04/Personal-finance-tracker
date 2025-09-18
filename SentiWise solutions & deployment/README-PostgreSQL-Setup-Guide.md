# PostgreSQL Database Setup Guide for SentiWise
## Why PostgreSQL?
Using PostgreSQL from the beginning ensures:

1. Production-Development Parity: Avoid surprises when deploying

2. Advanced Features: Support for complex queries and data types

3. Scalability: Handles growth in users and data volume

4.Data Integrity: Robust transaction support and constraints

### Installation Instructions
#### Step 1: Install PostgreSQL
1. Visit PostgreSQL Download Page

2. Download the EDB installer for Windows

3. Run installer with default settings

4. Record the password for the 'postgres' superuser

5. Note the port number (default: 5432)

#### Step 2: Create Application Database
1. Open pgAdmin from Start Menu

2. Connect to PostgreSQL server using password from installation

3. Navigate to: Servers → PostgreSQL → Databases

4. Right-click → Create → Database

5. Name: sentiwise_db → Save

#### Step 3: Install Python Database Adapter
```bash
pip install psycopg2-binary
```
#### Step 4: Configure Django Settings
Update sentifinance/settings.py:

```python
# Add to imports
from decouple import config

# Replace DATABASES setting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```
#### Step 5: Environment Configuration
Create .env file in project root:

```ini
DB_NAME=sentiwise_db
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
DB_HOST=localhost
DB_PORT=5432
```
CRITICAL: Add .env to .gitignore:

```gitignore
# Environment variables
.env
```
#### Step 6: Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
#### Verification Steps
1. Run development server: python manage.py runserver

2. Access admin interface: /admin

3. Login with superuser credentials

4. Verify database connection works

### Troubleshooting Common Issues
#### Connection Refused
- Ensure PostgreSQL service is running (services.msc)

- Verify host/port in configuration

#### Authentication Failed
- Confirm username/password in .env file

- Check PostgreSQL authentication settings

#### Database Doesn't Exist
- Verify database name matches created database in pgAdmin

- Check for typos in configuration

### Production Preparation
1. Environment Variables: Use platform-specific settings for production

2. Database Backup: Implement automated backup strategy

3. Connection Pooling: Consider PGBouncer for production deployment

4. Monitoring: Set up database performance monitoring

This setup ensures a robust database foundation for SentiWise's development and future growth.