from tui.controls import Control
from tui.controls import DialogueWindow
from tui.controls.rich_format_text import RichFormatText
from tui.text_formats import BackgroundColours


class Scene:
    """
    The base class for a scene.
    """

    def __init__(self, width: int, height: int, background: str = ' ', exit_transition: callable = None):
        self._internal_rft: RichFormatText | None = None

        self.background = background
        self.background_rft = RichFormatText.create_by_size(width, height, background)
        [self.background_rft.set_format(i, slice(None), background=BackgroundColours.DEFAULT) for i in range(height)]
        self.controls: list[Control] = []  # list of controls in the scene
        self.width = width
        self.height = height
        self.on_scene_update: callable = None
        self.exit_transition = exit_transition

    def register_scene_update_hook(self, func: callable):
        """
        Register a function to be called when the scene is updated.
        """
        self.on_scene_update = func

    def remove_scene_update_hook(self):
        """
        Remove the function that is called when the scene is updated.
        """
        self.on_scene_update = None

    def add_control_at(self, control: Control, x: int, y: int):
        """
        Add a control at a specific position rather than its original position.
        """
        control.x_coord = x
        control.y_coord = y
        self.controls.append(control)
        self.render()

    def play(self):
        """
        The method for starting the scene.
        """
        return None  # default scene output

    def render(self, suppress_hook: bool = False):
        """
        Render the scene.
        """
        self._internal_rft = RichFormatText.create_by_size(self.width, self.height, self.background)
        self._internal_rft.copy_from(self.background_rft)

        # sort controls by z-index, lowest first, then by y-coordinate, and then by x-coordinate
        self.controls.sort(key=lambda c: (c.z_coord, c.y_coord, c.x_coord))
        for control in self.controls:
            control.render()
            self._internal_rft.copy_from(control.get_rft_object(), control.y_coord, control.x_coord)

        if self.on_scene_update is not None and not suppress_hook:
            self.on_scene_update(self)

    def get_rendered(self, force_rerender: bool = False, suppress_hook: bool = False) -> list[str]:
        """
        Get the list representation of the rendered scene.
        :param force_rerender: Force the scene to be re-rendered.
        :param suppress_hook: Suppress the scene update hook.
        :return: The list representation of the rendered scene.
        """
        if force_rerender or self._internal_rft is None:
            self.render(suppress_hook=suppress_hook)
        return self._internal_rft.render()

    def get_control(self, control_id: str) -> Control:
        """
        Get a control by its ID.
        """
        for control in self.controls:
            if control.control_id == control_id:
                return control
        raise ValueError(f'Control with ID "{control_id}" not found.')

    def get_rft(self, force_rerender: bool = False, suppress_hook: bool = False) -> RichFormatText:
        """
        Get the RichFormatText object of the rendered scene.
        :param force_rerender: Force the scene to be re-rendered.
        :param suppress_hook: Suppress the scene update hook.
        :return: The RichFormatText object of the rendered scene.
        """
        if force_rerender or self._internal_rft is None:
            self.render(suppress_hook=suppress_hook)
        return self._internal_rft

    def show_dialogue(self, dialogue: DialogueWindow, func: callable):
        """
        Show a dialogue window. Ask for user input and return the result.
        If func is None, the dialogue will only be displayed on top as if it is a general control.
        """
        dialogue.z_coord = max([c.z_coord for c in self.controls] + [0]) + 1
        self.controls.append(dialogue)
        self.render()

        if func is None:
            return None

        result = func(self)

        self.controls.remove(dialogue)
        self.render()
        return result
