# 💻 Laptop Price Predictor

A machine learning web application that predicts laptop prices in **Sri Lankan Rupees (LKR)** based on hardware specifications. Built with **Streamlit** and a trained **scikit-learn** model.

---

## 🌐 Live Demo

> 🔗 [laptop-price-predictor.streamlit.app](https://laptop-price-predictor-07.streamlit.app/)

---

## 📁 Project Structure

```
Laptop_price_predictor/
│
├── model/                        # Standalone model folder (reference)
│   └── predictor.pickle
│
└── website/                      # Main application
    ├── env/                      # Virtual environment (not pushed to GitHub)
    ├── model/
    │   └── predictor.pickle      # Trained ML model
    ├── .gitignore
    ├── requirements.txt
    └── streamlit_app.py          # Main Streamlit application
```

---

## ✨ Features

- 🔮 **Instant price prediction** using a trained machine learning model
- 🎛️ **Sidebar layout** — all inputs in one place, result displayed cleanly
- 📊 **Live spec summary cards** — update in real time as you configure
- 🏷️ **Feature badges** — highlights selected OS, display type, and touch support
- 📜 **Auto-scroll to result** — page scrolls to predicted price automatically
- 🔒 **Sidebar always visible** — locked open, never collapses

---

## ⚙️ Laptop Specifications Supported

| Category | Options |
|---|---|
| **RAM** | 4 GB, 8 GB, 16 GB, 32 GB, 64 GB |
| **Brand** | Acer, Apple, Asus, Dell, HP, Lenovo, MSI, Toshiba, Other |
| **Type** | Notebook, Ultrabook, Gaming, 2-in-1 Convertible, Netbook, Workstation |
| **Operating System** | Windows, macOS, Linux, Other |
| **CPU** | Intel Core i3 / i5 / i7, AMD, Other |
| **GPU** | Intel, AMD, Nvidia |
| **Display** | IPS, Touch Screen |
| **Weight** | 0.5 kg – 5.0 kg |

---

## 🧠 How It Works

1. User selects laptop specifications via the sidebar
2. Inputs are **one-hot encoded** to match the training feature set
3. Encoded features are fed into the trained **pickle model**
4. Predicted value is multiplied by **221** to convert to LKR
5. Result is displayed in a styled card with auto-scroll

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit + Custom CSS |
| **Backend / ML** | scikit-learn, NumPy |
| **Model format** | Python Pickle (.pickle) |
| **Language** | Python 3 |
| **Deployment** | Streamlit Community Cloud |

---

## 📊 Model Details

- **Training data:** Laptop price dataset with brand, specs, and display features
- **Target variable:** Laptop price (normalized, then multiplied by 221 for LKR conversion)
- **Preprocessing:** One-hot encoding for all categorical variables
- **Model type:** Regression model (trained in Jupyter Notebook, exported as pickle)

---

<div align="center">
  <sub>Built using Streamlit &nbsp;|&nbsp; Deployed on Streamlit Community Cloud</sub>
</div>
