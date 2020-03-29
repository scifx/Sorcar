import bpy

from bpy.props import EnumProperty, BoolProperty
from bpy.types import Node
from .._base.node_base import ScNode
from ...helper import focus_on_object

class ScSetSelectionMode(Node, ScNode):
    bl_idname = "ScSetSelectionMode"
    bl_label = "Set Selection Mode"

    in_selection_type: EnumProperty(name="Mode", items=[("VERT", "Vertices", "", "VERTEXSEL", 1), ("EDGE", "Edges", "", "EDGESEL", 2), ("FACE", "Faces", "", "FACESEL", 4)], default={'VERT'}, options={"ENUM_FLAG"}, update=ScNode.update_value)

    def init(self, context):
        self.node_executable = False
        super().init(context)
        self.inputs.new("ScNodeSocketObject", "Object")
        self.inputs.new("ScNodeSocketSelectionType", "Selection Type").init("in_selection_type", True)
        self.outputs.new("ScNodeSocketObject", "Object")
    
    def error_condition(self):
        return (
            self.inputs["Object"].default_value == None
            or len(self.inputs["Selection Type"].default_value) == 0
        )
    
    def pre_execute(self):
        focus_on_object(self.inputs["Object"].default_value, True)
    
    def functionality(self):
        bpy.context.tool_settings.mesh_select_mode = ["VERT" in self.inputs["Selection Type"].default_value, "EDGE" in self.inputs["Selection Type"].default_value, "FACE" in self.inputs["Selection Type"].default_value]
    
    def post_execute(self):
        return {"Object": self.inputs["Object"].default_value}