# Resume & CV Builder

A powerful, Django-based web application designed to help users create professional Resumes and comprehensive academic CVs with ease. Choose from a variety of premium templates and customize your document to fit your career goals.

## Key Features

### 1. Distinct Resume & CV Builders
*   **Resume Builder**: Tailored for industry roles. Focuses on Professional Experience, Education, and Skills.
*   **CV Builder**: Tailored for academic and research roles. Includes additional sections for **Research**, **Publications**, and **Awards & Honors**.

### 2. Premium Templates
Choose from 11 distinct, professionally designed templates:
*   **Modern**: Clean and balanced.
*   **Classic**: Traditional Time New Roman style.
*   **Creative**: Colorful and unique.
*   **Elegant Serif**: Sophisticated and minimalist.
*   **Executive Pro**: Bold with a strong sidebar.
*   **Minimalist Clean**: Whitespace-heavy and simple.
*   **Vertical Timeline**: Creative timeline layout on dark mode.
*   **Tech Modern**: Code-inspired dark theme.
*   **Academic Professional**: Dense, text-heavy layout for CVs.
*   **Designer Bold**: High contrast and artistic.
*   **Compact Single Page**: Optimized to fit everything on one page.

### 3. Dynamic Definitions
*   Add or remove sections (Experience, Education, Skills, Research, Publications, Awards) dynamically using JavaScript.
*   Real-time updates to your document structure.

### 4. User Dashboard
*   Manage multiple Resumes and CVs.
*   Visual badges to distinguish between document types.
*   Edit or delete documents easily.

## Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd resume-builder
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Start the Server**
    ```bash
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000` in your browser.

## Usage

1.  **Register/Login**: Create an account to save your documents.
2.  **Choose Document**: Select "Create Resume" or "Create CV" from the dashboard or home page.
3.  **Fill Details**: Enter your personal info, experience, education, and other details. New sections like Research will appear automatically if you chose "CV".
4.  **Select Template**: Choose one of the 11 templates from the dropdown.
5.  **Save & Print**: Save your document. Use your browser's "Print to PDF" feature (Ctrl+P / Cmd+P) to save the final output as a PDF. **Background graphics must be enabled in print settings.**

## Technologies Used
*   **Backend**: Python, Django
*   **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
*   **Database**: SQLite (default) / PostgreSQL (compatible)
