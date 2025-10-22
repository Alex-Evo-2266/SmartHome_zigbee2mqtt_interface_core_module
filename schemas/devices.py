from typing import List, Dict, Optional
from pydantic import BaseModel, Field


# --- Exposes / Options -------------------------------------------------------

class ZigbeeExposeFeature(BaseModel):
    type: str
    name: str
    property: Optional[str] = None
    value_min: Optional[float] = None
    value_max: Optional[float] = None
    value_on: Optional[str] = None
    value_off: Optional[str] = None
    description: Optional[str] = None
    access: Optional[int] = None
    unit: Optional[str] = None
    features: Optional[List["ZigbeeExposeFeature"]] = None

    class Config:
        extra = "ignore"


class ZigbeeOption(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    access: Optional[int] = None
    unit: Optional[str] = None

    class Config:
        extra = "ignore"


class ZigbeeDefinition(BaseModel):
    source: Optional[str] = None
    model: Optional[str] = None
    vendor: Optional[str] = None
    description: Optional[str] = None
    supports_ota: Optional[bool] = None
    exposes: List[ZigbeeExposeFeature] = Field(default_factory=list)
    options: List[ZigbeeOption] = Field(default_factory=list)

    class Config:
        extra = "ignore"


ZigbeeExposeFeature.model_rebuild()


# --- Network layer: endpoints / clusters ------------------------------------

class ZigbeeCluster(BaseModel):
    input: Optional[List[str]] = Field(default_factory=list)
    output: Optional[List[str]] = Field(default_factory=list)

    class Config:
        extra = "ignore"


class ZigbeeEndpoint(BaseModel):
    bindings: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    clusters: Optional[ZigbeeCluster] = None

    class Config:
        extra = "ignore"


# --- Main device -------------------------------------------------------------

class ZigbeeDevice(BaseModel):
    friendly_name: str
    ieee_address: str
    type: str

    definition: Optional[ZigbeeDefinition] = None
    endpoints: Dict[str, ZigbeeEndpoint] = Field(default_factory=dict)

    manufacturer: Optional[str] = None
    model_id: Optional[str] = None
    network_address: Optional[int] = None
    power_source: Optional[str] = None
    supported: Optional[bool] = None
    interview_completed: Optional[bool] = None
    software_build_id: Optional[str] = None
    date_code: Optional[str] = None

    class Config:
        extra = "ignore"


# --- Wrapper для всего списка устройств -------------------------------------

class ZigbeeDevicesList(BaseModel):
    __root__: List[ZigbeeDevice]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, idx):
        return self.__root__[idx]
