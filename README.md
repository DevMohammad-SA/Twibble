# 🐦 Twibble

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=111827)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-managed-blue?style=for-the-badge&labelColor=111827)](https://github.com/astral-sh/uv)
[![Django](https://img.shields.io/badge/Django-6.0-0C4B33?style=for-the-badge&logo=django&logoColor=white&labelColor=111827)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge&logo=opensourceinitiative&logoColor=white&labelColor=111827)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/DevMohammad-SA/Twibble?style=for-the-badge&logo=github&logoColor=white&label=Stars&color=EAB308&labelColor=111827)](https://github.com/DevMohammad-SA/Twibble/stargazers)

**Twibble** is a minimalist, Twitter-like microblogging platform built with Django.
It lets users share short posts, follow others, and explore a simple, clean social feed.

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

- **Python:** 3.12+
- **Dependency management:** uv
- **Backend:** Django 6.0
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** SQLite (for development), PostgreSQL (for production)
- **Auth:** Django built-in authentication
- **Image Processing:** Pillow
- **Env config:** `.env` (python-dotenv)
- **Linting & Formatting:** Ruff
- **Pre-commit Hooks:** Automated linting, formatting, and tests

---

## Reproducible Environment

This project uses modern python dependency management with:

- `pyproject.toml` for dependency definitions.
- `uv.lock` for exact dependency versions.

To recreate the exact environment:

```bash
uv sync
```

---

## Screenshots

_Screenshots coming soon!_

## 📦 Installation

1. **Install uv**
uv is used to manage dependencies and virtual environments.

```bash
pip install uv
```

or

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository**

```bash
git clone https://github.com/DevMohammad-SA/Twibble.git
cd Twibble
```

3. **Install dependencies**

```bash
uv sync
```

This will:

- Create a virtual environment automatically.
- Install all dependencies specified in `pyproject.toml`.
- Reproduce the exact development environment.

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
   uv run python manage.py migrate
   uv run python manage.py runserver
   ```

6. **Access the app**
   Open your browser and go to `http://127.0.0.1:8000/`

7. **Install pre-commit hooks**

   ```bash
   uv run pre-commit run --all-files
   ```

---

## To-Do

- [x] Add likes and replies
- [x] Add image uploads
- [x] Add search functionality
- [ ] Create REST API (optional)
- [x] Add notifications system
- [x] Implement hashtags support
- [x] Add Arabic locale support
- [x] Implement bookmark support

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING](./CONTRIBUTING.md) for guidelines. Feel free to open issues or submit pull requests.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Author

Made with ❤️ by Mohammad Albuainain
