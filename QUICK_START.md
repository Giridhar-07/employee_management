# Quick Start Guide - Company Management System

## 🚀 Get Running in 5 Minutes

### Windows Users

```batch
# 1. Open Command Prompt in project directory
cd company_management_system

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
python wsgi.py
```

Visit: **http://localhost:5000**

### macOS/Linux Users

```bash
# 1. Navigate to project directory
cd company_management_system

# 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
python wsgi.py
```

Visit: **http://localhost:5000**

---

## 📋 First Steps in the Application

### 1. Add Your First Employee
- Click **Employees** → **Add New Employee**
- Fill in details (Name, Email, Department, Position, Salary)
- Click **Add Employee**

### 2. Mark Attendance
- Go to **Attendance** → **Mark Attendance**
- Select employee and date
- Choose status (Present/Absent/Late/Leave)
- Click **Mark Attendance**

### 3. Generate Salary
- Go to **Salary** → **Generate Salary**
- Select month
- Add allowances/deductions if any
- Click **Generate Salary**

---

## 🌍 Deploy to Render (Free)

### Prerequisites
- GitHub account
- Repository with this code pushed to GitHub

### Deployment Steps

1. **Sign Up on Render**
   - Visit [render.com](https://render.com)
   - Click "Sign Up" and use GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Select your GitHub repository
   - Authorize if asked

3. **Configure**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Plan:** Free
   - Click "Create Web Service"

4. **Set Environment**
   - Go to "Environment" tab
   - Add: `FLASK_ENV` = `production`
   - Add: `SECRET_KEY` = Any random string
   - Click "Save"

5. **Deploy**
   - Wait for build to complete
   - Your app is live! 🎉

**Access your app:** `https://your-app-name.onrender.com`

---

## 🔧 Environment Variables

Create `.env` file in project root:

```env
FLASK_ENV=development
FLASK_APP=wsgi.py
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///company.db
```

For production (Render):
```env
FLASK_ENV=production
SECRET_KEY=<strong-random-string>
```

---

## 📚 Project Highlights

✅ **Complete Employee Management**
- Add, Edit, Delete employees
- Search and filter
- View detailed profiles
- Export to CSV

✅ **Attendance Tracking**
- Mark individual attendance
- Bulk mark for all employees
- Multiple status options
- Filter by date/employee/status

✅ **Salary Management**
- Generate monthly payroll
- Calculate with allowances/deductions
- Track payment status
- View history

✅ **Modern UI**
- Bootstrap 5 responsive design
- Professional appearance
- Mobile-friendly
- Fast and clean

---

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Edit wsgi.py line 10, change 5000 to 5001
python wsgi.py
```

**Module not found?**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**Database error?**
```bash
# Recreate database
python -c "from app import create_app, db; app = create_app()"
```

---

## 📞 Common Tasks

### Add Sample Data
```python
python

from app import create_app, db
from app.models import Employee
from datetime import datetime

app = create_app()
app.app_context().push()

emp = Employee(
    name="Jane Smith",
    email="jane@company.com",
    department="HR",
    position="Manager",
    salary=60000,
    joining_date=datetime.now(),
    status="Active"
)
db.session.add(emp)
db.session.commit()

exit()
```

### Clear Database
```bash
# Delete the database file
rm company.db  # macOS/Linux
del company.db  # Windows
```

### Run in Production Mode
```bash
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 4
```

---

## ✨ Features At A Glance

| Feature | Status |
|---------|--------|
| Employee CRUD | ✅ Complete |
| Attendance Tracking | ✅ Complete |
| Salary Management | ✅ Complete |
| Search & Filter | ✅ Complete |
| Export to CSV | ✅ Complete |
| Responsive UI | ✅ Complete |
| Free Deployment | ✅ Ready |
| Database Included | ✅ SQLite/PostgreSQL |

---

## 🎯 Next Steps

1. **Add your employees** - Start populating data
2. **Mark attendance** - Use bulk mark for efficiency
3. **Generate payroll** - Create salary records
4. **Deploy** - Get it live on Render
5. **Customize** - Adjust to your needs

---

## 📖 Full Documentation

See **README.md** for:
- Detailed API routes
- Database schema
- Customization guide
- Advanced configuration
- Security information
- Performance tips

---

**Version:** 1.0.0 | **Status:** Production Ready ✅

Happy managing! 🚀
