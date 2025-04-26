# MIXING TIME DETERMINATION - Using Colorimetric Method

**By Yago G. S. Silva¹, Fernando A. Cecatto² and Elisabeth F. P. Augusto³**  
*Federal University of São Paulo*  
*Contacts:*  
- yago.gregorio@unifesp.br¹  
- fernando.assis@unifesp.br²  
- elisabeth.augusto@unifesp.br³

---

## Description

This program was developed to determine the global mixing time of a reactor using a colorimetric method. It analyzes an experimental video and returns the mixing time.

We developed this program to characterize our bioreactor. We were looking for a global measurement method using a colorimetric approach. The program essentially converts the experiment video into frames and analyzes the color change in four areas of the video (explained in the “Select the Areas” section), chosen by the user. It finds the frame where the experiment starts, and from there, it analyzes the green component of the RGB color space in this first version and determines the mixing time.

---

## Features

- **Video Analysis**: Converts the video into frames and analyzes color changes.
- **Area Selection**: Allows the user to choose four areas of the video for analysis.
- **Mixing Time Determination**: Calculates the global mixing time based on the changes in the green component of the RGB color space.

---

## How to Use

1. **Steps**:
   - Import the experimental video into the program.
   - Select the four areas you want to analyze (detailed in the "Select the Areas" section).
   - The program will automatically detect the starting frame of the experiment and begin the analysis.
   - The mixing time will be calculated based on the analysis of the green color component changes.

---

## Select the Areas

The program allows the user to select four specific areas in the video for analysis. These areas will be monitored for changes in the intensity of the green component of the RGB color space during the experiment. The goal is to measure the time it takes for the mixture to reach a homogeneous state, based on the variation in green color.
