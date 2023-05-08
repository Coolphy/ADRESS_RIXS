classdef app1_exported < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure            matlab.ui.Figure
        UITable             matlab.ui.control.Table
        PathEditFieldLabel  matlab.ui.control.Label
        PathEditField       matlab.ui.control.EditField
        AtomEditFieldLabel  matlab.ui.control.Label
        AtomEditField       matlab.ui.control.EditField
        FromEditFieldLabel  matlab.ui.control.Label
        FromEditField       matlab.ui.control.NumericEditField
        ToEditFieldLabel    matlab.ui.control.Label
        ToEditField         matlab.ui.control.NumericEditField
        ReadButton          matlab.ui.control.Button
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Position = [100 100 1024 768];
            app.UIFigure.Name = 'MATLAB App';

            % Create UITable
            app.UITable = uitable(app.UIFigure);
            app.UITable.ColumnName = {'Column 1'; 'Column 2'; 'Column 3'; 'Column 4'};
            app.UITable.RowName = {};
            app.UITable.Position = [13 54 998 704];

            % Create PathEditFieldLabel
            app.PathEditFieldLabel = uilabel(app.UIFigure);
            app.PathEditFieldLabel.HorizontalAlignment = 'right';
            app.PathEditFieldLabel.Position = [6 18 30 22];
            app.PathEditFieldLabel.Text = 'Path';

            % Create PathEditField
            app.PathEditField = uieditfield(app.UIFigure, 'text');
            app.PathEditField.Position = [51 18 352 22];

            % Create AtomEditFieldLabel
            app.AtomEditFieldLabel = uilabel(app.UIFigure);
            app.AtomEditFieldLabel.HorizontalAlignment = 'right';
            app.AtomEditFieldLabel.Position = [423 18 33 22];
            app.AtomEditFieldLabel.Text = 'Atom';

            % Create AtomEditField
            app.AtomEditField = uieditfield(app.UIFigure, 'text');
            app.AtomEditField.Position = [471 18 100 22];

            % Create FromEditFieldLabel
            app.FromEditFieldLabel = uilabel(app.UIFigure);
            app.FromEditFieldLabel.HorizontalAlignment = 'right';
            app.FromEditFieldLabel.Position = [591 18 33 22];
            app.FromEditFieldLabel.Text = 'From';

            % Create FromEditField
            app.FromEditField = uieditfield(app.UIFigure, 'numeric');
            app.FromEditField.Position = [639 18 100 22];

            % Create ToEditFieldLabel
            app.ToEditFieldLabel = uilabel(app.UIFigure);
            app.ToEditFieldLabel.HorizontalAlignment = 'right';
            app.ToEditFieldLabel.Position = [760 18 25 22];
            app.ToEditFieldLabel.Text = 'To';

            % Create ToEditField
            app.ToEditField = uieditfield(app.UIFigure, 'numeric');
            app.ToEditField.Position = [800 18 100 22];

            % Create ReadButton
            app.ReadButton = uibutton(app.UIFigure, 'push');
            app.ReadButton.Position = [918 18 100 22];
            app.ReadButton.Text = 'Read';

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = app1_exported

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end