function icol = find_eph(Eph,sv,time)
%FIND_EPH  Finds the proper column in ephemeris array

%Kai Borre and C.C. Goad 11-26-96
%Copyright (c) by Kai Borre
%$Revision: 1.0 $  $Date: 1997/09/23  $

icol = 0;
%sv
%find column to define eph
isat = find(Eph(1,:) == sv);
n = size(isat,2);
if n == 0, return, end;
icol = isat(1);
dtmin = Eph(21,icol);
for t = 1:n
   itest = isat(t);
   dtest = Eph(21,itest);
   if dtest < dtmin
      icol = itest;
      dtmin = dtest;
   end
end

dtmin = Eph(21,icol)-time;
for t = 1:n
%   dt = Eph(21,t)-time;
% Modified by Chon 25/12/2000 Otherwise this function will pick the wrong ephemeris for some sats
dt = Eph(21,isat(t))-time;
   if dt < 0
      if abs(dt) < abs(dtmin)
%         icol = t;
% Modified by Chon 25/12/2000
         icol = isat(t);
         dtmin = dt;
      end
   end
end
%%%%%%%%%%%%  find_eph.m  %%%%%%%%%%%%%%%%%
