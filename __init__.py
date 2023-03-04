# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Auto Range",
    "author": "Tintwotin",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View > Range > Auto Range",
    "description": "Auto-sets the range to include all strips.",
    "warning": "",
    "doc_url": "",
    "category": "Sequencer",
}

from bpy.types import (
    Operator,
    PropertyGroup,
)
import bpy
import datetime
from operator import attrgetter
from bpy.props import (
    BoolProperty,
    PointerProperty,
)


class PropertyGroup(bpy.types.PropertyGroup):
    auto_range_toggle: BoolProperty(
        name="Auto Range", description="Auto sets range from first to last strip"
    )


def auto_range_active_strip(scene):

#    if not context.scene or not context.scene.sequence_editor:
#        return

    if bpy.context.scene.auto_range_strip.auto_range_toggle == False:
        return
    screen = bpy.context.screen
    if screen.is_animation_playing or screen.is_scrubbing:
        selection = bpy.context.selected_sequences
        bpy.ops.sequencer.select_all(action='SELECT')
        bpy.ops.sequencer.set_range_to_strips()
        #bpy.ops.sequencer.view_all()
        bpy.ops.sequencer.select_all(action='DESELECT')
        for s in selection: s.select = True       
        return


def menu_auto_range(self, context):
    manager = context.scene.auto_range_strip
    self.layout.separator()
    self.layout.prop(manager, "auto_range_toggle")


classes = (PropertyGroup,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.SEQUENCER_MT_range.append(menu_auto_range)
    bpy.types.SEQUENCER_MT_select.append(menu_auto_range)
    bpy.app.handlers.frame_change_post.append(auto_range_active_strip)
    bpy.types.Scene.auto_range_strip = PointerProperty(type=PropertyGroup)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.SEQUENCER_MT_context_menu.remove(menu_auto_range)
    bpy.types.SEQUENCER_MT_range.remove(menu_auto_range)
    bpy.app.handlers.frame_change_post.remove(auto_range_active_strip)


if __name__ == "__main__":
    register()
