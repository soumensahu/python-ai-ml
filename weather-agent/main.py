from openai import OpenAI
import requests
client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  #api_key="AIzaSyB_LY4_wQImHSxR9bSUHr5ET4vn3ONcwZw",
    api_key="AIzaSyAtLpQ3veKX9AZLLCqov2KqPJg50wwhbHg",
)

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%c+%t"
    response=requests.get(url)
    
    if response.status_code==200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

def main():
    user_query=input("> input : ")
    response=client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
         
        {
            "role":"user","content":user_query
        }
    ]
    )
    print(response.choices[0].message.content)

#main()


