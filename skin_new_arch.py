from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from brain_new_arch import EdgeDetect


class AppLayout(FloatLayout):
    edge_detect = ObjectProperty()


class ButtonsLayout(RelativeLayout):
    normal = StringProperty()
    down = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':
            self.normal = 'icons/cellphone-screenshot_white.png'
            self.down = 'icons/cellphone-screenshot_red.png'
        else:
            self.normal = 'icons/monitor-screenshot_white.png'
            self.down = 'icons/monitor-screenshot_red.png'

    def on_size(self, layout, size):
        if platform == 'android':
            self.ids.screen.min_state_time = 0.3
        else:
            self.ids.screen.min_state_time = 1
        if Window.width < Window.height:
            self.pos = (0, 0)
            self.size_hint = (1, 0.2)
            self.ids.other.pos_hint = {'center_x': .3, 'center_y': .5}
            self.ids.other.size_hint = (.2, None)
            self.ids.screen.pos_hint = {'center_x': .7, 'center_y': .5}
            self.ids.screen.size_hint = (.2, None)
        else:
            self.pos = (Window.width * 0.8, 0)
            self.size_hint = (0.2, 1)
            self.ids.other.pos_hint = {'center_x': .5, 'center_y': .7}
            self.ids.other.size_hint = (None, .2)
            self.ids.screen.pos_hint = {'center_x': .5, 'center_y': .3}
            self.ids.screen.size_hint = (None, .2)

    def activate_stream(self):
        # self.parent.edge_detect.connect_camera(analyze_pixels_resolution=720,
        #                                        enable_analyze_pixels=True,
        #                                        enable_video=False, mode=1)
        self.parent.edge_detect.capture_screenshot()
        print(self.parent.edge_detect.preview.OBJECT)
        # print(self.parent.edge_detect.T)
        # print(self.parent.edge_detect.T800)

    # def deactivate_stream(self):
    #     # self.parent.edge_detect.disconnect_camera()
    #     self.parent.edge_detect.connect_camera(analyze_pixels_resolution=720,
    #                                            enable_analyze_pixels=True,
    #                                            enable_video=False, mode=2)
    # print(self.parent.edge_detect.T)
    # print(self.parent.edge_detect.T800)

    def turn_off(self):
        # self.parent.edge_detect._image_available.set()
        # self.parent.edge_detect.T[0].join()
        pass
        # self.parent.edge_detect.disconnect_camera()


Builder.load_string("""
<AppLayout>:
    edge_detect: self.ids.preview
    EdgeDetect:
        aspect_ratio: '16:9'
        id:preview
    ButtonsLayout:
        id:buttons

<ButtonsLayout>:
    normal:
    down:
    Button:
        id:other
        on_press: root.turn_off()

        height: self.width
        width: self.height
        background_normal: 'icons/camera-flip-outline.png'
        background_down:   'icons/camera-flip-outline.png'
    Button:
        id:screen
        on_press: root.activate_stream()
        height: self.width
        width: self.height
        background_normal: root.normal
        background_down: root.down
""")


