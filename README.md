# HMS
Django based Hostel Management System.



## Project Installation and Setup

1. **Create folder Locally**
    - Open the folder in VS code
       
2. **Create and activate virtual environment**

        python -m venv CRUD
        CRUD\Scripts\activate
3. **Install dependencies**

        pip install django
4. **pip install django**

        python manage.py makemigrations
        python manage.py migrate
5. **Create superuser (admin)**

        python manage.py createsuperuser
6. **Run the server**

        python manage.py runserver
7. **Access the application**
   
   - Open browser at http://127.0.0.1:8000/ → login page appears.
   - Admin panel is available at http://127.0.0.1:8000/admin/.
