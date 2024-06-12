function [week,sec_of_week] = gps_time(julday)
%GPS_TIME  Conversion of Julian Day number to GPS week and
%  	     Seconds of Week reckoned from Saturday midnight

%Kai Borre 05-20-96
%Copyright (c) by Kai Borre
%$Revision: 1.0 $  $Date: 1997/09/23  $

a = floor(julday+.5);
b = a+1537;
c = floor((b-122.1)/365.25);
e = floor(365.25*c);
f = floor((b-e)/30.6001);
d = b-e-floor(30.6001*f)+rem(julday+.5,1);
day_of_week = rem(floor(julday+.5),7); %rem = remainder
week = floor((julday-2444244.5)/7);
% We add +1 as the GPS week starts at Saturday midnight
sec_of_week = (rem(d,1)+day_of_week+1)*86400;
% Added by CHON 25 Sept 2000
if (sec_of_week>=604800.0)
   sec_of_week = sec_of_week-604800.0;
end

%%%%%%% end gps_time.m	%%%%%%%%%%%%%
