# Standards
from typing import List

# SPHINX
# from .base_repository import OracleBaseRepository
from func.src.repositories.oracle.base_repository import OracleBaseRepository


class EnumerateRepository(OracleBaseRepository):
    @classmethod
    async def get_activity(cls, code: int) -> list:
        sql = f"""
                SELECT 1
    		    FROM USPIXDB001.SINCAD_EXTERNAL_PROFESSIONAL
    		    WHERE CODE = :value
            """
        result = await cls.query(sql=sql, value=code)
        return result
    @classmethod
    async def get_city(cls, contry: str, state: str, id_city: float) -> list:
        sql = f"""
        SELECT 1
        FROM CORRWIN.TSCDXMUNICIPIO 
        WHERE SIGL_PAIS = '{contry}' 
        AND SIGL_ESTADO = '{state}' 
        AND NUM_SEQ_MUNI = {id_city}"""
        result = await cls.query(sql=sql, value=code)
        return result

    @classmethod
    async def get_country(cls, country_acronym: str) -> list:
        sql = f"""
            SELECT 1
            FROM CORRWIN.TSCPAIS
            WHERE SG_PAIS = :value
        """
        result = await cls.query(sql=sql, value=country_acronym)

        return result

    @classmethod
    async def get_marital_status(cls, code: int) -> list:
        sql = f"""
            SELECT 1
            FROM USPIXDB001.SINCAD_EXTERNAL_MARITAL_STATUS
            WHERE CODE = :value
        """
        result = await cls.query(sql=sql, value=code)

        return result

    @classmethod
    async def get_nationality(cls, code: int) -> list:
        sql = f"""
            SELECT 1
            FROM USPIXDB001.SINCAD_EXTERNAL_NATIONALITY
            WHERE CODE = :value
        """
        result = await cls.query(sql=sql, value=code)

        return result



import asyncio


if __name__ == '__main__':

    async def teste_repo():
        result_country = await EnumerateRepository.get_country("BR")
        result_ac = await EnumerateRepository.get_activity(105)
        result_na = await EnumerateRepository.get_nationality(1)
        result_ma = await EnumerateRepository.get_marital_status(1)

        print(result_ac)
        print(result_na)
        print(result_ma)
        print(result_country)
        if not all([result_ma, result_na, result_ac, result_country]):
            raise ValueError("FALSE")

    asyncio.run(teste_repo())

