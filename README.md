# 🎯 Motion Tracking with Optical Flow – Turn Any Video into an Object Tracking Playground!

**Ever wanted to track an object in a video like those futuristic surveillance systems?**  
This project makes it possible using **Lucas-Kanade Optical Flow**, a **powerful yet lightweight** tracking algorithm. Just **click on an object**, and the script will **automatically track its movement across frames**, drawing real-time motion trails.

---

## 🚀 What This Project Does
✔️ **User-Defined Object Tracking** → Click on any object in the first frame to begin tracking.  
✔️ **Smooth Motion Estimation** → Uses Optical Flow to accurately predict movement across frames.  
✔️ **Real-Time Visualization** → Motion paths are drawn dynamically as the object moves.  
✔️ **Multi-Point Tracking** → Select multiple keypoints for more robust tracking.  
✔️ **No Deep Learning Required** → Achieves real-time results without the need for large AI models.  

---

## 🔧 How It Works
1️⃣ **User Selects Points** → Click on the object in the first frame.  
2️⃣ **Feature Detection** → The script automatically identifies keypoints to track.  
3️⃣ **Motion Estimation** → Optical Flow predicts how those points move in subsequent frames.  
4️⃣ **Real-Time Tracking** → A motion path is drawn for each point.  

---

## 📦 Installation & Setup
This project is built with **Python & OpenCV**, making it easy to set up.  

### **1️⃣ Install Dependencies**
```bash
pip install opencv-python numpy
