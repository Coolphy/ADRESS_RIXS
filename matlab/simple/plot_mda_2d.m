function [X,Y,d1,d2] = plot_mda_2d(filePath,runNo)

fileName = make_name(runNo);
[x,y,d1,d2] = load_data(filePath,fileName);
[X,Y] = meshgrid(x,y);
figure(1);
s1 = surf(X,Y,d1,'EdgeColor','none');
colorbar;
% figure(2);
% s2 = surf(X,Y,d2,'EdgeColor','none');
% colorbar;

end

function fileName = make_name(runNo)

fileName = sprintf("X03MA_PC_%04d",runNo);

end

function [x,y,d1,d2] = load_data(filePath,fileName)

data_struct = load(sprintf("%s/%s.mat",filePath,fileName));
x = data_struct(1).(sprintf("S2_P1_%s",fileName));
y = data_struct(1).(sprintf("S1_P1_%s",fileName));
d1 = data_struct(1).(sprintf("D01_%s",fileName));
d2 = data_struct(1).(sprintf("D02_%s",fileName));

end