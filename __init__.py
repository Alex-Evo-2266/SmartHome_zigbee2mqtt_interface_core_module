from app.ingternal.modules.classes.baseModules import BaseModule
from app.ingternal.modules.arrays.serviceDataPoll import servicesDataPoll, ObservableDict
from app.configuration.settings import SERVICE_POLL, SERVICE_DATA_POLL
from app.pkg import itemConfig, ConfigItemType, __config__
from .settings import ZIGBEE_SERVICE_PATH, ZIGBEE_SERVICE_COORDINATOR_INFO_PATH, ZIGBEE_SERVICE_COORDINATOR_DEVICE_PATH
from .services.ZigbeeService import ZigbeeService
from typing import Optional

class Module(BaseModule):
    
    @classmethod
    async def start(cls):
        await super().start()

        services: ObservableDict = servicesDataPoll.get(SERVICE_POLL)
        zigbee_service: Optional[ZigbeeService] = services.get(ZIGBEE_SERVICE_PATH)
        services_data: ObservableDict = servicesDataPoll.get(SERVICE_DATA_POLL)
        services_data.set(ZIGBEE_SERVICE_COORDINATOR_INFO_PATH, {})
        services_data.set(ZIGBEE_SERVICE_COORDINATOR_DEVICE_PATH, {})

        async def restart():
            if zigbee_service:
                await zigbee_service.restart()

        __config__.register_config(
            itemConfig(tag="zigbee2mqtt", key="zigbeeTopicks", type=ConfigItemType.MORE_TEXT, value="root"),
            restart
        )

        print(zigbee_service)

        if zigbee_service:
            await zigbee_service.start()

