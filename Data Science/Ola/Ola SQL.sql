create database Ola;
use Ola;
select * from booking;

#1. Retrieve all successful bookings:
create view Successful_Bookings as
select * from booking
where Booking_Status = "Success";

#1. Retrieve all successful bookings:
select * from Successful_Bookings;

#2. Find the average ride distance for each vehicle type:
create view ride_distance_for_each as
select Vehicle_Type, avg(Ride_Distance)
as avg_distance from booking
group by Vehicle_Type;

#2. Find the average ride distance for each vehicle type:
select * from ride_distance_for_each;

#3. Get the total number of cancelled rides by customers:
create view Canceled_ride as
select count(*) from booking 
where Booking_Status = 'Canceled by customer';

#3. Get the total number of cancelled rides by customers:
select * from Canceled_ride;


#4. List the top 5 customers who booked the highest number of rides:
create view Top_Customer as
select Customer_ID, count(Booking_ID) as total_rides 
from booking
group by Customer_ID
order by total_rides desc limit 5;

#4. List the top 5 customers who booked the highest number of rides:
select * from Top_Customer;


# 5. Get the number of rides cancelled by drivers due to personal and car-related issues:
create view Canceled_ride as
select count(*) from booking
where Canceled_Rides_by_Driver =  'Personal & Car related issue';

# 5. Get the number of rides cancelled by drivers due to personal and car-r
select * from Canceled_ride;


#6. Find the maximum and minimum driver ratings for Prime Sedan bookings:
create view Max_Min_ratings as
select max(Driver_Ratings) as Max_ratings,
min(Driver_Ratings) Min_ratings
from booking where Vehicle_Type = 'Prime Sedan';

#6. Find the maximum and minimum driver ratings for Prime Sedan bookings:
select * from Max_Min_ratings;


# 7. Retrieve all rides where payment was made using UPI:
create view Pay_UPI as
select * from booking
where payment_Method = 'UPI';

# 7. Retrieve all rides where payment was made using UPI:
select * from Pay_UPI;

#8. Find the average customer rating per vehicle type:
create view cust_rat as
select Vehicle_Type, avg(Customer_Rating) as avg_cus_rating
from booking
group by Vehicle_Type;

#8. Find the average customer rating per vehicle type:
select * from cust_rat;


#9. Calculate the total booking value of rides completed successfully:
create view Total_book as
select sum(Booking_Value) as total_success
from booking
where Booking_Status = 'Success';

#9. Calculate the total booking value of rides completed successfully:
select * from Total_book;


#10. List all incomplete rides along with the reason:-- 
create view incomplete as
select Booking_ID, Incomplete_Rides_Reason
from booking
where Incomplete_Rides = 'Yes';

#10. List all incomplete rides along with the reason:--
select * from Incomplete;