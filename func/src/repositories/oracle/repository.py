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
    		    WHERE CODE = :code
            """
        result = await cls.query(sql=sql, filters=[code])
        return result

    @classmethod
    async def get_city(cls, country: str, state: str, id_city: float) -> list:
        sql = f"""
        SELECT 1
        FROM CORRWIN.TSCDXMUNICIPIO 
        WHERE SIGL_PAIS = :filter
        AND SIGL_ESTADO = :filter
        AND NUM_SEQ_MUNI = :filter
        """
        result = await cls.query(sql=sql, filters=[country, state, id_city])
        return result

    @classmethod
    async def get_country(cls, country_acronym: str) -> list:
        sql = f"""
            SELECT 1
            FROM CORRWIN.TSCPAIS
            WHERE SG_PAIS = :filter
        """
        result = await cls.query(sql=sql, filters=[country_acronym])

        return result

    @classmethod
    async def get_marital_status(cls, code: int) -> list:
        sql = f"""
            SELECT 1
            FROM USPIXDB001.SINCAD_EXTERNAL_MARITAL_STATUS
            WHERE CODE = :filter
        """
        result = await cls.query(sql=sql, filters=[code])

        return result

    @classmethod
    async def get_nationality(cls, code: int) -> list:
        sql = f"""
            SELECT 1
            FROM USPIXDB001.SINCAD_EXTERNAL_NATIONALITY
            WHERE CODE = :filter
        """
        result = await cls.query(sql=sql, filters=[code])

        return result

    async def get_state(cls, state: str) -> list:
        sql = f"""
            SELECT 1
            FROM CORRWIN.TSCESTADO
            WHERE SG_ESTADO = :filter
        """
        result = await cls.query(sql=sql, filters=[state])
        return result


if __name__ == '__main__':

    import asyncio

    async def teste_repo():
        result_country = await EnumerateRepository.get_country("BRA")
        result_ac = await EnumerateRepository.get_activity(105)
        result_na = await EnumerateRepository.get_nationality(1)
        result_ma = await EnumerateRepository.get_marital_status(1)
        result_city = await EnumerateRepository.get_city(state="SP", country="BRA", id_city=5325)
        print(result_city)
        print(result_ac)
        print(result_na)
        print(result_ma)
        print(result_country)
        if not all([result_ma, result_na, result_ac, result_country, result_city]):
            raise ValueError("FALSE")

    asyncio.run(teste_repo())
