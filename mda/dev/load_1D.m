function s = load_1D(filename)
    mda_file = mdaload(filename);
    pos=getfield(getfield(mda_file,'scan'),'positioners_data');
    positioner_name=getfield(getfield(getfield(mda_file,'scan'),'positioners'),'name');
    dets=getfield(getfield(mda_file,'scan'),'detectors_data');
    detector_name=getfield(getfield(getfield(mda_file,'scan'),'detectors'),'name');
    s = struct('xlabel',positioner_name,'x',pos,'ylabel',detector_name,'y',dets);
