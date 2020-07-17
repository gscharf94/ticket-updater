from datetime import datetime

def append_to_file(message, code):
    date_obj = datetime.today()

    day = str(date_obj.day)
    mon = str(date_obj.month)
    hour = str(date_obj.hour)
    min = str(date_obj.minute)
    sec = str(date_obj.second)

    content = f"{mon.zfill(2)}-{day.zfill(2)} {hour.zfill(2)}:{min.zfill(2)}:{sec.zfill(2)} > {code} > {message}"

    print(content)
    with open('logs.txt','a+') as f:
        f.write(content+"\n")
        
def success_file(success):
    if success == True:
        message = "YES"
    elif success == False:
        message = "NO"
    elif success == None:
        return

    with open('success','w+') as f:
        f.write(message)
