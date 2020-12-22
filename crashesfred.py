# Name of the Project: Data preprocessing - NYC Motor Vehicle Crashes
# Context of the study: BeCode, Liège Campus, AI/Data Operator Bootcamp, December 2020
# Objective: apply preprocessing techniques to a dataset (.csv file)
# Author: Frédéric Fourré
# Email: fourrefrederic593@gmail.com
# To run this file in a terminal: type python3, then exec(open('crashesfred.py').read())


import pandas as pd
import numpy as np
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


input_file = 'data_100000.csv'
dat = pd.read_csv(input_file, header = 0)

# initial shape of the DataFrame is (100000, 29)
dat.shape
# initial dtypes in the DataFrame
dat.dtypes
# put the original column names in a python list
original_headers = list(dat.columns.values)

# rename columns to facilitate inspection of the DataFrame
dat.columns = ['date', 'time', 'borough', 'zipcode', 'latitude', 'longitude', 'location', 'onstreet', 'offstreet', 'crossstreet', 'totinjured', 'totkilled', 'pedinjured', 'pedkilled', 'cycinjured', 'cyckilled', 'motinjured', 'motkilled', 'factorveh1', 'factorveh2', 'factorveh3', 'factorveh4', 'factorveh5', 'id', 'typeveh1', 'typeveh2', 'typeveh3', 'typeveh4', 'typeveh5']

headers = list(dat.columns.values)

# put crash events in chronological order
dat.date = pd.to_datetime(dat.date)
dat.time = pd.to_timedelta(dat.time+':00')
# concatenate
dat.date = pd.to_datetime(dat["date"] + dat["time"])
# sort
dat.sort_values(by = ["date"], inplace = True)

# split date and time, and add columns "year", "month", "day", "hour", "minute"
k = 2
dat.insert(k, "year", dat['date'].dt.year)
dat.insert(k + 1, "month", dat['date'].dt.month)
dat.insert(k + 2, "day", dat['date'].dt.day)
dat.insert(k + 3, "hour", pd.to_datetime(dat.time).dt.hour)
dat.insert(k + 4, "minute", pd.to_datetime(dat.time).dt.minute)

# detect missing values
dat.isnull().sum()

# remove rows for which location of the crash is not available
dat.dropna(axis = 0, how = 'any', subset = ['latitude', 'longitude', 'location'], inplace = True)

# remove rows with latitude AND longitude equal to 0
dat=dat[~((dat.latitude == 0) & (dat.longitude == 0))]
# shape is now (91796, 34)

# remove rows for which (factorveh1=NA AND factorveh2=NA AND etc. AND factorveh5=NA) 
cols1 = ['factorveh1', 'factorveh2', 'factorveh3', 'factorveh4', 'factorveh5']
dat.dropna(axis = 0, how = 'all', subset = cols1, inplace = True)
# shape is now (91442, 34)

# replace NaN and "Unspecified" values in factorvehi (i = 1, 2, 3, 4, 5) by 0
dat[cols1] = dat[cols1].fillna(0)
dat[cols1] = dat[cols1].replace('Unspecified', 0)

# replace NaN in 'borough', 'zipcode', 'onstreet', 'offstreet' and 'crossstreet' by 0
cols2 = ['borough', 'zipcode', 'onstreet', 'offstreet', 'crossstreet']
dat[cols2] = dat[cols2].fillna(0)

# processing typevehi (i = 1, 2, 3, 4, 5)
# find unique values in typevehi and convert these to lower case
cols3 = ["typeveh1", "typeveh2", "typeveh3", "typeveh4", "typeveh5"]
xval = dat[cols3].values.ravel()
x = pd.unique(xval)
y = list(pd.Series(x).str.lower())

# find any unique value containing string "tow" and display the results
sub = 'tow'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]

# check if filter RegEx works for filt object
pd.Series(filt).str.replace('^([tT][oO][wW]).+', 'Tow', regex = True)
# apply the filter to typevehi (i = 1, 2, 3, 4, 5)
dat[cols3] = dat[cols3].replace('^([tT][oO][wW]).+', 'Tow', regex = True)

# check "tow" cleaning for column "typeveh1"
dat["typeveh1"].value_counts()

# filter for Ambulance
xval = dat[cols3].values.ravel()
x = pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'amb'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([aA][mM][bB]).*', 'Ambulance', regex=True)

# filter for Tractor Truck
xval = dat[cols3].values.ravel()
x = pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'trac'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([tT][rR][aA][cC]).*', 'Tractor Truck', regex=True)

# filter for Fire Truck
xval = dat[cols3].values.ravel()
x = pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'fir'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([fF][iI][rR]).*', 'Fire Truck', regex=True)


# filter for Scooter
xval = dat[cols3].values.ravel()
x = pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'sco'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([sS][cC][oO]).*', 'Scooter', regex=True)

# filter for Pickup
xval = dat[cols3].values.ravel()
x = pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'pic'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([pP][iI][cC]).*', 'Pickup', regex=True)

# filter for Motorcycle
xval = dat[cols3].values.ravel()
x = pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'motor'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]

dat[cols3] = dat[cols3].replace('MOTORCYCLE', 'Motorcycle', regex = True)
dat[cols3] = dat[cols3].replace('motorcycle', 'Motorcycle', regex = True)
dat[cols3] = dat[cols3].replace('Motorbike', 'Motorcycle', regex = True)
dat[cols3] = dat[cols3].replace('MOPED', 'Motorcycle', regex = True)
dat[cols3] = dat[cols3].replace('moped', 'Motorcycle', regex = True)
dat[cols3] = dat[cols3].replace('Moped', 'Motorcycle', regex = True)

# filter for Bike
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'bik'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([bB][iI][kK]).*', 'Bike', regex = True)

# filter for Dump Truck
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'dum'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([dD][uU][mM]).*', 'Dump Truck', regex = True)

# filter for Taxi
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'tax'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('TAXI', 'Taxi', regex = True)

# filter for Box Truck
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'box'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([bB][oO][xX]).*', 'Box Truck', regex = True)

# filter for Van
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'van'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([vV][aA][nN]).*', 'Van', regex = True)

# filter for Bus
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'bus'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([bB][uU][sS]).*', 'Bus', regex = True)

# filter for Trailer
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'trail'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([tT][rR][aA][iI][lL]).*', 'Trailer', regex = True)

# filter for Sedan
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'seda'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([sS][eE][dD][aA]).*', 'Sedan', regex = True)


# filters for miscellaneous
dat[cols3] = dat[cols3].replace('SPORT UTILITY / STATION WAGON', 'Station Wagon/Sport Utility Vehicle', regex = True)
dat[cols3] = dat[cols3].replace('GARBAGE TR', 'Garbage or Refuse', regex = True)

xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'limo'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]

dat[cols3] = dat[cols3].replace('LIMOU', 'Limousine', regex = True)
dat[cols3] = dat[cols3].replace('LIMO', 'Limousine', regex = True)
dat[cols3] = dat[cols3].replace('limo', 'Limousine', regex = True)

dat[cols3] = dat[cols3].replace('MAIL TRUCK', 'Mail Truck', regex = True)
dat[cols3] = dat[cols3].replace('mailtruck', 'Mail Truck', regex = True)
dat[cols3] = dat[cols3].replace('MAILTRUCK', 'Mail Truck', regex = True)

dat[cols3] = dat[cols3].replace('TRUCK', 'Truck', regex = True)
dat[cols3] = dat[cols3].replace('truck', 'Truck', regex = True)

# filter for Forklift
xval = dat[cols3].values.ravel()
x =  pd.unique(xval)
y = list(pd.Series(x).str.lower())
sub = 'fork'
z = np.core.defchararray.find(y, sub, start = 0, end = None)
filt = x[z >= 0]
dat[cols3] = dat[cols3].replace('.*([fF][oO][rR][kK]).*', 'Forklift', regex = True)


# remove garbage or insignificant values in typevehi
# identify all vehicle types, sum values and sort types
tab = dat[cols3].apply(pd.Series.value_counts)
indextab = list(tab.index)
filt3count = tab.sum(axis = 1)
filt3 = filt3count.sort_values(axis = 0, ascending = False)
indexfilt3 = list(filt3.index)

# keep 34 vehicle types 
keep = ['Sedan', 'Station Wagon/Sport Utility Vehicle', 'Taxi', 'Pickup', 'Box Truck', 'Bike', 'Bus', 'Motorcycle', 'Tractor Truck', 'Van', 'Ambulance', 'Scooter', 'Convertible', 'Dump Truck', 'PK', 'Garbage or Refuse', 'Flat Bed', 'Carry All', 'Tow', 'Chassis Cab', 'Fire Truck', 'Tanker', 'Concrete Mixer', 'Flat Rack', 'Lift Boom', 'Armored Truck', 'Trailer', 'Beverage Truck', 'Limousine', 'Multi-Wheeled Vehicle', 'Truck', 'Stake or Rack', 'Forklift', 'Mail Truck']
# remove 328 vehicle types 
rem = ['3-Door', 'PASSENGER VEHICLE', 'Open Body', 'UNKNOWN', 'UNK', 'FDNY', 'USPS', 'DELV', 'Bulk Agriculture', 'Pedicab', 'UNKNO', 'FDNY Truck', 'REFG', 'UTIL', 'Minicycle', 'DELIV', 'Unknown', 'Lunch Wagon', 'COMMERCIAL', 'unkno', 'SCHOO', 'POWER SHOV', 'POSTAL TRU', 'COM', 'MTA B', 'unknown', 'PAS', 'USPS Truck', 'ELECT', 'Pallet', 'usps', 'unk', 'STREE', 'GOLF CART', 'US PO', 'PSD', 'POSTA', 'FLATBED', 'TRK', 'MACK', 'DELIVERY T', 'Motorized Home', 'ICE CREAM', 'BACKH', 'commercial', 'Well Driller', 'COMME', 'wagon', 'FLAT', 'TRL', 'ELECTRIC S', 'Elect', 'Enclosed Body - Nonremovable Enclosure', 'Schoo', 'SUV', 'elect', 'FDNY EMS', 'RV', 'ROAD SWEEP', 'fdny', 'government', 'GARBA', 'hrse', 'Hopper', 'FOOD', 'postal tru', 'BOBCA', 'PC', 'LIGHT TRAI', 'sanitation', 'OTHER', 'Glass Rack', 'MOVIN', 'BULLD', 'Unkno', 'SANITATION', 'back', 'WORK', 'Delv', 'Delivery t', 'UHAUL', 'DELIVERY V', 'bobca', 'UT', 'USPS POSTA', 'DELIVERY', 'FREIGHTLIN', 'ASPHA', 'ACCESS A R', 'Flatbed', 'Flat bed', 'ALUMI', 'AMAZON SPR', 'BOB CAT', 'APPOR', 'BACK HOE', 'FRIEGHTLIN', 'Commercial', 'FREIGHT FL', 'DETAC', 'Flat', 'BLACK', 'FUSION', 'FREIGHT TR', 'BACKHOE LO', 'Fleet', 'Cement Tru', 'Const', 'Horse', 'HORSE', 'HI TA', 'HEARSE', 'HAUL FOR H', 'HAND', 'Golf Cart', 'Golf', 'Go kart', 'Courier', '18 WEELER', 'Ford sprin', '18 WHEELER', 'GLP050VXEV', '35 FT', 'GLNEN', '4D', '4DS', 'GATOR', 'Front-Load', 'Freight', '4dsd', 'DIRTB', 'E450', 'FREIG DELV', 'ENGIN', 'F550', 'E-SKA', 'CAT32', 'CHEVROLET', 'Enclosed Body - Removable Enclosure', 'COURIER', 'Electric s', 'CHEVY EXPR', 'CHURC', 'E-SKATEBOA', 'ENCLO', 'FD Truck', 'EMS Truck', 'EMS', 'E-UNICYCLE', 'CITY', 'E350', 'ELECTRIC M', 'CONT', 'COMMERICAL', 'CONCRETE M', 'ELEC. UNIC', 'FD LADDER', 'E REVEL SC', 'FREIG', 'FLAT BED', 'INTERNATIO', 'BOBCAT FOR', 'FOOD Truck', 'BS', 'BTM', 'DRILL RIG', 'FLATBED TR', 'Deliv', 'FLATBED FR', 'Bucket Tru', 'Can', 'CRANE', 'Depar', 'Crane', 'CAMPE', 'FED E', 'CAT', 'FDNY LADDE', 'FDNY Engin', 'FDNY ENGIN', 'FDNY #226', 'CAT.', 'DOT EQUIPM', 'yello', 'INTL', 'IP', 'Wagon', 'Wh Ford co', 'almbulance', 'backhoe', 'boom', 'boom lift', 'com', 'comm.', 'const', 'constructi', 'crane', 'cross', 'dark color', 'deliv', 'dilevery t', 'WINEB', 'WHITE', 'VEHICLE 2', 'USPOS', 'UHAUL Trai', 'UKN', 'UNATTACHED', 'UNKN', 'UNKNOWN VE', 'UPS Truck', 'USPS/GOVT', 'Utility.', 'UTILI', 'UTILITY', 'UTILITY TR', 'UTILITY VE', 'Unk', 'Utili', 'dp', 'e skate bo', 'e-350', 'trlr', 'stree', 'street cle', 'suburban', 'tk', 'transport', 'trl', 'uhaul', 'spec-', 'uhaul truc', 'uknown', 'util', 'utili', 'utility', 'vespa', 'sprin', 'self', 'electric s', 'itas', 'excav', 'f-250', 'fdny ems', 'forlift', 'g spc', 'golf cart', 'message si', 'rep', 'mopd', 'motor', 'p/sh', 'pc', 'prks', 'range', 'U-HAUL', 'Truck TRAI', 'Truck FLAT', 'winne', 'MOBIL', 'MOBILE', 'MOTOR', 'MOTOR SKAT', 'MTA Truck', 'MTA b', 'Mta', 'MECHANICAL', 'NYC ACS Va', 'NYC FD', 'NYS A', 'OTH', 'P/SH', 'PALFINGER', 'MINI', 'MAIL', 'POLIC', 'LADDER TRU', 'JETSKI', 'JLG L', 'JOHN', 'JOHN DEERE', 'John Deere', 'LADDER 34', 'LCOM', 'Livestock Rack', 'LCOMM', 'LEFT THE S', 'LMA', 'Lawnmower', 'Lift', 'Light trai', 'PASS', 'POST', 'Tree cutte', 'TRA/R', 'Snow Plow', 'Sprin', 'Subn', 'Sweeper', 'TL', 'TOYOT', 'TRANS', 'Sanitation', 'TRLR', 'TUCK', 'Tilt tande', 'Toyota', 'Train', 'Trc', 'Skateboard', 'SWT', 'POWER', 'SELF', 'PU', 'Parce', 'Postal tru', 'Pumper', 'RAM', 'RDS', 'SKATEBOARD', 'SWEEPER', 'SKID LOADE', 'SLINGSHOT', 'SMALL COM VEH(4 TIRES) ', 'SMART CAR', 'SPECIAL PU', 'STREET SWE', '0']


dat = dat[~dat[cols3].isin(rem).any(axis = 1, skipna = False)]
# shape is now (90779, 34)

# replace NaN values in typevehi with 0
dat[cols3] = dat[cols3].fillna(0)
dat.isnull().sum()

# check for duplicates 
dat.duplicated().any()

# create tuples from "latitude and "longitude" and put them in new column "location2"
dat['location2'] = dat[['latitude', 'longitude']].apply(tuple, axis = 1)
#shape is now (90779, 35)

# reverse geocoding
geolocator = Nominatim(user_agent = "fourrefrederic593@gmail.com")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds = 1)

# reset index (a new column "index" is created which contains the old indexes)
dat = dat.reset_index()
# shape is now (90779, 36)

# for loop: index will be [a, a+1, etc., b-1]
a = 0
b = 1000
datloop = dat.iloc[a:b, :]

i = 0
# for row in dat[["location2"]].head(n = 10).itertuples():
for row in datloop.itertuples():
    infoloc = reverse(row.location2)      
    if "road" in infoloc.raw["address"]:
        dat.loc[row.Index, 'onstreet2'] = infoloc.raw["address"]["road"]
    if "suburb" in infoloc.raw["address"]:  
        dat.loc[row.Index, 'borough2'] = infoloc.raw["address"]["suburb"]
    if "postcode" in infoloc.raw["address"]:   
        dat.loc[row.Index, 'zipcode2'] = infoloc.raw["address"]["postcode"]          
    i += 1
    print(i)


# save DataFrame to a .csv file
dat.to_csv("datcrashesfred.csv")















