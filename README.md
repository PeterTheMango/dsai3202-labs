# DSAI3202 - Lab 4, Part 1
### Objectives:
- Develop a Python program that simulates temperature readings from multiple sensors, calculates average temperatures, and displays the information in real-time in the console.  
### Tasks:
- Implement Sensor Simulation (***simulate_sensor*** function)
	- Write a function called simulate_sensor that simulates temperature readings from a sensor.
	- Use random.randint(15, 40) to generate random temperatures.
	- Make simulate_sensor update a global dictionary latest_temperatures with its readings every second. 
	- ![function](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxw8MRfhgr0eTvpDudEcyznl2hYmNa7iUSRXQIO)
- Implement Data Processing
	- Write a function called process_temperatures that continuously calculates the average temperature from readings placed in a queue. 
	- Make process_temperatures update a global dictionary temperature_averages with the calculated averages.
- Integrate Threading
	- Create threads for each call simulate_sensor and the process_temperatures function.  
	- Understand how to use daemon=True to manage thread lifecycle with the main program.  
	- ![ProcessThreadFunction](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwxONr6tcMrX6sYKmFaeqh0cNWP8pG9VdBvljk)
- Implement Display Logic
	- Write a function initialize_display to print the initial layout for displaying
	- ![initial_display](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwQHnYenTGcuHx4mkDJ2fAVlESOhzrtP9NqYwa)
	- Develop update_display to refresh the latest temperatures and averages in place on the console without erasing the console.
	- ![update_display](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxw8UGU66gr0eTvpDudEcyznl2hYmNa7iUSRXQI)
- Synchronize Data Access
	- Use  RLock  and  Condition  from the threading module to synchronize access to shared data structures and control the timing of updates. 
- Finish building the Main Program and organize your files.
	- Put the functions in a separate file.  
	- Create a file for the maim program.  
	- Initialize a queue and share data structures.  
	- Start the sensors and data processors threads.  
	- Initialize the console display and start the display update thread. Make the display updated every 5s.  
	- Ensure the main thread keeps running to allow the daemon threads to operate.  
### Questions:
- **Which synchronization metric did you use for each of the tasks?**  
	- `We should use RLock for the updating of temperatures and updating of display as this requires access to the data without it being edited to avoid race conditions. We should use Condition when updating the data to notify the process_temperature function that new data was added and should recalculate.`
- **Why did the professor not ask you to compute metrics?**
	- `Since have made the program with multithreading from the start and not improving a Sequential program, there is no need to compute for metrics in this exercise.`

### Assignment 1 Bonus 5%: 

 - [x] Make the latest temperature updated every  1s, and the average temperatures update every 5s, in place. 
> "It was not hard but it was annoying" 
> \- PeterTheMango, at 11PM on 25/02/25 
![update_avg](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwuwwveLpPIDC7ys8GiKakvzEXhWBcHNUZm91l)
![update_latest_temp](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxw9V8j40BMdDvhl5AEZpe0Wkox3KJ4YHOrIwG2)
### Task Reflections
> Why use Queues?
	`To help keep sharing of global data between threads safe and less likely to be corrupted.`
	
> What did we get from implementing it a certain way?
`Originally, I implemented it where the display is done all at the same time which is fine and probably helped with making it easy to update the display every X seconds. Seperating the updates into two different threads and functions helped me understand why RLocks and Conditions were efficient in the use cases mentioned above.`

> Why is synchronizations important in the code?
`It either leads to outdated data being used in the output which is caused by race conditions. It also ensures that we are not making edits to the data while one function is working on it.`

> What can we do to improve?
`Improving the output mechanics could be better because the cursor will flash positions when updating the average.`

### Acknowledgements

> Claude and Blackbox (AI) helped me with the output formatting errors I was getting where it overlapped each other and deleted other lines.

> ChatGPT 4o (AI) helped me in creating the docstrings for each of the functions.

> StackOverflow for introducing me on how to use the `sys` package in order to update the outputs without clearing as well as the start of the unicode characters to move the cursor.  
