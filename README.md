# Full-Stack E-Commerce Application 🛍️

This is a complete full-stack web application that serves as a simple e-commerce storefront. It features a modern, decoupled architecture with a React frontend that consumes data from a custom-built Flask REST API.

***

## Features

-   **Dynamic Product Catalog:** Displays a grid of products fetched from the backend.
-   **Product Detail View:** Click on any product to see a detailed view with more information.
-   **Department Navigation:** Browse products by department using a collapsible sidebar.
-   **RESTful API:** A well-structured backend API provides all the data for products and departments.

***

## Tech Stack

-   **Frontend:** **React.js** (with Vite), **react-router-dom** for navigation, and custom CSS for styling.
-   **Backend:** **Flask** (Python)
-   **Database:** **SQLite 3**

***

## Architectural Overview

The application follows a modern decoupled architecture:

1.  **Frontend (React SPA):** A Single Page Application (SPA) built with React provides a fast and interactive user experience. It handles all the user interface logic and client-side routing.
2.  **Backend (Flask REST API):** A Python-based REST API built with Flask serves as the data layer. It connects to the database, processes requests from the frontend, and returns data in JSON format.
3.  **Database (SQLite):** A lightweight, file-based SQL database stores all product and department information.

***

## Setup and Run Instructions

To run this project locally, you'll need to run both the backend and frontend servers in separate terminals.

### 1. Backend API (Flask)

1.  **Navigate to the API directory:**
    ```bash
    cd milestone2
    ```
2.  **Activate the Conda environment:**
    ```bash
    conda activate ecommerce_env
    ```
3.  **Run the Flask server:**
    ```bash
    python app.py
    ```
    *The API will be running at `http://12.0.0.1:5000`.*

### 2. Frontend Application (React)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend # or vite-project
    ```
2.  **Install dependencies (if you haven't already):**
    ```bash
    npm install
    ```
3.  **Run the React development server:**
    ```bash
    npm run dev
    ```
    *The application will be available at `http://localhost:5173`.*

***

## API Endpoints

The backend provides the following REST API endpoints:

| Method | Endpoint                                 | Description                                 |
| :----- | :--------------------------------------- | :------------------------------------------ |
| `GET`  | `/api/products`                          | Get a paginated list of all products.       |
| `GET`  | `/api/products/{id}`                     | Get details for a single product by its ID. |
| `GET`  | `/api/departments`                       | Get a list of all departments and their product counts. |
| `GET`  | `/api/departments/{id}`                  | Get details for a single department by its ID. |
| `GET`  | `/api/departments/{id}/products`         | Get a list of all products in a specific department. |
