from tkinter.messagebox import showerror


def error_db(message_error, error):
    showerror(title="Connection Error DB",
              message=message_error)
