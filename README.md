# 🌾 Crop Prediction & Smart Food Recommendation System

A full-stack Machine Learning + FastAPI + React project that predicts the **best crop to grow** based on real-time **weather**, **soil properties**, and **geolocation**.  
It also recommends **a random dish** made from that crop and calculates its **total nutrition value** using an ingredient-level nutrition database.

---

## 🚀 Features

### 🔍 **1. Automatic Crop Prediction**
Prediction uses:
- City name (auto → lat/lon)
- Current temperature
- Humidity
- Rainfall
- Soil defaults (based on Indian states)
- ML model (RandomForest or similar)
- Scaler for preprocessing

---

### 🍛 **2. Random Dish Recommendation**
Using a custom dataset (`Ifood_new.csv`), the system:
- Finds dishes containing the predicted crop  
- Randomly picks a different dish on every prediction  
- Displays all ingredients

---

### 🥗 **3. Nutrition Calculator**
Uses 5 combined CSV nutrition datasets:
- FOOD-DATA-GROUP1.csv  
- FOOD-DATA-GROUP2.csv  
- FOOD-DATA-GROUP3.csv  
- FOOD-DATA-GROUP4.csv  
- FOOD-DATA-GROUP5.csv  

It sums nutrients for every ingredient in a dish.

---

### 🌦️ **4. Real-Time Weather API**
Uses Open-Meteo API:
- Temperature  
- Humidity  
- Rainfall  
- Fully free + no API key required  

---

### 🌍 **5. Frontend (React)**
Beautiful, simple UI that:
- Accepts city name  
- Fetches crop prediction  
- Shows dish & nutrition  
- Clean and error-safe  

---

## 🧠 Tech Stack

### **Frontend**
- React (Vite)
- JavaScript

### **Backend**
- FastAPI
- Uvicorn
- Requests
- Pandas
- NumPy
- Joblib
- Scikit-learn

### **Machine Learning**
- Pretrained model: `crop_model.pkl`
- Pretrained scaler: `scaler.pkl`
- Dataset: `Crop_recommendation.csv`

---

## 📂 Project Structure
projects/
│
├── crop_frontend/ # React frontend
│ ├── src/
│ ├── package.json
│ └── ...
│
├── project/ # FastAPI backend
│ ├── main.py
│ ├── crop_model.pkl
│ ├── scaler.pkl
│ ├── Ifood_new.csv
│ ├── FOOD-DATA-GROUP*.csv
│ ├── requirements.txt
│ └── ...
│
└── .gitignore



---

# 🛠️ How to Run the Project

## 1️⃣ Backend (FastAPI)

### Step 1: Create & activate virtual environment

Step 2: Install dependencies
pip install -r requirements.txt
Step 3: Run server
uvicorn main:app --reload

Backend runs at:

http://localhost:8000
2️⃣ Frontend (React)
cd crop_frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173

