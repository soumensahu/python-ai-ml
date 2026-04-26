import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
text="hey there ! I am soumen"
tokens=enc.encode(text)
print("tokens:",tokens)
decode= enc.decode([48467, 1354, 1073, 357, 939, 4069, 2712])

print("decode:",decode)