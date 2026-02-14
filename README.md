# 🌱 GreenTwin

**An Intelligent Plant Care Assistant Powered by Digital Twins**

## Problem Statement
Plant care is often inconsistent, reactive, and knowledge-heavy. GreenTwin addresses this by providing a unified plant care assistant that combines guidance, monitoring, and intelligence into a single, reliable system.

## Solution Overview
GreenTwin is a full-stack, production-ready plant care web application. Each plant is represented as a digital twin — a continuously updated digital representation that reflects the plant’s health, growth, stress, and disease risk.

### Key Innovations
1.  **Digital Twins for Plants**: Live internal state evolving over time.
2.  **Integrated Disease Intelligence**: ML-based disease risk assessment from leaf images.
3.  **Unified Assistant Experience**: Coherent interface for care tips, reminders, and alerts.

## Architecture

### Backend
-   **Framework**: FastAPI (Python)
-   **Database**: PostgreSQL
-   **ML Inference**: PyTorch / MobileNet
-   **Task Queue**: APScheduler

### Frontend
-   **Framework**: React (Vite)
-   **Styling**: CSS Modules / Styled Components
-   **State Management**: React Context

### ML Models
-   **Tomato Disease Model**: CNN based on MobileNetV2, trained on PlantVillage dataset.

## Setup Instructions

### Prerequisites
-   Python 3.9+
-   Node.js 16+
-   PostgreSQL

### Backend Setup
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

### Frontend Setup
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
