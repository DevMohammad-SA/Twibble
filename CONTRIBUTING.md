# Contributing to Twibble

Thank you for considering contributing to Twibble!

## How Can I Contribute ?

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- **Description**: A clear description of the bug
- **Steps to Reproduce**: How to reproduce the issue
- **Expected Behavior**: What you expect to happen
- **Actual Behavior**: What actually happened
- **Screenshots**: If applicable
- **Environment**: Python version, Django version, OS

### Suggesting Feature

Feature requests are welcome! Please create an issue with the following information:

- **Description**: A clear description of the feature
- **Use Case**: Why this feature would be useful
- **Possible Implementation**: If you have ideas on how to implement it

### Pull Requests

1. **Fork the repository** and create your branch from `master`
2. **Make your changes** following our coding standards
3. **Test your changes** throughly
4. **Update documentation** if needed
5. **Commit your changes** with clear commit messages
6. **Push to your fork** and submit a pull request

## Development Setup

1. **Clone your fork:**

```bash
git clone https://github.com/DevMohammad-SA/Twibble.git
cd Twibble
```

2. **Create a virtual environment:**

  ```bash
  python -m venv venv
  source venv/bin/activate # On Windows: venv\Scripts\activate
  ```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

```bash
cp example.env .env
# Edit .env with your configuration
```

5. **Run migrations:**

```bash
python manage.py migrate
```

6. **Create a superuser:**

```bash
python manage.py createsuperuser
```

7. **Run the development server:**

```bash
python manage.py runserver
```

## Coding Standards

### Pre-commit hooks

We use pre-commit hooks to maintain code quality. Install them:

```bash
pip install pre-commit
pre-commit install
```

The hooks will automatically run on each commit to check:

- Code formatting
- Linting
- Template formatting (djlint)

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstring to functions and classes
- Keep functions small and focused

### Django Best Practices

- Follow Django's [coding style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- Use Django's built-in features when possible
- Write tests for new features
- Use class-based views when appropriate

### Commit messages

Write clear commit messages:

```
Add user editing feature

- Created ProfileUpdateView
- Added profile edit form
- Updated user profile template
- Added tests for profile editing
```

Format:

- Use present tense ("Add feature" not "Added feature")
- First line: brief summary (50 chars or less)
- Blank line, then detailed description if needed

## Testing

Run tests before submitting a pull request:

```bash
python manage.py test
```

Write tests for new features:

- Place tests in the appropriate app's `tests.py`
- Follow Django's testing conventions
- Aim for good test coverage

## Code Review Process

1. Maintainers will review your pull request
2. Address any requested changes
3. Once approved, your PR will be merged

## Questions ?

Feel free to create an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see [LICENCSE](LICENSE)).
