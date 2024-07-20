from typing import List

from one_dragon.base.conditional_operation.atomic_op import AtomicOp
from one_dragon.base.conditional_operation.state_recorder import StateRecorder
from one_dragon.base.operation.one_dragon_context import OneDragonContext
from one_dragon.utils import i18_utils
from one_dragon.utils.i18_utils import gt
from zzz_od.application.devtools.screenshot_helper.screenshot_helper_config import ScreenshotHelperConfig
from zzz_od.application.dodge_assistant.dodge_assistant_config import DodgeAssistantConfig
from zzz_od.config.game_config import GameConfig, GamePlatformEnum
from zzz_od.config.one_dragon_config import OneDragonConfig
from zzz_od.context.battle_context import BattleContext
from zzz_od.context.battle_context import BattleEventEnum
from zzz_od.context.yolo_context import YoloContext
from zzz_od.context.yolo_context import YoloStateEventEnum
from zzz_od.controller.zzz_pc_controller import ZPcController


class ZContext(OneDragonContext, YoloContext, BattleContext):

    def __init__(self):
        OneDragonContext.__init__(self)
        YoloContext.__init__(self, event_bus=self)
        BattleContext.__init__(self, event_bus=self)

        self.one_dragon_config: OneDragonConfig = OneDragonConfig()

        self.init_instance_config()

    def init_instance_config(self) -> None:
        """
        按实例初始化配置
        :return:
        """
        instance_idx = 0

        # 基础配置
        self.game_config: GameConfig = GameConfig(instance_idx)

        # 应用配置
        self.screenshot_helper_config: ScreenshotHelperConfig = ScreenshotHelperConfig(instance_idx)
        self.dodge_assistant_config: DodgeAssistantConfig = DodgeAssistantConfig(instance_idx)

    def init_by_config(self) -> None:
        """
        根据配置进行初始化
        :return:
        """
        OneDragonContext.init_by_config(self)
        i18_utils.update_default_lang(self.game_config.game_language)

        if self.game_config.platform == GamePlatformEnum.PC.value.value:
            self.controller = ZPcController(
                game_config=self.game_config,
                win_title=self.game_config.win_title,
                standard_width=self.project_config.screen_standard_width,
                standard_height=self.project_config.screen_standard_height
            )
