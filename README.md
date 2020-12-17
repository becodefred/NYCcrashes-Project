### 1. Background

Name of the Project: Data preprocessing - NYC Motor Vehicle Crashes  
Context of the study: BeCode, Liège Campus, AI/Data Operator Bootcamp, December 2020  
Objective: apply preprocessing techniques to a dataset (.csv file)   
Author: Frédéric Fourré  
Email: fourrefrederic593@gmail.com


### 2. Dataset

Source: New York City (NYC) OpenData (see https://data.cityofnewyork.us)  
Title: Motor Vehicle Collisions - Crashes  
Initial sample shape: 100000 rows, 29 columns  
Description: each row represents a crash event. A few column names: &quot;crash date&quot;, &quot;zip code&quot;, &quot;number of persons injured&quot;, &quot;contributing factor vehicle 1&quot;, &quot;vehicle type code 1&quot;. Full description available at https://data.cityofnewyork.us  

Data in our sample were collected between 23/03/2013 and 29/09/2020  

Name of the .csv file containing the original data: data_100000.csv  


### 3. Tools

GeoPy, NumPy, Pandas


### 4. To run the file

From terminal, type `python3`, then type `exec(open('crashesfred.py').read())`


### 5. Preprocessing steps

Initial shape of the DataFrame is (100000, 29)

5.1 Rename the columns to facilitate inspection of the DataFrame: &quot;date&quot;, &quot;time&quot;, &quot;borough&quot;, &quot;zipcode&quot;, &quot;latitude&quot;, &quot;longitude&quot;, &quot;location&quot;, &quot;onstreet&quot;, &quot;offstreet&quot;, &quot;crossstreet&quot;, &quot;totinjured&quot;, &quot;totkilled&quot;, &quot;pedinjured&quot;, &quot;pedkilled&quot;, &quot;cycinjured&quot;, &quot;cyckilled&quot;, &quot;motinjured&quot;, &quot;motkilled&quot;, &quot;factorveh1&quot;, &quot;factorveh2&quot;, &quot;factorveh3&quot;, &quot;factorveh4&quot;, &quot;factorveh5&quot;, &quot;id&quot;, &quot;typeveh1&quot;, &quot;typeveh2&quot;, &quot;typeveh3&quot;, &quot;typeveh4&quot;, &quot;typeveh5&quot;

5.2 Put crash events in chronological order, and add columns &quot;year&quot;, &quot;month&quot;, &quot;day&quot;, &quot;hour&quot; and &quot;minute&quot;

5.3 There were missing values (NA in Pandas) for &quot;latitude&quot;, &quot;longitude&quot; and &quot;location&quot;. We made geocoding tests to see if it was possible to retrieve latitude and longitude from &quot;borough&quot;, &quot;zipcode&quot;, &quot;onstreet&quot; and &quot;offstreet&quot;. The answer is no, in general, due to mechanical errors in writing which are unpredictable

Remove rows for which location of the crash is not available. Also remove rows with latitude and longitude equal to 0

5.4 Remove rows for which (factorveh1 = NA AND factorveh2 = NA AND etc. AND factorveh5 = NA) 

5.5 Replace NaN and &quot;Unspecified&quot; values in factorvehi (i = 1, 2, 3, 4, 5) by 0

5.6 Replace NaN values in &quot;borough&quot;, &quot;zipcode&quot;, &quot;onstreet&quot;, &quot;offstreet&quot; and &quot;crossstreet&quot; by 0

5.7 Processing typevehi (i = 1, 2, 3, 4, 5)

&nbsp;&nbsp;5.7.1 Find unique values in typevehi and convert these to lower case.

&nbsp;&nbsp;5.7.2 Find unique values containing string &quot;tow&quot; (examples: TOW, Tow truck), apply &quot;tow filter&quot; to typevehi (i = 1, 2, 3, 4, 5) and replace the name of any occurence with name &quot;Tow&quot;

&nbsp;&nbsp;5.7.3 Repeat the process described in 5.7.2 with the following filters: &quot;amb&quot; (Ambulance), &quot;trac&quot; (Tractor Truck), &quot;fir&quot; (Fire Truck), &quot;sco&quot; (Scooter), &quot;pic&quot; (Pickup), &quot;motor&quot; (Motorcycle), &quot;bik&quot; (Bike), &quot;dum&quot; (Dump Truck), &quot;tax&quot; (Taxi), &quot;box&quot; (Box Truck), &quot;van&quot; (Van), &quot;bus&quot; (Bus), &quot;trail&quot; (Trailer), &quot;seda&quot; (Sedan), &quot;fork&quot; (Forklift)

&nbsp;&nbsp;5.7.4 Apply miscellaneous filters to get the following unique values: Limousine, Truck, Mail Truck, Station Wagon/Sport Utility Vehicle, Garbage or Refuse

&nbsp;&nbsp;5.7.5 Remove garbage or insignificant values in typevehi (examples: OTHER, UNKNOWN, pc)

&nbsp;&nbsp;5.7.6 Replace NaN values in typevehi (i = 1, 2, 3, 4, 5) with 0

5.8 Look for duplicates

5.9 Create tuples from &quot;latitude and &quot;longitude&quot; and put them in a new column named &quot;location2&quot;

5.10 Reset index of DataFrame

5.11 Reverse geocoding: from coordinates in &quot;location2&quot; find values for borough, zipcode and street, and put the results in &quot;borough2&quot;, &quot;zipcode2&quot; and &quot;onstreet2&quot;. 

Used to check the data in the original dataset or replace missing values. 

Final shape of DataFrame is (90779, 39)

5.12 Save the final DataFrame in a .csv file: see datcrashesfred.csv


### 6. Improvements/To do

For 5.7: 

- use a For loop to sort vehicle types
- other sample datasets may contain other garbage or insignificant strings (mechanical mistakes in written language are unpredictable) and new vehicle types. The program should at least be able to detect such modifications
- check the meaning of some vehicle types (example: PK)

Compare the results obtained from reverse geocoding to the original data (borough, zipcode, onstreet)








