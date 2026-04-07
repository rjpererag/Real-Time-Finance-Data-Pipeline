from pyflink.table import TableEnvironment
from ..settings import JobSettings


def parse_connection_details_to_str(conn_details: dict) -> str:
    conn_params = [f"'{k}' = '{v}'" for k, v in conn_details.items()]
    return ",".join(conn_params)


def run_finance_job(
    t_env: TableEnvironment,
    conn_details: dict,
    job_settings: JobSettings,
):
    parsed_conn = parse_connection_details_to_str(conn_details)
    full_sql = f"{job_settings.schema} WITH ({parsed_conn})"

    t_env.execute_sql(full_sql)
    result_table = t_env.sql_query(f"SELECT * FROM {job_settings.table_name}")
    result_table.execute().print()
