%Input GPS Navigation File and Plot satellite coordinates - ENHANCED VERSION
%TEY SUI ZER A18GH0130
%Modified from Kai Borre and DR.Tajul Arrifin
%Enhanced with dynamic satellite processing and flexible plotting

clear;clc;

%Input navigation file
inputnav = '../data/chur1610.19n';

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

%Process GPS satellites dynamically with 32 threshold
% Discover which satellites actually exist in the RINEX file
unique_sats = unique(Eph(1,:)); % Get unique satellite numbers from first row
unique_sats = unique_sats(unique_sats > 0); % Remove zeros
max_prn = 32; % Maximum GPS PRNs (threshold)
fprintf('Found %d satellites in RINEX file: %s\n', length(unique_sats), mat2str(unique_sats));
fprintf('Processing up to %d satellites (1-%d) with dynamic discovery\n', max_prn, max_prn);

%Compute satellite coordinate for all epoch, calculate 1 by 1
svposh = zeros(max_prn, 5); % Initialize svposh matrix for all 32 satellites
svposc = cell(rwt, 1); % Initialize cell array
for i = 1:rwt    
    timesat = mytime(i,2);  %define time
    for j = 1:max_prn  %loop through all 32 satellites (like original)
        sv = j; %use satellite number j (like original)
        col_Eph = find_eph(Eph,sv,timesat);
        k = col_Eph;
        if k > 0  % Only process if ephemeris data is available
            try
                satposition = satpos(timesat,Eph(:,k)); %input=time,eph eg:satillte 10=column 10
                X = satposition(1);
                Y = satposition(2);
                Z = satposition(3);
                svposh(j,:) = [timesat sv X Y Z]; %compute data for this satellite
            catch
                % Error in satpos calculation
                svposh(j,:) = [timesat sv NaN NaN NaN]; %compute data for this satellite
            end
        else
            % No ephemeris data available for this satellite at this time
            svposh(j,:) = [timesat sv NaN NaN NaN]; %compute data for this satellite
        end
    end
    svposc{i,1}=svposh; %combine epoch files, c is in cell format
end
svpos = cell2mat(svposc);%Satellite coordinate for all epoch, transform cell to matrix form

%Separate data by satellite dynamically (exactly like original)
svpos_data = cell(max_prn, 1);
legend_labels = cell(max_prn, 1);

% Create individual satellite variables like original (1-32)
for sv = 1:max_prn
    sat_data = svpos(svpos(:,2) == sv, :);
    if isempty(sat_data)
        svpos_data{sv} = NaN(rwt, 5); % fill with NaN if satellite absent
    else
        % pad with NaN if shorter
        len = size(sat_data, 1);
        if len < rwt
            pad = NaN(rwt-len, 5);
            sat_data = [sat_data; pad];
        end
        svpos_data{sv} = sat_data;
    end
    legend_labels{sv} = sprintf('svpos%02d', sv);
end

% Set graphics toolkit to gnuplot for headless mode
graphics_toolkit('gnuplot');
figure('visible', 'off')

%Plot all satellites dynamically
%For individual satellite plotting please see below
%to specify epoch use command below
rwt=1000; %100 x interval second 

% Prepare plot data for all 32 satellites (exactly like original)
plot_args = cell(1, max_prn*3);
for sv = 1:max_prn
    plot_args{(sv-1)*3+1} = svpos_data{sv}(1:rwt,3); % X
    plot_args{(sv-1)*3+2} = svpos_data{sv}(1:rwt,4); % Y
    plot_args{(sv-1)*3+3} = svpos_data{sv}(1:rwt,5); % Z
end

% Plot all 32 satellites in one plot3 call (exactly like original)
plot3(plot_args{:}, 'LineWidth', 2);
legend(legend_labels);
xlabel('X (m)');ylabel('Y (m)');zlabel('Z (m)'); %ecef wgs84 ellipsoid model

% Create results directory if it doesn't exist
if ~exist('../results', 'dir')
    mkdir('../results');
end

% Get input filename without extension
[~, name, ~] = fileparts(inputnav);

% Save the plot
png_filename = fullfile('../results', [name '.png']);
print(png_filename, '-dpng', '-r300');
fprintf('✓ Saved: %s\n', png_filename);

% Save CSV data
csv_filename = fullfile('../results', [name '.csv']);
csvwrite(csv_filename, svpos);
fprintf('RINEX Processing Complete!\n');
fprintf('Data saved to: %s\n', csv_filename);
fprintf('Total epochs processed: %d\n', rwt);
fprintf('Total satellite positions calculated: %d\n', size(svpos, 1));
fprintf('Number of satellites processed: %d\n', max_prn);
