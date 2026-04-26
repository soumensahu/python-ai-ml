from google import genai

client = genai.Client(
    api_key="AIzaSyB_LY4_wQImHSxR9bSUHr5ET4vn3ONcwZw"
)


response=client.models.generate_content(
    model="gemini-3-flash-preview", contents="what is the time now in india?"
)

print(response.text)