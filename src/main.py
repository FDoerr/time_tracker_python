import gui
import project_handler as db


def setup_database():
    db.create_projects_table()
    db.create_tasks_table()
    db.create_sessions_table()
    db.create_trigger_check_project_id_on_session_insert()
    db.create_trigger_check_project_id_on_session_update()


def place_gui_elements():
    gui.place_top_frame()
    gui.place_elements_in_top_frame()

    gui.place_middle_frame()
    gui.place_elements_in_middle_frame()

    gui.place_bottom_frame()
    gui.place_elements_in_bottom_frame()


def main():
    setup_database()
    place_gui_elements()
    gui.root.mainloop()
    

if __name__ == "__main__":
    main()