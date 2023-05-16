%%
path = 'X:\Wei_e20799\CrSbS3_May_2023\MDA';
data = struct();
%%
run_no = 12;

data(1).(sprintf('X03MA_PC_%04d', run_no)) = load(sprintf('%s/X03MA_PC_%04d.mat', path, run_no), '-mat');
Y = data(1).(sprintf('X03MA_PC_%04d', run_no)).(sprintf('S1_P1_X03MA_PC_%04d', run_no));
Z = data(1).(sprintf('X03MA_PC_%04d', run_no)).(sprintf('S2_P1_X03MA_PC_%04d', run_no));
D1 = data(1).(sprintf('X03MA_PC_%04d', run_no)).(sprintf('D01_X03MA_PC_%04d', run_no));
D2 = data(1).(sprintf('X03MA_PC_%04d', run_no)).(sprintf('D02_X03MA_PC_%04d', run_no));
%%
figure;
p1 = surf(Z, Y, D1, 'EdgeColor', 'none');
colormap jet;
colorbar;
pbaspect([1 6 1])
view(2)

figure;
p2 = surf(Z, Y, D2, 'EdgeColor', 'none');
colormap jet;
colorbar;
pbaspect([1 6 1])
view(2)
