import requests
import pandas as pd
import time
import json
page = 20
per_page = 40
search_queries = ['Аналитик данных', "Инженер данных", "ML инженер", "AI разработчик"]  


def query(per_page, search_queries, pages_to_parse):

    for search_query in search_queries:
        for page in range(pages_to_parse):
            url = "https://api.hh.ru/vacancies"
            params = {
                "page" : page,
                "per_page" : per_page,
                "text" : f"!{search_query}"
            }
            response = requests.get(url, params = params)

            data_json = response.json()

            response = data_json["items"]

            time.sleep(0.5) 

            yield from response
                   
      

def create_data_frame():

    data_frame = []
    for data in query(per_page, search_queries, page):
       

        data_string = {
            "id" : str(data["id"]),
            "Job_title" : data["name"],
            "Company" : data["employer"]["name"],
            "Region" : data["area"]["name"],
            "Job description" : " ".join(
                (data.get("snippet", {}).get("responsibility") or "")
                .replace("<highlighttext>", "*")
                .replace("</highlighttext>", "*")
                .split("*")
            ),
            "Employment_type" : data["schedule"]["name"],
            "Schedule" : data["work_format"][0]["name"] if data["work_format"] else None,
            "Key_skills" : " ".join(
                (data.get("snippet", {}).get("requirement") or "")
                .replace("<highlighttext>", "*")
                .replace("</highlighttext>", "*")
                .split("*")
            ),
                
        }

        if not(data["salary"]):
            data_string["Salary"] = None
            data_string["Salary_currency"] = None
        else:
            data_string["Salary"] = data["salary"]["from"]
            data_string["Salary_currency"] = data["salary"]["currency"]
        data_frame.append(data_string)
    

    df = pd.DataFrame(data_frame)
    df.to_csv(r'C:\Users\User\Desktop\Проекты\визуализация\hh_job.csv', sep = ";", encoding = "utf-8-sig", index = False)    

if __name__ == "__main__":
    create_data_frame()     
