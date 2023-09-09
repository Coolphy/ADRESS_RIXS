function [en, tey, tfy] = plot_xas(filePath, baseAtom, runNo)

    [en, tey, tfy] = load_xas(filePath, baseAtom, runNo);
    figure();
    plot(en, tey);
    hold on;
    plot(en, tfy);
    legend('TEY', 'TFY')

end

function fileName = make_name(baseAtom, runNo)

    fileName = sprintf("%s_%04d", baseAtom, runNo);

end

function [en, tey, tfy] = load_xas(filePath, baseAtom, runNo)

    fileName = make_name(baseAtom, runNo);
    data = readtable(sprintf("%s/%s.xas", filePath, fileName), 'FileType', 'text', 'NumHeaderLines', 35);
    en = data{:, 1};
    tey = data{:, 2};
    tfy = data{:, 3};

end
