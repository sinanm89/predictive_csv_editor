def return_enter_event(reader):
    """Return the event that happens when enter is pressed."""
    line = editor_app.get_next_line()
    line[3] = editor_app.textbox.text()
    editor_app.saved_lines.append(line)
    editor_app.line_postprocessor(editor_app, line)
    editor_app.debugger.setText(str(line))