import requests
import json

def callApiAi2Sys():
        rs_data = ""
        try:
            send_data = {
                "model": "gpt-4o-mini",
                "messages": []
            }
            send_data["messages"].append({
                "role": "system",
                "content": "Doanh nghiệp"
            })
            send_data["messages"].append({
                "role": "system",
                "content": "Doanh nghiệp"
            })
            send_data["messages"].append({
                "role": "user",
                "content": "Xin chào"
            })
            #18/05/2024 vì hàm post AI cần dùng nhiều lần, nên đóng gói lại
         
            response_ = requests.post(url="https://api.openai.com/v1/chat/completions", data=json.dumps(send_data), headers={
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "Cache-Control": "no-cache",
                            "User-Agent": "Min.Cafe 27.1",
                            "Authorization": "Bearer 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" 
                        }, timeout=3*60)
            response_ = response_.json()
            print("response_", response_)
        
            if "choices" in response_:
                if len(response_)>0:
                    if "message" in response_["choices"][0]:
                        if "content" in response_["choices"][0]["message"]:
                            rs_data = response_["choices"][0]["message"]["content"]
          
            print("rs_data:===",rs_data)
        except Exception as inst: 
            print("lõi", inst)


if __name__ == "__main__":
    callApiAi2Sys()