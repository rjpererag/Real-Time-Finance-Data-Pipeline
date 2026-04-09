def parse_connection_details_to_str(conn_details: dict) -> str:
    conn_params = [f"'{k}' = '{v}'" for k, v in conn_details.items()]
    return ",".join(conn_params)
