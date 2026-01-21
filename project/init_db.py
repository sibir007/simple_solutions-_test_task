from dotenv import load_dotenv

load_dotenv()

from database.db import main, drop_db, create_db, init_db_with_start_value

if __name__=='__main__':
    # main()
    init_db_with_start_value()