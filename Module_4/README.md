# AI-Driven Precision Irrigation and Pest Mitigation System  
### Using Q-Learning Reinforcement Learning Algorithm

---

## 📌 Project Overview

This project implements an **AI-driven precision agriculture system** that optimizes irrigation and pesticide scheduling under real-world constraints.  
Reinforcement Learning (specifically **Q-Learning**) is used to determine the most efficient action for each crop plot based on soil, pest, and environmental conditions.

The simulation models a **200-acre agricultural zone in Odisha**, divided into 50 heterogeneous plots with varying soil capacity, crop maturity, and pest vulnerability.  
Environmental constraints include:

- **30% reduction** in weekly water quota  
- **Heatwave forecast (72 hours)**  
- **Limited service capacity:** 2 drones + 1 AGV  
- **20-minute battery per trip**  
- **Sudden pest outbreak in two high-risk plots**

---

## 🚀 Features

- Reinforcement Learning environment designed for precision agriculture  
- Q-Learning agent that learns optimal irrigation & pest control policies  
- Baseline rule-based system for comparison  
- Simulation of soil moisture, evapotranspiration, pest growth, and weather  
- Visual performance comparison using Matplotlib  
- Fully modular and customizable Python code  
- LaTeX project report included  

---

## 🧠 Reinforcement Learning Design

### **State Representation**
Each plot is described by:
- Soil moisture (5 bins)  
- Pest index (5 bins)  
- Time of day (4 bins)  
- Water quota ratio (5 bins)  

### **Actions**
| Action | Meaning |
|--------|---------|
| 0 | No action |
| 1 | Low irrigation |
| 2 | Medium irrigation |
| 3 | High irrigation |
| 4 | Pesticide spray |

### **Reward Function**
Encourages:
- Maintaining optimal moisture  
- Reducing pest index  
- Conserving water  
- Avoiding water depletion penalties  

---

## 📁 Project Structure

