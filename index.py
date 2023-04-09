import os
import json
import pandas as pd
from helper.maps_helper import MapsHelper
from dotenv import load_dotenv
load_dotenv()

MAPS_KEY = os.environ.get('GOOGLE_API_KEY')
maps_helper = MapsHelper(MAPS_KEY)

excel_writer = pd.ExcelWriter('./out/MDIP.xlsx', engine="xlsxwriter")
with pd.ExcelFile("./file/MDIP_2013_2023.xlsx") as excel_reader:
    for sheet in excel_reader.sheet_names:
        try:
            excel_df = pd.read_excel(excel_reader, sheet_name=sheet)
        except ValueError as error:
            print("Script executado com sucesso!")
        except Exception as error:
            print("Error:", error)
        else:
            errors = []
            output = []
            for index, row in excel_df.iterrows():
                if row["MUNICIPIO_CIRCUNSCRICAO"] != "S.PAULO":
                    continue

                lat = float(row["LATITUDE"])
                long = float(row["LONGITUDE"])
                isError, result = maps_helper.getNeighborhood(lat, long)
                dt = row.to_dict()
                if not isError:
                    dt["BAIRRO"] = result
                else:
                    dt["BAIRRO"] = "ERRO"
                    dt_error = { "NUM_BO": row["NUM_BO"], "maps_result": result }
                    errors.append(dt_error)
                output.append(dt)
            with open("./out/erro.json", "w") as json_out:
                json_out.write(json.dumps(errors, indent=2))

            index = index + 1
            df_output = pd.DataFrame(output)
            df_output.to_excel(excel_writer, sheet_name=sheet)
    excel_writer.close()
