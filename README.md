# Signal Viewer
![Main Picture](screenshots/home.png)


## Description

- Desktop Application Designed For Signal Analysis
- User-Friendly Interface For Easy Visualization And Comparison Of Different Signals
- Handles Multi-Channel Signal Viewing, Allowing Flexible Control Over Each Signal
- Offers Extra Features Like Viewing A Live Signal In Real Time, Gluing Two Signals Togther

## Tech Stack Used

|**Functionality** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)|
|--- | --- |
|**UI** | ![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)|
|**Styling** | [![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=fff)](#)|

## Features
### 1. Signal Browsing

- Browse & View A Signal File (Make Sure Its Format & Extension Are The Same As The Files Inside `signals` Directory)

### 2. Signal Manipulation
   
- Play, Pause & Rewind The Signal

![Playback GIF](screenshots/playback.gif)
&nbsp;
- Change The Color Of The Signal
  
![Change Color GIF](screenshots/color.gif)
&nbsp;
- Change The Name Of The Signal
   
![Change Name GIF](screenshots/name.gif)
&nbsp;
- Show & Hide The Signal

![Show & Hide GIF](screenshots/visibility.gif)
&nbsp;
- Control The Speed Of The Signal Plotting
   
![Adjust Speed GIF](screenshots/speed.gif)
&nbsp;
- Link The Two Graphs Together, Ensuring Synchronized Control
   
![Link GIF](screenshots/link.gif)
- Other Features Like Changing The Zoom & Pan Level, Moving The Signal Between The Two Graphs

### 3. Real Time Signal
- View A Real Time Signal Showcasing The Current Temperature In Cairo, Egypt Using `OpenWeather` API

![Live Signal GIF](screenshots/live.gif)
### 4. Signal Gluing

- Glue Two Signal Together With Different Interpolation Orders Of The Gap
  
![Gluing Signal GIF](screenshots/glue.gif)

- Export The Gluing Results As A PDF
![PDF Report Picture](screenshots/report.png)

## Installation

1. Make Sure That Pip & Python Are Installed On Your System

2. Clone The Repo Onto Your Local System or Download The Zip File & Extract It
   ```bash
    git clone https://github.com/mostafa-aboelmagd/signal-viewer.git
    ```

3. Nagivate To The Project's Directory 
   
4. Install The Required Libraries
    ```bash
    pip install -r requirements.txt
    ```

5. Run `main.py` File
    ```bash
    python main.py
    ```

## Contributors

| Name | GitHub | LinkedIn |
| ---- | ------ | -------- |
| Mostafa Ayman | [![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white)](https://github.com/mostafa-aboelmagd) | [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mostafa--aboelmagd/) |
| Ali Zayan | [![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white)](https://github.com/alizayan684) | [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/%D8%B9%D9%84%D9%8A-%D8%B2%D9%8A%D8%A7%D9%86-%F0%9F%94%BB%F0%9F%87%B5%F0%9F%87%B8-b98239264/) |
| Zeyad Amr | [![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white)](https://github.com/Zisco2002)| [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/zeyad-amr-3506b225b/) |
| Omar Khaled | [![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white)](#)| [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/omar-khaled-064b7930a/) |
