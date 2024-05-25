import requests
import json

def collect_data(api_link:str) -> json:
    try:
        response = requests.get(api_link)
        if response.status_code == 200:
            return response.json()
    except Exception as error:
        return error

def data_pre_processing(datas:list) -> list:
    final_data = []
    count  = 0
    for data in datas:
        pre_processing_data = {
            "country_num": count,
            "country_code": data.get("cca3"),
            "is_independent": data.get("independent"),
            "region": data.get("region"),
            "subregion": data.get("subregion"),
            "area_size": data.get("area"),
            "population": data.get("population"),
            "language": data.get("languages").get(list(data.get("languages").keys())[0]),
            "timezone": data.get("timezones"),
            "currency": data.get("currencies").get(list(data.get("currencies").keys())[0]).get("name")
        }
        final_data.append(pre_processing_data)
        count = count + 1
    return final_data

def write_to_file(final_clean_data: list, output_file:str) -> None:
    try:
        with open(output_file, "w") as file:
            clean_data_json_str = json.dumps(final_clean_data)
            file.write(clean_data_json_str)
        return "Successfully write the data to a file."
    except Exception as error:
        return error


url = "https://restcountries.com/v3.1/independent?status=true"
output_file = "api_clean_data.json"
response_data = collect_data(url)
clean_data = data_pre_processing(response_data)
status = write_to_file(clean_data, output_file)
print(status)