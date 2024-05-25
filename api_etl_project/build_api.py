from fastapi import FastAPI
from pydantic import BaseModel
import json



app = FastAPI()

class CountryData(BaseModel):
    country_num: int
    country_code: str
    is_independent: bool
    region: str
    subregion: str
    area_size: float
    population: int
    language: str
    timezone: list
    currency: str

class DataInfo(BaseModel):
    message: str
    country_data: CountryData

def read_data_file():
    with open("api_clean_data.json", 'r') as file:
        data = json.loads(file.read())
    return data

def update_data_file(data):
    with open("api_clean_data.json", 'w') as file:
        file.write(json.dumps(data))

@app.get("/")
def sample_api():
    return {"Message":"Thanks for checking out our API end points. Please check our APIs in the docs page by visiting http://127.0.0.1:8000/docs"}

@app.get("/countries")
def collect_countries_info():
    api_data = read_data_file()
    return api_data

@app.get("/countries/{country_code}")
def collect_single_country_info(country_code: str):
    api_data = read_data_file()
    for single_data in api_data:
        if single_data['country_code'].lower() == country_code.lower():
            return single_data
    else:
        return {"message": "Data doesn't exist in the database"}

# @app.delete("/countries/delete/{country_num}")
# def delete_single_record(country_num: int):
#     api_data = read_data_file()
#     for single_data in range(len(api_data)):
#         if api_data[single_data]['country_num'] == country_num:
#             del api_data[single_data]
#             update_data_file(api_data)
#             return {"message": f"Country_num:{country_num} was deleted successfully"}


# @app.delete("/countries/delete")
# def delete_all_record():
#     api_data = read_data_file()
#     api_data.clear()
#     update_data_file(api_data)
#     return {"message": f"All the data got deleted successfully"}


@app.post("/countries/new_country", response_model=DataInfo)
def add_new_country(new_country:CountryData):
    api_data = read_data_file()
    for country in api_data:
        if new_country.country_code.lower() == country['country_code'].lower():
            return {"message": "Data is exist", "country_data":new_country}
    formatted_data = {
        "country_num": new_country.country_num,
        "country_code": new_country.country_code,
        "is_independent": new_country.is_independent,
        "region": new_country.region,
        "subregion": new_country.subregion,
        "area_size": new_country.area_size,
        "population": new_country.population,
        "language": new_country.language,
        "timezone": new_country.timezone,
        "currency": new_country.currency
    }
    api_data.append(formatted_data)
    update_data_file(api_data)
    return  {"message": "Successfully stored the in the Database", "country_data":new_country}


# "http://127.0.0.1:8000/countries/new_country"