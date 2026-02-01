# 🐦 Twibble

**Twibble** is a minimalist, Twitter-like microblogging platform built with Django. It lets users share short posts, follow others, and explore a simple, clean social feed.

---

## Features

- User registration and login
- Post short messages (tweets)
- Follow/unfollow other users
- View a personalized feed
- User profiles with follower/following counts
- Profile editing and account settings
- Responsive design using Bootstrap 5

---

## Tech Stack

- **Python:** 3.8+
- **Backend:** Django 6.0
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite (for development), PostgreSQL (for production)
- **Auth:** Django built-in authentication
- **Image Processing:** Pillow
- **Env config:** `.env` (python-dotenv)
- **Linting & Formatting:** Ruff
- **Pre-commit Hooks:** Automated linting, formatting, and tests

---

## Screenshots

_Screenshots coming soon!_

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/DevMohammad-SA/twibble.git
   cd twibble
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   # --- For Unix-like (Mac/Linux) ---
   source venv/bin/activate       # Bash / Zsh
   source venv/bin/activate.fish  # Fish
   source venv/bin/activate.csh   # Csh / Tcsh
   source venv/bin/Activate.ps1   # PowerShell Core

   # --- For Windows ---
   venv\Scripts\activate          # Command Prompt (cmd.exe)
   .\venv\Scripts\Activate.ps1    # PowerShell
   ```

3. **Install dependencies and setup pre-commit**

   ```bash
   pip install -r requirements.txt
   pre-commit install
   ```

4. **Set up environment variables**

   Copy the example environment file and update it with your configuration:

   ```bash
   cp example.env .env
   ```

   Or create a `.env` file manually in the root directory with at minimum:

   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

   > **Security Note:** Generate a secure secret key for production. You can use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` to generate one.

   See `example.env` for additional configuration options including database, email, and timezone settings.

5. **Apply migrations and run server**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. **Access the app**
   Open your browser and go to `http://127.0.0.1:8000/`

7. **Run pre-commit hooks**

   ```bash
   pre-commit run --all-files
   ```

---

## ✅ To-Do

- [x] Add likes and replies
- [x] Add image uploads
- [x] Add search functionality
- [ ] Create REST API (optional)
- [x] Add notifications system
- [x] Implement hashtags support
- [x] Add Arabic locale support
- [x] Implement bookmark support

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

This project is open source and available for educational purposes.

---

## Author

Made with ❤️ by Mohammad Albuainain
