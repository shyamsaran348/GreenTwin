# 🌱 GreenTwin
**An Intelligent Plant Care Assistant Powered by Digital Twins**

## 1. Problem Statement
Plant care is often inconsistent, reactive, and knowledge-heavy. Users managing home gardens, institutional green spaces, or small farms struggle with:
*   Remembering correct care schedules
*   Understanding plant-specific needs
*   Identifying diseases early
*   Tracking plant health progression over time

Most existing solutions offer static care tips or isolated features such as reminders or image lookup, but fail to provide a continuous, intelligent understanding of plant health. This leads to late disease detection, improper care decisions, plant loss, and inefficient resource use.

**There is a need for a unified plant care assistant that combines guidance, monitoring, and intelligence into a single, reliable system.**

## 2. Solution Overview
GreenTwin is a full-stack, production-ready plant care web application that assists users throughout the complete lifecycle of plant management. Each plant is represented as a **digital twin** — a continuously updated digital representation that reflects the plant’s health, growth, stress, and disease risk.

GreenTwin enables users to:
*   Create and manage detailed plant profiles
*   Receive timely care reminders
*   Monitor plant health through visual indicators
*   Detect diseases early using image-based ML
*   Track growth history through timelines and galleries

The system is designed for real usage, not demonstration, with persistent data, real inference, and real user workflows.

## 3. Core Innovation
GreenTwin introduces three key innovations:

1.  **Digital Twins for Plants**: Each plant maintains a live internal state that evolves over time instead of static records.
    *   **Novelty**: Implements a **Synergistic Stress Model** where Disease and Drought multiply each other's impact (Non-linear decay).
    *   **Biological Realism**: Includes a **Recovery Lag** system—plants heal slowly over time rather than instantly resetting.
2.  **Integrated Disease Intelligence**: Machine learning analyzes leaf images to assess disease risk and feed results directly into plant health simulation.
3.  **Unified Assistant Experience**: Care tips, reminders, disease alerts, and progress tracking are delivered through a single coherent interface rather than separate tools.
4.  **Active Adaptation (Auto-Pilot)**: The system doesn't just monitor; it **acts**. It automatically skips watering schedules during rain and triggers emergency alerts during heatwaves.

## 4. Application Architecture

### 4.1 Digital Twin Engine
Each plant twin maintains:
*   **Health Score (0–100)**
*   **Growth Stage**
*   **Water Stress Level**
*   **Heat / Light Stress**
*   **Disease Risk Index**

These values are updated based on user care actions, disease prediction results, and historical trends. This allows the system to generate predictive alerts, not just reactive warnings.

### 4.2 Intelligent Care Advisor (The Brain) 🧠
Beyond simple schedules, GreenTwin uses a **Species-Specific Knowledge Base** combined with real-time **Hyper-Local Weather Telemetry**.
*   **Context-Aware Advice**: "Mist your Ferns" (Low Humidity) vs "Water your Cactus" (Heatwave).
*   **Auto-Pilot Scheduler**:
    *   *Rain Detected*: **Auto-Skips** watering tasks.
    *   *Heat > 35°C*: Creates **URGENT** priority tasks.

### 4.3 Machine Learning Architecture
GreenTwin uses a plant-specific disease intelligence framework, reflecting real biological differences between plants.

**ML Flow:**
1.  User uploads a leaf image.
2.  Selects plant type.
3.  Backend routes request to the correct plant model.
4.  CNN predicts disease class and confidence.
5.  Output updates digital twin state.
6.  Alerts and recommendations are generated.

The platform supports multiple plant models, each independently trained (currently optimized for Tomato plants).

## 5. Dataset Details
*   **Dataset Used**: PlantVillage Dataset (Public agricultural research dataset).
*   **Supported Species (14 Types)**:
    *   **Apple**: Scab, Black Rot, Cedar Rust, Healthy
    *   **Blueberry**: Healthy
    *   **Cherry**: Powdery Mildew, Healthy
    *   **Corn**: Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy
    *   **Grape**: Black Rot, Esca (Black Measles), Leaf Blight, Healthy
    *   **Orange**: Huanglongbing (Citrus Greening)
    *   **Peach**: Bacterial Spot, Healthy
    *   **Pepper, Bell**: Bacterial Spot, Healthy
    *   **Potato**: Early Blight, Late Blight, Healthy
    *   **Raspberry**: Healthy
    *   **Soybean**: Healthy
    *   **Squash**: Powdery Mildew
    *   **Strawberry**: Leaf Scorch, Healthy
    *   **Tomato**: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Mosaic Virus, Yellow Leaf Curl Virus, Healthy

This comprehensive dataset ensures reliable training and stable real-world behavior across a wide variety of garden plants.

## 6. Technology Stack
### Frontend
*   **Responsive Web Application**: React / HTML / CSS / JavaScript
*   **Accessible UI Design**: High-contrast Dark Mode
*   **Charts**: Real-time growth and health tracking (Recharts)

### Backend
*   **Python**: FastAPI
*   **REST APIs**: Authentication & authorization
*   **Reminder Scheduler**: APScheduler
*   **Digital Twin Engine**: Custom Logic
*   **ML Inference Service**: PyTorch

### Machine Learning
*   **Python**: PyTorch / MobileNetV2 (Transfer Learning)
*   **Confidence-based predictions**

### Database & Storage
*   **Relational Database**: SQLite (Dev) / PostgreSQL (Prod)
*   **Persistent plant and user data**

## 7. User-Facing Features
*   ✅ Plant profile creation and management
*   ✅ Smart care scheduling and reminders
*   ✅ Health score and stress indicators
*   ✅ Growth timeline charts (Real-Time)
*   ✅ Leaf image upload and disease results
*   ✅ Garden gallery with history
*   ✅ Alert banners and informational overlays
*   ✅ **Intelligent Care Advisor** (Species + Weather specific tips)
*   ✅ **Real-Time Environment** (Temp, Humidity, Wind Speed)
*   ✅ **Auto-Pilot Mode** (Rain Skips & Heat Emergency Alerts)
*   ✅ Accessibility-friendly interface

## 8. SDG Alignment
*   **SDG 2 – Zero Hunger**: Reduces crop loss through early intervention; Improves plant health reliability.
*   **Good Health & Well-Being**: Healthier plants contribute to safer food systems; Reduced chemical misuse through early alerts.

## 9. Final Positioning Statement
GreenTwin is a complete, intelligent plant care assistant that uses digital twins and machine learning to guide users through plant management, health monitoring, and disease prevention. It is built as a real-world application with scalable intelligence, not a limited demonstration.

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
