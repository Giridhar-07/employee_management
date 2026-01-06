# Company Management System

A modern, feature-rich web application for managing company employees, attendance, and payroll. Built with Python, Flask, and Bootstrap for a professional user experience.

## ✨ Features

### Employee Management
- **Add/Edit/Delete Employees** - Complete CRUD operations for employee records
- **Employee Profile** - View detailed employee information including contact details, position, and salary
- **Search & Filter** - Find employees by name, email, position, department, or status
- **Department Overview** - View employees organized by department
- **Status Management** - Track employee status (Active, Inactive, On Leave)
- **CSV Export** - Export all employee data to CSV format for external use

### Attendance Management
- **Mark Attendance** - Record individual employee attendance with detailed notes
- **Bulk Mark** - Mark attendance for multiple employees at once
- **Multiple Status Options** - Present, Absent, Late, Sick Leave, Casual Leave
- **Attendance History** - View comprehensive attendance records with filters
- **Date Range Filter** - Filter attendance by specific date ranges
- **Attendance Reports** - Track attendance patterns for individual employees

### Salary Management
- **Salary Generation** - Generate payroll for employees on monthly basis
- **Allowances & Deductions** - Add allowances (DA, HRA) and deductions (Tax, Insurance)
- **Net Salary Calculation** - Automatic calculation of net salary
- **Payment Tracking** - Track salary payment status (Pending, Paid, Failed)
- **Monthly Records** - Maintain complete salary history
- **Quick Payment Status Update** - Mark salaries as paid

### Dashboard
- **Statistics** - View total employees, active employees, departments, and daily attendance
- **Department Distribution** - Visual representation of employee distribution across departments
- **Quick Actions** - Fast access to common operations

## 🏗️ Project Structure

```
company_management_system/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   ├── routes.py             # Application routes and business logic
│   ├── templates/            # HTML templates
│   │   ├── base.html         # Base template with navbar
│   │   ├── dashboard.html    # Dashboard page
│   │   ├── about.html        # About page
│   │   ├── employees/
│   │   │   ├── list.html     # List all employees
│   │   │   ├── add.html      # Add new employee form
│   │   │   ├── edit.html     # Edit employee form
│   │   │   └── view.html     # View employee details
│   │   ├── attendance/
│   │   │   ├── list.html     # View attendance records
│   │   │   ├── mark.html     # Mark single attendance
│   │   │   └── bulk_mark.html # Bulk mark attendance
│   │   └── salary/
│   │       ├── list.html     # View salary records
│   │       └── generate.html # Generate salary
│   └── static/               # CSS, JS, images
├── config.py                 # Configuration settings
├── wsgi.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration (Heroku/Render)
├── runtime.txt              # Python version specification
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** - Programming language
- **Flask** - Lightweight web framework
- **SQLAlchemy** - Object-relational mapping (ORM)
- **Flask-SQLAlchemy** - Flask integration for SQLAlchemy
- **SQLite** - Database (local development)
- **PostgreSQL** - Database (production on Render)

### Frontend
- **Bootstrap 5** - CSS framework for responsive design
- **HTML5** - Markup language
- **CSS3** - Styling
- **JavaScript** - Client-side interactivity
- **Font Awesome** - Icon library

### Deployment
- **Gunicorn** - WSGI HTTP Server
- **Render** - Cloud hosting platform (free tier available)

## 📋 System Requirements

- **Python:** 3.9 or higher
- **Operating System:** Windows, macOS, or Linux
- **Browser:** Any modern browser (Chrome, Firefox, Safari, Edge)
- **Internet:** Required for initial setup and deployment

## 🚀 Installation & Setup

### Local Development

#### 1. Clone or Download the Project
```bash
cd company_management_system
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and update settings if needed
# For local development, defaults should work fine
```

#### 5. Initialize Database
```bash
# Create database tables
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

#### 6. Run the Application
```bash
python wsgi.py
```

The application will start on `http://localhost:5000`

#### 7. (Optional) Add Sample Data
```python
# Open Python shell
python

# In Python shell:
from app import create_app, db
from app.models import Employee
from datetime import datetime

app = create_app()
app.app_context().push()

# Add a sample employee
emp = Employee(
    name="John Doe",
    email="john@example.com",
    phone="9876543210",
    department="IT",
    position="Software Engineer",
    salary=50000.00,
    joining_date=datetime.now(),
    status="Active"
)

db.session.add(emp)
db.session.commit()
print("Sample employee added!")

exit()
```

## 📱 Usage Guide

### Dashboard
- Open `http://localhost:5000/` to access the main dashboard
- View company statistics and department distribution

### Managing Employees
1. **View All Employees** - Navigate to Employees → View All
   - Use search to find employees by name, email, or position
   - Filter by department or status
   - Sort by name, department, or salary

2. **Add New Employee** - Click "Add New Employee"
   - Fill in all required fields
   - Email must be unique
   - Salary should be monthly amount

3. **Edit Employee** - Click edit button on any employee
   - Update any information
   - Change employee status

4. **Delete Employee** - Click delete button
   - Confirmation required
   - All related attendance and salary records are also deleted

5. **Export to CSV** - Click "Export CSV" button
   - Downloads all employee data

### Managing Attendance
1. **Mark Single Attendance** - Attendance → Mark Attendance
   - Select employee and date
   - Choose status and add notes if needed

2. **Bulk Mark** - Attendance → Bulk Mark
   - Select date
   - Set status for all active employees at once
   - Save time when marking entire company attendance

3. **View Records** - Attendance → View Records
   - Filter by employee, date range, or status
   - View all historical records

### Managing Salary
1. **Generate Salary** - Salary → Generate Salary
   - Select month
   - Add allowances and deductions for each employee
   - Net salary auto-calculates
   - Salary is generated only for active employees

2. **View Records** - Salary → View Records
   - Filter by employee, month, or payment status
   - Mark salary as paid with one click

3. **Payment Tracking**
   - Track pending payments
   - Update payment status after processing

## 🌐 Deployment to Render (Free)

Render is a modern cloud platform with a generous free tier perfect for this application.

### Prerequisites
- GitHub account with project repository
- Render account (signup at render.com)

### Step-by-Step Deployment

#### 1. Push Code to GitHub
```bash
cd company_management_system

# Initialize git if not done
git init
git add .
git commit -m "Initial commit"

# Push to GitHub repository
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

#### 2. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Authorize Render to access your GitHub repositories

#### 3. Deploy on Render
1. Click "New +" button in Render dashboard
2. Select "Web Service"
3. Connect your GitHub repository
4. Fill in deployment details:
   - **Name:** `company-management-system` (or your preference)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Plan:** Select "Free" tier
   - **Region:** Choose your region
5. Click "Create Web Service"

#### 4. Configure Environment Variables
In Render dashboard:
1. Go to your service settings
2. Add environment variables:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = Generate a strong random string
   - `DATABASE_URL` = Leave for SQLite (auto-configured)

#### 5. Wait for Deployment
- Render automatically deploys on push to main branch
- Your app will be available at `your-app-name.onrender.com`

#### 6. Manage Database (First Time Setup)
Since Render uses PostgreSQL in production, the system automatically handles this with SQLAlchemy.

### Important Notes for Production
- Change `SECRET_KEY` in environment variables to a strong random value
- Use strong database credentials if using external database
- Enable HTTPS (Render does this automatically)
- Monitor logs in Render dashboard for any issues

## 📊 Database Schema

### Employees Table
```
- id (Primary Key)
- name (String, indexed)
- email (String, unique, indexed)
- phone (String)
- department (String, indexed)
- position (String)
- salary (Float)
- joining_date (DateTime)
- status (String) - Active/Inactive/On Leave
- created_at (DateTime)
- updated_at (DateTime)
```

### Attendance Table
```
- id (Primary Key)
- employee_id (Foreign Key)
- date (Date, indexed)
- status (String) - Present/Absent/Late/etc
- notes (Text)
- created_at (DateTime)
```

### SalaryRecords Table
```
- id (Primary Key)
- employee_id (Foreign Key)
- month (String) - Format: YYYY-MM
- basic_salary (Float)
- allowances (Float)
- deductions (Float)
- net_salary (Float)
- payment_status (String) - Pending/Paid/Failed
- payment_date (DateTime)
- created_at (DateTime)
```

## 🔒 Security Features

- Input validation on all forms
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection with Flask
- Password hashing ready (extensible)
- Environment variables for sensitive data
- Safe database queries with parameterization

## 🎨 Customization

### Change Theme Colors
Edit `app/templates/base.html` CSS variables:
```css
:root {
    --primary-color: #2c3e50;      /* Change primary color */
    --secondary-color: #3498db;    /* Change secondary color */
    --success-color: #27ae60;      /* Success color */
    --danger-color: #e74c3c;       /* Danger color */
}
```

### Add More Fields to Employee
1. Edit `app/models.py` - Add field to Employee class
2. Create database migration or recreate database
3. Update `app/templates/employees/add.html` and `edit.html`
4. Update `app/routes.py` if needed

### Extend Functionality
- Add leave management
- Implement performance reviews
- Add role-based access control (admin/employee/manager)
- Create advanced reporting features
- Add email notifications

## 🐛 Troubleshooting

### Issue: Database Error on Startup
**Solution:**
```bash
# Delete existing database and recreate
rm company.db  # or *.db files

# Restart application
python wsgi.py
```

### Issue: Port Already in Use
**Solution:**
```bash
# Change port in wsgi.py from 5000 to another port like 5001
python wsgi.py  # Or specify port
```

### Issue: Template Not Found
**Solution:**
- Ensure all HTML files are in `app/templates/` directory
- Check template folder structure matches routes

### Issue: Database Won't Migrate on Render
**Solution:**
- Render automatically creates tables on first deploy
- If issues persist, manually run migrations in Render Shell

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Render Deployment Guide](https://render.com/docs)

## 📝 API Endpoints (Routes)

### Main Routes
- `GET /` - Dashboard
- `GET /about` - About page

### Employee Routes
- `GET /employees/` - List employees
- `GET /employees/add` - Add employee form
- `POST /employees/add` - Submit new employee
- `GET /employees/<id>` - View employee
- `GET /employees/<id>/edit` - Edit employee form
- `POST /employees/<id>/edit` - Submit edit
- `POST /employees/<id>/delete` - Delete employee
- `GET /employees/export/csv` - Export employees

### Attendance Routes
- `GET /attendance/` - View attendance records
- `GET /attendance/mark` - Mark single attendance
- `POST /attendance/mark` - Submit attendance
- `GET /attendance/bulk-mark` - Bulk mark form
- `POST /attendance/bulk-mark` - Submit bulk attendance

### Salary Routes
- `GET /salary/` - View salary records
- `GET /salary/generate` - Generate salary form
- `POST /salary/generate` - Submit salary generation
- `POST /salary/<id>/mark-paid` - Mark salary as paid

## 🤝 Contributing

This is an educational project. Feel free to fork, modify, and improve for your use case!

## 📄 License

MIT License - Feel free to use this project for personal and commercial purposes.

## 🆘 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review the code comments
3. Check Flask and SQLAlchemy documentation
4. Enable debug mode to see detailed error messages

## ✨ Future Enhancements

- [ ] Role-based access control (Admin, Manager, Employee views)
- [ ] Leave management system
- [ ] Performance review module
- [ ] Payroll reports and analytics
- [ ] Email notifications
- [ ] Mobile app version
- [ ] Advanced search and filters
- [ ] Data backup and recovery
- [ ] Audit logs
- [ ] Department management

## 📞 Version Info

**Current Version:** 1.0.0  
**Release Date:** January 2024  
**Python Version:** 3.9+  
**Last Updated:** January 2024

---

**Built with ❤️ using Flask, SQLAlchemy, and Bootstrap**

Happy managing! 🚀
