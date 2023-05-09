function simple_gui

global info_dict;
info_dict = struct([]);

f = figure('Position',[0 0 1024 768],'DeleteFcn',@f_Callback);

col_names = {' Energy (eV) ',' Polarization ',' Temperature (K) ',' X (mm) ',' Y (mm) ',' Z (mm) ',' Theta (deg.) ',' Phi (deg.) ',' Tilt (deg.) ',' Acquire (s) ',' Split (s) ',' Slit (um) ',' Beam Current (mA) '};

t = uitable (f,'Position', [13 54 998 704],'Units','normalized',"ColumnName", col_names);

uicontrol(f,'Style','text','String','Path','HorizontalAlignment','right','Position',[6 18 30 22],'Units','normalized');

epath = uicontrol(f,'Style','edit',...
    'String','','HorizontalAlignment','left','Position',[51 18 352 22],'Units','normalized');

uicontrol(f,'Style','text','String','Atom','HorizontalAlignment','left','Position',[423 18 33 22],'Units','normalized');

eatom = uicontrol(f,'Style','edit',...
    'String','','HorizontalAlignment','left','Position',[471 18 100 22],'Units','normalized');

uicontrol(f,'Style','text','String','From','HorizontalAlignment','left','Position',[591 18 33 22],'Units','normalized');

efrom = uicontrol(f,'Style','edit',...
    'String','','HorizontalAlignment','left','Position',[639 18 100 22],'Units','normalized');

uicontrol(f,'Style','text','String','To','HorizontalAlignment','left','Position',[760 18 25 22],'Units','normalized');

eto = uicontrol(f,'Style','edit',...
    'String','','HorizontalAlignment','left','Position',[800 18 100 22],'Units','normalized');

bload = uicontrol(f,'Style','pushbutton','String','Load','Position',[918 18 100 22],'Units','normalized','Callback',@bload_Callback);

function bload_Callback(src,event)
dirname = get(epath,'String');
atom = get(eatom,'String');
start = get(efrom,'String');
last = get(eto,'String');

filelist = make_list(atom,start,last);
info = load_info(filelist,dirname);
set(t,'RowName', filelist);
set(t,'Data', info);

end

end
