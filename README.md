# ConfigHub Setup & Run Instructions

The ConfigHub application backend and frontend are fully implemented. Follow these steps to run the application locally.

## Prerequisites

- Python 3.8+
- - PostgreSQL installed and running
  - - `createdb` command available (or manually create a database named `confighub`)
   
    - ## Setup
   
    - 1.  **Navigate to the project directory:**
      2.      ```bash
      3.      cd ConfigHub
      4.      ```
     
      5.  2.  **Create and activate a virtual environment:**
          3.      ```bash
          4.      python3 -m venv venv
          5.      source venv/bin/activate  # On Windows: venv\\Scripts\\activate
          6.      ```
        
          7.  3.  **Install dependencies:**
              4.      ```bash
              5.      pip3 install -r requirements.txt
              6.      ```
            
              7.  4.  **Database Setup:**
                  5.      Create the database and apply migrations.
                  6.      ```bash
                  7.      # createdb confighub (SQLAlchemy will use local SQLite if not found)
                  8.      export FLASK_APP=app:create_app
                  9.      flask db init
                  10.      flask db migrate -m "Initial migration"
                  11.      flask db upgrade
                  12.      ```
                
                  13.  5.  **Seed Database (Optional):**
                       6.      This creates an admin user (admin@example.com / admin123) and a demo user (user@example.com / user123), along with sample presets.
                       7.      ```bash
                       8.      python3 seed.py
                       9.      ```
                     
                       10.  ## Running the Application
                     
                       11.  1.  **Start the server:**
                            2.      You can use the provided `run.py` script:
                            3.      ```bash
                            4.    python3 run.py
                            5.    ```
                                      Or use Flask directly:
                                      ```bash
                                      flask run
                                      ```

                                  2.  **Access the application:**
                                      Open your browser and navigate to http://127.0.0.1:5001 (or the port shown in the terminal).

                                  ## Features Implemented

                                  -   **User Authentication:** Register, Login, Logout (hashed passwords).
                                  -   **Presets Management: Create (with tags, tables, images), View, Edit, Delete.
                                  -   **Exploration:** Search presets by title/description, filter public presets.
                                  -   **User Interactions:** Like presets, Archive presets.
                                  -   **User Profile:** View user's public presets, liked presets, and(if owner) archived presets.
                                  -   **Admin Dashboard:** View system stats and recent users (accessible to admin users).
                                  -   **Modern UI:** Dark-themed, responsive design with CSS variables.

                                  ## Notes on Verification

                                  Due to environment restrictions preventing direct command execution and server binding, automatic verification could not be completed. Please follow the steps above to verify the application functionality manually.
