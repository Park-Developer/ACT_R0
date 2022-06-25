def convert_DB_to_UserInfo(user_db)->dict:
    user_info={}

    user_info["username"]=user_db["username"]
    user_info["email"]=user_db["email"]
    user_info["tier"]=user_db["tier"]
    print("templa tool")
    print(user_info)
    return user_info