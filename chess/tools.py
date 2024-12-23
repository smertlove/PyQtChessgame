def set_obj_color(obj, color: str, bg_color: str):
    obj.setAutoFillBackground(True)

    obj.setStyleSheet(
        f"""
            color: {color};
            background-color: {bg_color};
        """
    )
