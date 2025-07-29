# Quiz Frontend Application

This is the frontend application for the Quiz Platform, built with React.

## Project Structure

The project follows a component-based architecture, organized into logical folders:

-   `public/`: Static assets served directly by the web server (e.g., `index.html`, `favicon.ico`).
-   `src/`: All React source code.
    -   `assets/`: Images, icons, fonts, and other static media.
    -   `components/`: Reusable UI components, categorized by their purpose (e.g., `common`, `auth`, `quizzes`, `admin`, `results`).
    -   `contexts/`: React Context API for managing global state (e.g., `AuthContext`, `QuizContext`).
    -   `hooks/`: Custom React hooks for reusable logic (e.g., `useAuth`, `useQuizTimer`).
    -   `pages/`: Top-level components that represent different routes/views of the application (e.g., `Auth`, `Dashboard`, `Quizzes`, `Results`, `Admin`).
    -   `services/`: API interaction logic, encapsulating calls to the backend (e.g., `authService`, `quizService`, `userService`).
    -   `styles/`: Global styles (e.g., `index.css`).
    -   `App.js`: The main application component, handling global layout and routing.
    -   `index.js`: The entry point for the React application.
    -   `reportWebVitals.js`: For measuring performance metrics.

## Features

-   **User Authentication:** Login, Registration, and Logout functionality.
-   **Role-Based Access:** Differentiates between regular users and administrators.
-   **Quiz Management (Admin):** Create, edit, and delete quizzes and their questions.
-   **Quiz Taking (User):** Browse available quizzes, take quizzes with a timer, and submit answers.
-   **Results Viewing:** Users can view their past quiz results; Admins can view all results.
-   **Responsive Design:** Adapts to various screen sizes.
-   **API Integration:** Uses `axios` for interacting with a backend API (dummy data currently used for demonstration).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd quiz-frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project and add your API base URL:
    ```
    REACT_APP_API_BASE_URL=http://localhost:5000/api
    ```
    *Note: Replace `http://localhost:5000/api` with your actual backend API URL.*

4.  **Run the application:**
    ```bash
    npm start
    # or
    yarn start
    ```
    This will start the development server and open the application in your browser (usually at `http://localhost:3000`).

## Available Scripts

In the project directory, you can run:

-   `npm start`: Runs the app in development mode.
-   `npm test`: Launches the test runner.
-   `npm run build`: Builds the app for production to the `build` folder.
-   `npm run eject`: Removes the single build dependency from your project.

## API Endpoints (Conceptual)

This frontend is designed to interact with a backend API that provides endpoints similar to:

**Authentication:**
-   `POST /api/auth/login`
-   `POST /api/auth/register`
-   `POST /api/auth/logout`

**Quizzes (User/Public):**
-   `GET /api/quizzes` (Get all available quizzes)
-   `GET /api/quizzes/:quizId` (Get details of a specific quiz)
-   `GET /api/quizzes/:quizId/questions` (Get questions for taking a quiz)
-   `POST /api/quizzes/:quizId/submit` (Submit quiz answers)

**Results (User):**
-   `GET /api/results/my` (Get current user's results)
-   `GET /api/results/:quizId/:resultId` (Get a specific detailed result)

**Admin (Protected by Admin Role):**
-   `GET /api/admin/quizzes` (Manage all quizzes)
-   `POST /api/admin/quizzes`
-   `PUT /api/admin/quizzes/:quizId`
-   `DELETE /api/admin/quizzes/:quizId`
-   `GET /api/admin/quizzes/:quizId/questions` (Manage questions for a quiz)
-   `POST /api/admin/quizzes/:quizId/questions`
-   `PUT /api/admin/quizzes/:quizId/questions/:questionId`
-   `DELETE /api/admin/quizzes/:quizId/questions/:questionId`
-   `GET /api/admin/users` (Manage all users)
-   `PUT /api/admin/users/:userId/role`
-   `DELETE /api/admin/users/:userId`
-   `GET /api/admin/results` (Get all quiz results)

## Contributing

Feel free to contribute to this project. Please open an issue or submit a pull request.

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]