# Vendora 🛍️  
An online storefront platform built with Django, designed to empower local vendors and sellers to reach customers easily.

## Live Demo  
🔗 [https://vendora.pythonanywhere.com](https://vendora.pythonanywhere.com)  

## Tech Stack  
- **Backend:** Python 3 · Django · Django-restframework
- **Database:** SQLite (for now) - would migrate to postgres 
- **Frontend:** HTML · CSS · Bootstrap-inspired custom styles  
- **Dev Environment:** Termux on Android (1 GB RAM device) · Vim Editor 
- **Deployment:** PythonAnywhere  

## Features  
- Vendor registration,email verification, login & dashboard  
- notifications
- Product listing & management  
- Customer browsing of products by category
- Payment Gateway · paystack
- Responsive UI for mobile & desktop  
- Built and deployed entirely on constrained hardware  

## Installation & Local Setup
You could use the below guide or make use of the helper script. The media files are compressed and also available.
```bash
git clone https://github.com/Granzular/vendora.git  
cd vendora  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver
