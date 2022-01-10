from panda3d.core import TextNode, TextFont, NodePath
from scripts.EZpanda.EZnode import Node



class Text(Node):
    __slots__=(
        'panda_text',
        'panda_node',
        'clear_frame',
        'clear_card'
        )
    #Alignment flags:
    A_BOXED_CENTER = TextNode.A_boxed_center
    A_BOXED_LEFT = TextNode.A_boxed_left
    A_BOXED_RIGHT = TextNode.A_boxed_right
    A_CENTER = TextNode.A_center
    A_LEFT = TextNode.A_left
    A_RIHT = TextNode.A_right

    #Render flags:
    RM_DISTANCE_FIELD = TextFont.RM_distance_field
    RM_EXTRUDE = TextFont.RM_extruded
    RM_INVALID = TextFont.RM_invalid
    RM_POLYGON = TextFont.RM_polygon
    RM_SOLID = TextFont.RM_solid
    RM_TEXTURE = TextFont.RM_texture
    RM_WIREFRAME = TextFont.RM_wireframe

    def __init__(self, font, text="", parent=None):
        Node.__init__(self, parent=parent)
        self.panda_text = TextNode('')
        self.panda_text.set_text(text)
        self.panda_node.attach_new_node(self.panda_text)
        self.font = font

        #Rotate by default so it will be facing the aspect2D camera then apply the transform:
        self.panda_node.set_p(-90)
        self.panda_node.flatten_light()

        #Pass through functions:
        self.clear_frame = self.panda_text.clear_frame
        self.clear_card = self.panda_text.clear_card

    def make_mesh(self):
        self.panda_text.setCardDecal(True)
        mesh = NodePath( self.panda_text.generate() )
        mesh.set_scale(self.scale)
        return mesh



    @property
    def text(self):
        return self.panda_text.get_text()
    @text.setter
    def text(self, str_):
        self.panda_text.set_text(str_)

    @property
    def font(self):
        return self.panda_text.get_font()
    @font.setter
    def font(self, font):
        self.panda_text.set_font(font)

    @property
    def small_caps(self):
        return self.panda_text.get_small_caps()
    @small_caps.setter
    def small_caps(self, bool_):
        self.panda_text.set_small_caps(bool_)

    @property
    def small_caps_scale(self):
        return self.panda_text.get_small_caps_scale()
    @small_caps_scale.setter
    def small_caps_scale(self, float_):
        self.panda_text.set_small_caps_scale(float_)

    @property
    def slant(self):
        return self.panda_text.get_slant()
    @slant.setter
    def slant(self, float_):
        self.panda_text.set_slant(float_)

    @property
    def color(self):
        return self.panda_text.get_text_color()
    @color.setter
    def color(self, rgba):
        self.panda_text.set_text_color(*rgba)

    @property
    def shadow(self):
        return self.panda_text.get_shadow()
    @shadow.setter
    def shadow(self, xy):
        self.panda_text.set_shadow(*xy)

    @property
    def shadow_color(self):
        return self.panda_text.get_shadow_color()
    @shadow_color.setter
    def shadow_color(self, rgba):
        self.panda_text.set_shadow_color(*rgba)

    @property
    def wordwrap(self):
        return self.panda_text.get_wordwrap()
    @wordwrap.setter
    def wordwrap(self, float_):
        self.panda_text.set_wordwrap(float_)

    @property
    def align(self):
        return self.panda_text.get_align()
    @align.setter
    def align(self, A_MODE):
        self.panda_text.set_align(A_MODE)

    @property
    def frame_color(self):
        return self.panda_text.get_frame_color()
    @frame_color.setter
    def frame_color(self, rgba):
        self.panda_text.set_frame_color(*rgba)

    @property
    def frame_width(self):
        return self.panda_text.get_frame_line_width()
    @frame_width.setter
    def frame_width(self, int_):
        self.panda_text.set_frame_line_width(int_)

    @property
    def frame_corners(self):
        return self.panda_text.get_frame_corners()
    @frame_corners.setter
    def frame_corners(self, bool_):
        self.panda_text.set_frame_corners(bool_)

    @property
    def card_color(self):
        return self.panda_text.get_card_color()
    @card_color.setter
    def card_color(self, rgba):
        self.panda_text.set_card_color(*rgba)

    @property
    def card_decal(self):
        return self.panda_text.get_card_decal()
    @card_decal.setter
    def card_decal(self, bool_):
        self.panda_text.set_card_decal(bool_)

    def set_card_margin(self, lrbt):
        self.panda_text.set_card_as_margin(*lrbt)

    def set_frame_margin(self, lrbt):
        self.panda_text.set_frame_as_margin(*lrbt)

