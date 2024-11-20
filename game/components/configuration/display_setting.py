from components.constant.default import DefaultSetting


class DisplaySetting:
    def __init__(self, max_x_cell, max_y_cell, setting_data={}) -> None:
        self.cell_size = (
            setting_data["cell_size"]
            if "cell_size" in setting_data
            else DefaultSetting.CELL_SIZE
        )
        self.max_cell_size = (
            setting_data["max_cell_size"]
            if "max_cell_size" in setting_data
            else DefaultSetting.MAX_CELL_SIZE
        )
        self.min_cell_size = (
            setting_data["min_cell_size"]
            if "min_cell_size" in setting_data
            else DefaultSetting.MIN_CELL_SIZE
        )
        self.window_size = (
            setting_data["window_size"]
            if "window_size" in setting_data
            else DefaultSetting.WINDOW_SIZE
        )
        self.max_y_cell = max_x_cell
        self.max_x_cell = max_y_cell
        self.map_size_x = self.max_x_cell * self.cell_size
        self.map_size_y = self.max_y_cell * self.cell_size
