![png (1)](https://github.com/user-attachments/assets/9c555e73-11f6-40c7-b8e4-c8e41d009354)

## 📝 Django Ink Spill

A simple blogging web app built with Django 5.2 and basic HTML/CSS, designed for sharing thoughts, fan theories, or short stories. It supports post creation, editing, and includes user authentication features.

🔗 Live Demo: https://django-project-jwx4.onrender.com

### ✨ Features
* 🏠 Home Page with blog summaries
* 📄 Full post pages for individual reading
* ✍️ Create, edit, and delete blog posts (for logged-in users)
* 🔐 Login and Sign Up system
* 📦 Clean project structure using Django's templating system
* 🎨 Styled using basic custom CSS (no framework)

### ⚙️ Tech Stack
* Backend: Django 5.2
* Frontend: Django Templates + HTML/CSS
* Database: SQLite (default Django DB)
* Language: Python 3.13.1

### 🚀 Getting Started Locally
#### 1.Create a virtual environment
``` python -m venv .venv ```
#### 2. Activate the virtual environment
```.venv\Scripts\activate```
#### 3. Install dependencies
``` pip install -r requirements.txt```
#### 4. Run database migrations
``` python manage.py migrate```
#### 5. python manage.py runserver
``` python manage.py runserver ```
#### 6. Click the Link given, or go to
``` http://127.0.0.1:8000/ ```
### 📌 Notes
Don't forget to create a ```.env``` file and configure any secrets (like Django's SECRET_KEY) before 
``` 
DEBUG= True
SECRET_KEY=
DATABASE_URL=
ALLOWED_HOSTS=
```
### Models

#### The application has two main models:

1. **Post**: Represents a blog post with title, description, content, author, and creation timestamp.
2. **Comment**: Represents a comment on a post with author information, content, and creation timestamp. 
  The `hash_email` function provides privacy by hashing email addresses using HMAC with a random salt.
### Views

The application uses both class-based and function-based views:

- **Class-based views**:

- `PostListView`: Displays a paginated list of posts
- `PostDetailView`: Shows a single post with its comments
- `PostCreateView`: Handles post creation
- `PostUpdateView`: Handles post editing
- `PostDeleteView`: Handles post deletion
- `SignUpView`: Handles user registration
- `CustomLoginView`: Handles user login



- **Function-based views**:

- `logout_view`: Handles user logout
- `add_comment`: Handles comment creation
- `custom_404`: Displays custom 404 page

### Forms

The application uses Django forms for data validation:

- `PostForm`: Form for creating and editing posts

## 🖼️ Usage

### Creating a Post

1. Log in to your account
  ![image](https://github.com/user-attachments/assets/f30e0dc3-7f1e-48b8-9106-33f8f705cead)

2. Click on "New Post" button
  ![image](https://github.com/user-attachments/assets/f4b9b263-7815-4173-80b2-dd0429087598)

3. Fill in the title, description, and content
  ![image](https://github.com/user-attachments/assets/94409c28-62e1-4599-a2dd-de76cf37093b)

4. Click "Submit"
  ![image](https://github.com/user-attachments/assets/07fb151f-d6b7-4e55-b908-73ad0a64f73b)



### Commenting on a Post

1. Navigate to a post detail page
2. Scroll to the comment section
3. Enter your comment
4. Click "Submit"
  ![image](https://github.com/user-attachments/assets/08575654-340c-4fe8-9109-f035114893d1)



### Managing Your Posts

1. Log in to your account
2. Navigate to your post
3. Use the edit buttons to manage your post

  ![image](https://github.com/user-attachments/assets/40cc3a4e-6386-4efb-82df-220bf0804d92)

4. Use the Submit to Finalize the Edit  
  ![image](https://github.com/user-attachments/assets/b9c3c02b-302c-4929-8490-04c37667647b)




### 📃 License
This project is open-source and free to use.
