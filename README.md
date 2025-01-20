# PathCoder

PathCoder is a Flask-based web application designed to help users create personalized learning roadmaps for learning programming. The app tailors a learning path based on the user's preferences, experience level, and goals. It provides a user-friendly dashboard with features such as task management, personalized learning paths, user registration, and progress tracking.

## Features

- **User Registration & Login**: Secure registration and login system with session management.
- **Personalized Learning Roadmap**: Based on the user’s experience level and coding preferences, an AI model API generates a customized learning path.
- **Task Management**: Users can view, update, or delete tasks in their to-do list, helping them track progress.
- **External API Integration**: Displays an inspirational quote on the dashboard, integrated from an external API.
- **Path Selection**: Users can select the coding path they want to follow (e.g., web development, game development, or data science) for a tailored learning roadmap.
- **Dynamic HTML Rendering**: Uses Jinja2 templating engine for rendering dynamic content.

## Tech Stack

- **Backend**: Flask
- **Database**: SQLite
- **ORM**: SQLAlchemy (for database management)
- **Frontend**: HTML, CSS and Jinja2 templating engine
- **External APIs**: For quote integration and AI