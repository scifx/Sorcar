import bpy

from bpy.props import StringProperty, IntProperty
from bpy.types import Node
from .._base.node_base import ScNode
from .._base.node_selection import ScSelectionNode

class ScSelectManually(Node, ScSelectionNode):
    bl_idname = "ScSelectManually"
    bl_label = "Select Manually"
    
    prop_vert: StringProperty(default="[]")
    prop_edge: StringProperty(default="[]")
    prop_face: StringProperty(default="[]")
    prop_active: IntProperty()

    def save_selection(self):
        bpy.ops.object.mode_set(mode="OBJECT")
        self.prop_vert = str([i.index for i in self.inputs["Object"].default_value.data.vertices if i.select])
        self.prop_edge = str([i.index for i in self.inputs["Object"].default_value.data.edges if i.select])
        self.prop_face = str([i.index for i in self.inputs["Object"].default_value.data.polygons if i.select])
        self.prop_active = self.inputs["Object"].default_value.data.polygons.active
        bpy.ops.object.mode_set(mode="EDIT")
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        if (self.node_executable):
            if (self == context.space_data.edit_tree.nodes.active):
                if (self == context.space_data.edit_tree.nodes.get(str(context.space_data.edit_tree.node))):
                    layout.operator("sc.save_selection")
    
    def functionality(self):
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")
        for i in eval(self.prop_vert):
            self.inputs["Object"].default_value.data.vertices[i].select = True
        for i in eval(self.prop_edge):
            self.inputs["Object"].default_value.data.edges[i].select = True
        for i in eval(self.prop_face):
            self.inputs["Object"].default_value.data.polygons[i].select = True
            self.inputs["Object"].default_value.data.polygons.active = self.prop_active
        bpy.ops.object.mode_set(mode="EDIT")