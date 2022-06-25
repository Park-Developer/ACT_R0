import click
from flask import Flask
from flask.cli import AppGroup
from Flask_Web.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from Flask_Web import master
from config import ACT_logger

def make_master_CLI(app):
    master_cli=AppGroup('master') # CLI 그룹 생성

    @master_cli.command('test') # command - function 매칭
    def test():
        print("ACT_R0 Test!")

    @master_cli.command('master_info_upload') # master정보를 user_list에 업로드
    def master_info_upload():
        db = get_db()
        try:
            insert_sql_cmd=("INSERT INTO user_list "
                       "(email, username, password, tier, login_state,"
                       "profile_img_addr, telegram_api, access_code, access_code_time, upbit_access_key,"
                       "upbit_secret_key, allowed_ip, target_coin, balance_update_time, current_cash_balance, current_coin_list) "
                       "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

            master_info=master.get_master_info()

            db.execute(insert_sql_cmd,master_info)
            db.commit()

        except db.IntegrityError:
            ACT_logger.warning("cli_warn1 master info already exists")
            
            # master 정보가 이미 존재하는 경우 기존 정보 삭제하고 다시 정보 삽입
            try:
                delete_master_info_cmd="DELETE FROM user_list where username='master';"
                db.execute(delete_master_info_cmd) # delete command

                db.execute(insert_sql_cmd, master_info)
                db.commit()
            except Exception as e:
                ACT_logger.error(e)

            ACT_logger.debug("master info load to DB successfully(retry)")
        else:
            ACT_logger.debug("master info load to DB successfully")

    app.cli.add_command(master_cli) # cli group 등록

def make_debug_CLI(app):
    pass

def make_CLI(app):
    make_master_CLI(app) # master command
    make_debug_CLI(app)  # debug command
