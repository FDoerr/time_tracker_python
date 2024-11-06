from gui import root
import project_handler as db


def setup_database():
    db.create_projects_table()
    db.create_tasks_table()
    db.create_sessions_table()
    db.create_trigger_check_project_id_on_session_insert()
    db.create_trigger_check_project_id_on_session_update()


def main():
    setup_database()
    root.mainloop()


if __name__ == "__main__":
    main()