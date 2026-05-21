from openai import OpenAI

API_KEY="AIzaSyAcs2EsZfBo_nC-XDtONeFHVbmsind-HJ8"

client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  api_key=API_KEY,
)

response=client.chat.completions.create(
    model="gemini-3.5-flash",
    messages=[
        {
            "role":"user",
            "content":[
                {"type":"text","text":"generate a caption for this image in 50 words"},
                {"type":"image_url","image_url":{"url":"https://images.pexels.com/photos/37662141/pexels-photo-37662141.jpeg?_gl=1*1so5y2o*_ga*MTIwNjQ5MTIyNi4xNzc5MzMzMzk5*_ga_8JE65Q40S6*czE3NzkzMzMzOTgkbzEkZzEkdDE3NzkzMzM0MjkkajI5JGwwJGgw"}},
            ]
            
        }
    ]
)

print(f"Response: {response.choices[0].message.content}")