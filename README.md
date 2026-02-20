# Metro CDMX - Route Calculator  
A desktop application developed in Python to calculate routes and estimated travel times in the Mexico City Metro system.

> [!Warning]  
> This is an academic project completed in a few weeks, so its coverage is limited to a section of the Mexico City Metro system and does not include the entire network. It may also present performance limitations (especially on Windows) or issues related to window size, as we do not have extensive experience with Python or its libraries. For more details, see the [Notes](#Notes) section.

> [!Note]  
> You can view the project’s PPT file by clicking
> [here](https://www.canva.com/design/DAG6dDJUXF8/CQd0U0vlWWYd-ESSwZLuug/view?utm_content=DAG6dDJUXF8&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h306a0f4a96)

## Features  
- 🗺️ **Interactive visualization**: Mexico City Metro map with the calculated route highlighted  
- ⏱️ **Optimal route calculation**: Uses the A* algorithm to find the fastest path  
- ♿ **Accessibility filters**: Options for users who require escalators or elevators  
- 📊 **Detailed information**: Displays estimated time, number of stations, and transfers  

## Technologies used  
- Python 3  
- Tkinter (graphical interface)  
- NetworkX (graph modeling)  
- Pillow (image loading and resizing)  
- heapq (priority queue for A*)  

## Usage  
1. Select the origin station.  
2. Select the destination station.  
3. Optionally enable accessibility filters.  
4. Click "SEARCH ROUTE".  
5. The application will display:  
   - Approximate time.  
   - Number of stations.  
   - Number of transfers.  
   - Highlighted route on the map.  

## Notes  
- Distances and coordinates are approximate.  
- The model includes a subset of lines.  
- The calculated time is a theoretical estimation based on constant speed (10 m/s).  
- Accessibility services are considered only at the initial and final stations and during transfers.  
- Transfers imply a 5-minute penalty.  
- Each intermediate station implies a 30-second penalty.
