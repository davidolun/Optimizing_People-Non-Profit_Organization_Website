# Optimizing People Website

A comprehensive Django website for Optimizing People, a Christian non-profit organization dedicated to making a difference through Christ's love by providing medical care, water supply, food distribution, and spiritual support to impoverished communities.

## Features

### 🏠 **Pages**
- **Home**: Mission statement, activities overview, beliefs, featured quotes and events
- **Who We Are**: Team member profiles, organization story, values, and contact form
- **What We Do**: Detailed service descriptions, activities, and spiritual services
- **Quotes**: Inspirational quotes with random quote generator
- **Events**: Upcoming events with search functionality and event details
- **Contact**: Multiple contact forms (general, volunteer, newsletter)
- **Donate**: Comprehensive donation system with multiple giving options

### 🎨 **Design Features**
- Modern, responsive Bootstrap 5 design
- Mobile-friendly interface
- Smooth animations and hover effects
- Professional color scheme with Christian themes
- Interactive elements and forms

### 🔧 **Technical Features**
- Django 4.2.7 with Python 3.8+
- SQLite database (easily upgradeable to PostgreSQL)
- Image upload support for team photos and events
- Email notifications for contact forms
- Admin interface for easy content management
- SEO-friendly URLs and meta tags
- Security best practices implemented

### 📊 **Content Management**
- Team member management with photos and bios
- Event creation and management
- Quote management system
- Activity and belief management
- Contact message tracking
- Donation tracking

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd optimizing_people_website
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@optimizingpeople.org
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the website**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Usage

### Adding Content

1. **Team Members**
   - Go to Admin → Team Members
   - Add team member details, photos, and positions
   - Set display order for homepage

2. **Events**
   - Go to Admin → Events
   - Create upcoming events with descriptions and images
   - Mark events as featured for homepage display

3. **Quotes**
   - Go to Admin → Quotes
   - Add inspirational quotes with authors and sources
   - Mark quotes as featured for homepage display

4. **Activities**
   - Go to Admin → Activities
   - Add service descriptions and images
   - Set display order for "What We Do" page

5. **Beliefs**
   - Go to Admin → Beliefs
   - Add organizational beliefs and values

### Customization

1. **Styling**
   - Modify CSS in `templates/base.html`
   - Update color scheme in CSS variables
   - Add custom styles as needed

2. **Content**
   - Update organization information in templates
   - Modify contact information in footer
   - Add social media links

3. **Functionality**
   - Extend models in `frontend/models.py`
   - Add new views in `frontend/views.py`
   - Create new templates as needed

## Deployment

### Production Settings

1. **Update settings.py**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

2. **Database**
   - Consider upgrading to PostgreSQL for production
   - Update DATABASES setting accordingly

3. **Static Files**
   - Run `python manage.py collectstatic`
   - Configure web server to serve static files

4. **Security**
   - Use environment variables for sensitive settings
   - Enable HTTPS
   - Update SECRET_KEY

### Recommended Hosting
- Heroku
- DigitalOcean
- AWS
- PythonAnywhere

## File Structure

```
optimizing_people_website/
├── optimizing_people/          # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── frontend/                   # Main app
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # URL patterns
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Admin configuration
│   └── apps.py
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   └── frontend/              # App templates
│       ├── home.html
│       ├── who_we_are.html
│       ├── what_we_do.html
│       ├── quotes.html
│       ├── events.html
│       ├── contact.html
│       ├── donate.html
│       ├── event_detail.html
│       └── team_member_detail.html
├── media/                      # User uploaded files
├── static/                     # Static files
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Support

For support or questions about this website, please contact:
- Email: info@optimizingpeople.org
- Website: www.optimizingpeople.org

## License

This project is created for Optimizing People organization. All rights reserved.

---

**Optimizing People** - Making a difference through Christ's love
# optimizing_people
