%Calculate GPS week and generate time for 24 hours
%LEE HONG SHENG 29/02/2020
%Modified from Kai Borre
function [my_time] = gpsweekcal(date,interval)
if date(1,1)<86     %<86=20** >86=19**
    year = date(1,1)+2000;
else
    year = date(1,1)+1900;
end
month = date(1,2);
day = date(1,3);
h = [0:interval:86399]'/3600;  %[begin time:interval:last second(86400=2nd day)]
jd = julday(year,month,day,h);  %JULIAN day* based on astronomical observation to compute a day
[week, sec_of_week] = gps_time(jd); %calculate gps rate
time = round(sec_of_week);  %this week how many th second
my_time = [week time];   