from pydantic import BaseModel, Field, ConfigDict


class Stream(BaseModel):
    event_type: str = Field(alias="e")
    event_time: int = Field(alias="E")
    symbol: str = Field(alias="s")
    aggregate_trade_id: int = Field(alias="a")
    price: str = Field(alias="p")
    quantity: str = Field(alias="q")
    first_trade_id: int = Field(alias="f")
    last_trade_id: int = Field(alias="l")
    trade_time: int = Field(alias="T")
    market_buyer: bool = Field(alias="m")
    ignore: bool = Field(alias="M")

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
