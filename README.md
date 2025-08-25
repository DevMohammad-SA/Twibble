# 🐦 Twibble

**Twibble** is a minimalist, Twitter-like microblogging platform built with Django. It lets users share short posts, follow others, and explore a simple, clean social feed.

---

## Features

- User registration and login
- Post short messages (tweets)
- Follow/unfollow other users
- View a personalized feed
- User profiles with follower/following counts
- ⚙ Profile editing and account settings
- Responsive design using Bootstrap 5

---

## Tech Stack

- **Backend:** Django 5.2
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite (for development)
- **Auth:** Django built-in authentication
- **Env config:** `.env`

---

## Screenshots

## No screenshots at the moment :)

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/DevMohammad-SA/twibble.git
   cd twibble
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:

   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

5. **Apply migrations and run server**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. **Access the app**
   Open your browser and go to `http://127.0.0.1:8000/`

---

## ✅ To-Do

- Add likes and replies
- Add image uploads
- Add search functionality
- Create REST API (optional)

---

## Author

Made with ❤️ by Mohammad Albuainain
