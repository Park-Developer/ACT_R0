import click
from flask import Flask
from flask.cli import AppGroup
from Flask_Web.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from Flask_Web import master
from config import ACT_logger

from Upbit_Trade.Strategy1 import Strategy

def make_strategy_CLI(app):
    strategy_cli=AppGroup("Strategy")

    @strategy_cli.command("strategy1_info_upload")
    def strategy1_info_upload():
        db = get_db()
        strategy1_obj=Strategy()

        strategy1_introduction=strategy1_obj.intro_part
        strategy1_para=strategy1_obj.para_reference

        # sql qry command
        insert_sql_cmd=("INSERT INTO strategy "
                        "(name, introduction, code, link, version, developer, contributor, "
                        "dynamic_ref,monitoring_time,dynamic_bid,minute_unit,dynamic_ask) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")

        # strategy1 upload data
        upload_data=(
            strategy1_introduction["name"],
            strategy1_introduction["introduction"],
            "code test",
            "link test",
            strategy1_introduction["version"],
            strategy1_introduction["developer"],
            strategy1_introduction["contributor"],
            strategy1_para["dynamic_ref"],
            strategy1_para["monitoring_time"],
            strategy1_para["dynamic_bid"],
            strategy1_para["minute_unit"],
            strategy1_para["dynamic_ask"]
        )

        db.execute(insert_sql_cmd, upload_data)
        db.commit()

    app.cli.add_command(strategy_cli)  # cli group 등록
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
                       "upbit_secret_key, allowed_ip, balance_update_time, current_cash_balance,"
                       "write_post, view_post, like_post, dislike_post) "
                       "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

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

    @master_cli.command('test_post_upload')
    def test_post_upload():
        db=get_db()
        try:
            insert_sql_cmd=("INSERT INTO post "
                       "(author_id , title, body, type, view_num, like_num, dislike_num) "
                       "VALUES (?,?,?,?,?,?,?)")

            # [REF] master id : 1
            ''' <TEST CASE1> '''
            test_post1_info=(1,"test_post1","이것은 테스트 포스트임\n아이구야","시황",1,1,0)

            db.execute(insert_sql_cmd, test_post1_info)
            db.commit()

            ''' <TEST CASE2> '''
            test_post2_info=(1,"test_post2","또다른 테스트 포스트임\n아이구야","일반",1,0,1)

            db.execute(insert_sql_cmd, test_post2_info)
            db.commit()

        except db.IntegrityError:
            ACT_logger.warning("cli_warn2 test_post already exists")

    app.cli.add_command(master_cli) # cli group 등록

def make_debug_CLI(app):
    pass

def make_CLI(app):
    make_master_CLI(app) # master command
    make_debug_CLI(app)  # debug command
    make_strategy_CLI(app)