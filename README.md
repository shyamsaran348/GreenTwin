# 🌱 GreenTwin

**A Digital Twin-Powered Plant Care Assistant**

## Problem Statement Coverage (Project #7)

This project strictly implements the "Plant Care Assistant" problem statement designed to guide users in plant management.

### ✅ Core Features
| Requirement | GreenTwin Implementation |
| :--- | :--- |
| **Guides users** | Comprehensive Dashboard + Detail Pages |
| **Tips** | "Care Tips & Schedule" Section with watering/sunlight advice |
| **Reminders** | Background Scheduler + "Next Reminder" Logic |
| **Plant Profiles** | Dedicated Plant Detail Page with Species & ID |
| **Disease Alerts** | **AI-Powered Disease Intelligence** (MobileNetV2) |
| **Garden Gallery** | "My Garden" Grid View with Plant Images |

### ✅ Frontend Features
-   **Plant Profile Forms**: "Add Plant" Modal with species selection.
-   **Care Schedule UI**: List of upcoming care tasks.
-   **Growth Timeline Charts**: **Real-Time Interactive Graph** for tracking height.
-   **Plant-ID Mock**: Integrated into Disease Intelligence (identifies species/health).
-   **Info Overlays**: Tooltips on Health & Growth Charts.
-   **Accessibility**: High-contrast Dark Mode Design.

### ✅ Backend Features
-   **Plant DB API**: RESTful API for CRUD operations (SQLite/PostgreSQL).
-   **Authentication**: Secure JWT Login/Registration.
-   **Reminder System**: Background Task Scheduler (APScheduler).
-   **Disease Info API**: Python ML Engine for inference.
-   **Image Upload Backend**: Handling multipart form data for analysis.

### 🌍 SDG Alignment
-   **Goal 2: Zero Hunger**: Promotes home gardening of food crops (e.g., Tomatoes).
-   **Goal 3: Good Health**: Encourages mental well-being through nature connection.

## Architecture

### Backend
-   **Framework**: FastAPI (Python)
-   **Database**: SQLite (Local Dev) / PostgreSQL (Prod)
-   **ML Inference**: PyTorch / MobileNet
-   **Task Queue**: APScheduler

### Frontend
-   **Framework**: React (Vite)
-   **Styling**: Modern CSS Variables (Premium Dark Theme)
-   **Visualization**: Recharts (Data Driven)

## Setup Instructions

### Backend
1.  Navigate to `backend/`:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend
1.  Navigate to `frontend/`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## License
MIT
