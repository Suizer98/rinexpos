%Input GPS Navigation File and Plot satellite coordinates
%TEY SUI ZER A18GH0130
%Modified from Kai Borre and DR.Tajul Arrifin

clear;clc;

%Input navigation file
inputnav = 'chur1610.19n';

%Form and read NAV file for easier access
rinexe (inputnav,'Rinexnav.nav');
navfile = 'Rinexnav.nav';
Eph = get_eph(navfile);

%Parameters setting
%datein = [YY MM DD]
datein = [19 06 10];
intervalin = 15;%in second    %1 minute generate one data
[mytime] = gpsweekcal(datein,intervalin);
[rwt,colt] = size(mytime);  %calculate time size
starttime = mytime(1,2);  %can be deleted
endtime = mytime(rwt,2);

%Compute satellite coordinate for all epoch, calculate 1 by 1
for i = 1:rwt    
    timesat = mytime(i,2);  %define time
    for j = 1:32  %we got 32 satellites
        sv = j; %define no of run, finish epoch then continue to next satellites
        col_Eph = find_eph(Eph,sv,timesat);
        k = col_Eph;
        satposition = satpos(timesat,Eph(:,k)); %input=time,eph eg:satillte 10=column 10
        X = satposition(1);
        Y = satposition(2);
        Z = satposition(3);
        svposh(j,:) = [timesat sv X Y Z]; %compute 32 data
    end
    svposc{i,:}=svposh; %combine epoch files, c is in cell format
end
svpos = cell2mat(svposc);%Satellite coordinate for all epoch, transform cell to matrix form

%Separate data by satellite, define satellite data 1 by 1
svpos01 = svpos; %define 1st satellites from all data
svpos01(svpos01(:,2) ~= 1,:) = []; %throw data when svpos01 not = 1....

svpos02 = svpos;
svpos02(svpos02(:,2) ~= 2,:) = [];

svpos03 = svpos;
svpos03(svpos03(:,2) ~= 3,:) = [];

svpos04 = svpos;
svpos04(svpos04(:,2) ~= 4,:) = [];

svpos05 = svpos;
svpos05(svpos05(:,2) ~= 5,:) = [];

svpos06 = svpos;
svpos06(svpos06(:,2) ~= 6,:) = [];

svpos07 = svpos;
svpos07(svpos07(:,2) ~= 7,:) = [];

svpos08 = svpos;
svpos08(svpos08(:,2) ~= 8,:) = [];

svpos09 = svpos;
svpos09(svpos09(:,2) ~= 9,:) = [];

svpos10 = svpos;
svpos10(svpos10(:,2) ~= 10,:) = [];

svpos11 = svpos;
svpos11(svpos11(:,2) ~= 11,:) = [];

svpos12 = svpos;
svpos12(svpos12(:,2) ~= 12,:) = [];

svpos13 = svpos;
svpos13(svpos13(:,2) ~= 13,:) = [];

svpos14 = svpos;
svpos14(svpos14(:,2) ~= 14,:) = [];

svpos15 = svpos;
svpos15(svpos15(:,2) ~= 15,:) = [];

svpos16 = svpos;
svpos16(svpos16(:,2) ~= 16,:) = [];

svpos17 = svpos;
svpos17(svpos17(:,2) ~= 17,:) = [];

svpos18 = svpos;
svpos18(svpos18(:,2) ~= 18,:) = [];

svpos19 = svpos;
svpos19(svpos19(:,2) ~= 19,:) = [];

svpos20 = svpos;
svpos20(svpos20(:,2) ~= 20,:) = [];

svpos21 = svpos;
svpos21(svpos21(:,2) ~= 21,:) = [];

svpos22 = svpos;
svpos22(svpos22(:,2) ~= 22,:) = [];

svpos23 = svpos;
svpos23(svpos23(:,2) ~= 23,:) = [];

svpos24 = svpos;
svpos24(svpos24(:,2) ~= 24,:) = [];

svpos25 = svpos;
svpos25(svpos25(:,2) ~= 25,:) = [];

svpos26 = svpos;
svpos26(svpos26(:,2) ~= 26,:) = [];

svpos27 = svpos;
svpos27(svpos27(:,2) ~= 27,:) = [];

svpos28 = svpos;
svpos28(svpos28(:,2) ~= 28,:) = [];

svpos29 = svpos;
svpos29(svpos29(:,2) ~= 29,:) = [];

svpos30 = svpos;
svpos30(svpos30(:,2) ~= 30,:) = [];

svpos31 = svpos;
svpos31(svpos31(:,2) ~= 31,:) = [];

svpos32 = svpos;
svpos32(svpos32(:,2) ~= 32,:) = [];

figure
%Plot all satellite
%For individual satellite plotting please see below
%to specify epoch use command below
rwt=1000; %100 x interval second 
plot3(svpos01(1:rwt,3),svpos01(1:rwt,4),svpos01(1:rwt,5),...  %1:end of data
    svpos02(1:rwt,3),svpos02(1:rwt,4),svpos02(1:rwt,5),svpos03(1:rwt,3),svpos03(1:rwt,4),svpos03(1:rwt,5),...
    svpos04(1:rwt,3),svpos04(1:rwt,4),svpos04(1:rwt,5),svpos05(1:rwt,3),svpos05(1:rwt,4),svpos05(1:rwt,5),...
    svpos06(1:rwt,3),svpos06(1:rwt,4),svpos06(1:rwt,5),svpos07(1:rwt,3),svpos07(1:rwt,4),svpos07(1:rwt,5),...
    svpos08(1:rwt,3),svpos08(1:rwt,4),svpos08(1:rwt,5),svpos09(1:rwt,3),svpos09(1:rwt,4),svpos09(1:rwt,5),...
    svpos10(1:rwt,3),svpos10(1:rwt,4),svpos10(1:rwt,5),svpos11(1:rwt,3),svpos11(1:rwt,4),svpos11(1:rwt,5),...
    svpos12(1:rwt,3),svpos12(1:rwt,4),svpos12(1:rwt,5),svpos13(1:rwt,3),svpos13(1:rwt,4),svpos13(1:rwt,5),...
    svpos14(1:rwt,3),svpos14(1:rwt,4),svpos14(1:rwt,5),svpos15(1:rwt,3),svpos15(1:rwt,4),svpos15(1:rwt,5),...
    svpos16(1:rwt,3),svpos16(1:rwt,4),svpos16(1:rwt,5),svpos17(1:rwt,3),svpos17(1:rwt,4),svpos17(1:rwt,5),...
    svpos18(1:rwt,3),svpos18(1:rwt,4),svpos18(1:rwt,5),svpos19(1:rwt,3),svpos19(1:rwt,4),svpos19(1:rwt,5),...
    svpos20(1:rwt,3),svpos20(1:rwt,4),svpos20(1:rwt,5),svpos21(1:rwt,3),svpos21(1:rwt,4),svpos21(1:rwt,5),...
    svpos22(1:rwt,3),svpos22(1:rwt,4),svpos22(1:rwt,5),svpos23(1:rwt,3),svpos23(1:rwt,4),svpos23(1:rwt,5),...
    svpos24(1:rwt,3),svpos24(1:rwt,4),svpos24(1:rwt,5),svpos25(1:rwt,3),svpos25(1:rwt,4),svpos25(1:rwt,5),...
    svpos26(1:rwt,3),svpos26(1:rwt,4),svpos26(1:rwt,5),svpos27(1:rwt,3),svpos27(1:rwt,4),svpos27(1:rwt,5),...
    svpos28(1:rwt,3),svpos28(1:rwt,4),svpos28(1:rwt,5),svpos29(1:rwt,3),svpos29(1:rwt,4),svpos29(1:rwt,5),...
    svpos30(1:rwt,3),svpos30(1:rwt,4),svpos30(1:rwt,5),svpos31(1:rwt,3),svpos31(1:rwt,4),svpos31(1:rwt,5),...
    svpos32(1:rwt,3),svpos32(1:rwt,4),svpos32(1:rwt,5),'LineWidth',2);
legend({'svpos01','svpos02','svpos03','svpos04','svpos05','svpos06','svpos07','svpos08','svpos09','svpos10',...
    'svpos11','svpos12','svpos13','svpos14','svpos15','svpos16','svpos17','svpos18','svpos19','svpos20',...
    'svpos21','svpos22','svpos23','svpos24','svpos25','svpos26','svpos27','svpos28','svpos29',...
    'svpos30','svpos31','svpos32'});
xlabel('X (m)');ylabel('Y (m)');zlabel('Z (m)'); %ecef wgs84 ellipsoid model

%Sample for plotting individual satellite
%Remove % and change the XX to respective satellite number
%Remember to add % for the above plot
% XX=01;
% plot3(svpos(XX)(1:rwt,3),svpos(XX)(1:rwt,4),svpos(XX)(1:rwt,5));
% legend('svposXX');
% xlabel('X');ylabel('Y');zlabel('Z');

XX = 1;
figure
plot3(eval(sprintf('svpos%02d(1:rwt, 3)', XX)), eval(sprintf('svpos%02d(1:rwt, 4)', XX)), eval(sprintf('svpos%02d(1:rwt, 5)', XX)));
legend(sprintf('svpos%02d', XX));
xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');