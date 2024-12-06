import json

def convert_text_to_json(text):
    print(text)
    start_index = text.find("{")
    end_index = text.rfind("}") + 1
    json_string = text[start_index:end_index]
    json_data = json.loads(json_string)
    return json_data


"""
local test
def main():
    with open("/Users/ritvijsaxena/Documents/assembly_hackathon/tests/response.txt", "r") as file:
        text = file.read()

    json_data = convert_text_to_json(text)
    print(json_data)

if __name__ == "__main__":
    main()

"""