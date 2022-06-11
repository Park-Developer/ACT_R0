import json

def set_loginState(is_login:bool,user_data_addr:str,login_user_name:str)->None:
    with open(user_data_addr, 'r') as f:
        user_list = json.load(f)

    for email,user_info in user_list.items():
        if user_info["username"]==login_user_name:
            if is_login==True:
                user_info["login_state"]="ON"
            else:
                user_info["login_state"] = "OFF"
            break


def check_account(input_info:dict,check_data:dict)->bool: # 이거 다시 설장
    if check_data["data_type"]=="local_file": # local file로 비교하는 경우
        # user info loop
        with open(check_data["user_list_address"], 'r') as f1:
            user_list = json.load(f1)

        with open(check_data["access_code_address"], 'r') as f2:
            access_code_list = json.load(f2)

        for email,user_info in user_list.items():
            if (input_info["email"]==email and input_info["password"]==user_info["password"]): # email & password check
                user_name=user_info["username"]

                generated_code=access_code_list[user_name]["code"]

                if(input_info["access_code"]==generated_code): # access code check
                    return True
                else:
                    return False

        return False
    else: # ex) DB 비교
        pass

if __name__ == '__main__':
    code_info = {
        "code_method": 0,
        "code_length": 8
    }

