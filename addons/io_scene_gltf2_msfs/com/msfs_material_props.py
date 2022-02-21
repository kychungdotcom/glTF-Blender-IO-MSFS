# glTF-Blender-IO-MSFS
# Copyright (C) 2022 The glTF-Blender-IO-MSFS authors

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy
from ..io.msfs_material import MSFSMaterial

from io_scene_gltf2.io.com.gltf2_io_extensions import Extension


class AsoboMaterialCommon:  # TODO: make sure all conditions for export are correct
    class Defaults:
        BaseColorFactor = [1.0, 1.0, 1.0, 1.0]
        EmissiveFactor = [0.0, 0.0, 0.0]
        MetallicFactor = 1.0
        RoughnessFactor = 1.0
        NormalScale = 1.0
        AlphaMode = "OPAQUE"
        AlphaCutoff = 0.5
        DoubleSided = False

    bpy.types.Material.msfs_material_type = bpy.props.EnumProperty(
        name="Type",
        items=(
            ("NONE", "Disabled", ""),
            ("msfs_standard", "Standard", ""),
            ("msfs_geo_decal", "Decal", ""),
            ("msfs_geo_decal_frosted", "Geo Decal Frosted", ""),
            ("msfs_windshield", "Windshield", ""),
            ("msfs_porthole", "Porthole", ""),
            ("msfs_glass", "Glass", ""),
            ("msfs_clearcoat", "Clearcoat", ""),
            ("msfs_parallax", "Parallax", ""),
            ("msfs_anisotropic", "Anisotropic", ""),
            ("msfs_hair", "Hair", ""),
            ("msfs_sss", "Sub-surface Scattering", ""),
            ("msfs_invisible", "Invisible", ""),
            ("msfs_fake_terrain", "Fake Terrain", ""),
            ("msfs_fresnel_fade", "Fresnel Fade", ""),
            ("msfs_environment_occluder", "Environment Occluder", ""),
            ("msfs_ghost", "Ghost", ""),
        ),
        default="NONE",
    )
    bpy.types.Material.msfs_base_color_factor = bpy.props.FloatVectorProperty(
        name="Base Color",
        description="The RGBA components of the base color of the material. The fourth component (A) is the alpha coverage of the material. The alphaMode property specifies how alpha is interpreted. These values are linear. If a baseColorTexture is specified, this value is multiplied with the texel values",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
        default=Defaults.BaseColorFactor,
    )
    bpy.types.Material.msfs_emissive_factor = bpy.props.FloatVectorProperty(
        name="Emissive Color",
        description="The RGB components of the emissive color of the material. These values are linear. If an emissiveTexture is specified, this value is multiplied with the texel values",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=3,
        default=Defaults.EmissiveFactor,
    )
    bpy.types.Material.msfs_metallic_factor = bpy.props.FloatProperty(
        name="Metallic Factor",
        description="The metalness of the material. A value of 1.0 means the material is a metal. A value of 0.0 means the material is a dielectric. Values in between are for blending between metals and dielectrics such as dirty metallic surfaces. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the metallic texel values",
        min=0.0,
        max=1.0,
        default=Defaults.MetallicFactor,
    )
    bpy.types.Material.msfs_roughness_factor = bpy.props.FloatProperty(
        name="Roughness Factor",
        description="The roughness of the material. A value of 1.0 means the material is completely rough. A value of 0.0 means the material is completely smooth. This value is linear. If a metallicRoughnessTexture is specified, this value is multiplied with the roughness texel values",
        min=0.0,
        max=1.0,
        default=Defaults.RoughnessFactor,
    )
    bpy.types.Material.msfs_normal_scale = bpy.props.FloatProperty(
        name="Normal Scale",
        description="The scalar multiplier applied to each normal vector of the texture. This value is ignored if normalTexture is not specified",
        min=0.0,
        max=1.0,
        default=Defaults.NormalScale,
    )
    bpy.types.Material.msfs_alpha_mode = bpy.props.EnumProperty(
        items=(
            (
                "OPAQUE",
                "Opaque",
                "The rendered output is fully opaque and any alpha value is ignored",
            ),
            (
                "MASK",
                "Mask",
                "The rendered output is either fully opaque or fully transparent depending on the alpha value and the specified alpha cutoff value. This mode is used to simulate geometry such as tree leaves or wire fences",
            ),
            (
                "BLEND",
                "Blend",
                "The rendered output is combined with the background using the normal painting operation (i.e. the Porter and Duff over operator). This mode is used to simulate geometry such as gauze cloth or animal fur",
            ),
            (
                "DITHER",
                "Dither",
                "The rendered output is blend with dithering dot pattern",
            ),
        ),
        default=Defaults.AlphaMode,
    )
    bpy.types.Material.msfs_alpha_cutoff = bpy.props.FloatProperty(
        name="Alpha Cutoff",
        description="When alphaMode is set to MASK the alphaCutoff property specifies the cutoff threshold. If the alpha value is greater than or equal to the alphaCutoff value then it is rendered as fully opaque, otherwise, it is rendered as fully transparent. alphaCutoff value is ignored for other modes",
        min=0.0,
        max=1.0,
        default=Defaults.AlphaCutoff,
    )
    bpy.types.Material.msfs_double_sided = bpy.props.BoolProperty(
        name="Double Sided",
        description="The doubleSided property specifies whether the material is double sided. When this value is false, back-face culling is enabled. When this value is true, back-face culling is disabled and double sided lighting is enabled. The back-face must have its normals reversed before the lighting equation is evaluated",
        default=Defaults.DoubleSided,
    )

    # Textures (reused across material types, but named different)
    # TODO: proper names per material type - also make sure these are right
    bpy.types.Material.msfs_base_color_texture = bpy.props.PointerProperty(
        name="Base Color Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_occlusion_metallic_roughness_texture = (
        bpy.props.PointerProperty(
            name="Occlusion Metallic Roughness Texture", type=bpy.types.Image
        )
    )
    bpy.types.Material.msfs_normal_texture = bpy.props.PointerProperty(
        name="Normal Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_blend_mask_texture = bpy.props.PointerProperty(
        name="Blend Mask Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_dirt_texture = bpy.props.PointerProperty(
        name="Dirt Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_wetness_ao_texture = bpy.props.PointerProperty(
        name="Wetness AO Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_opacity_texture = bpy.props.PointerProperty(
        name="Opacity Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_emissive_texture = bpy.props.PointerProperty(
        name="Emissive Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_detail_color_texture = bpy.props.PointerProperty(
        name="Detail Color Texture", type=bpy.types.Image
    )
    bpy.types.Material.msfs_detail_occlusion_metallic_roughness_texture = (
        bpy.props.PointerProperty(
            name="Detail Occlusion Metallic Roughness Texture", type=bpy.types.Image
        )
    )
    bpy.types.Material.msfs_detail_normal_texture = bpy.props.PointerProperty(
        name="Detail Normal Texture", type=bpy.types.Image
    )


class AsoboMaterialGeometryDecal:

    SerializedName = "ASOBO_material_blend_gbuffer"

    bpy.types.Material.msfs_base_color_blend_factor = bpy.props.FloatProperty(
        name="Base Color Blend Factor", min=0.0, max=1.0, default=0.0
    )
    bpy.types.Material.msfs_metallic_blend_factor = bpy.props.FloatProperty(
        name="Metallic Blend Factor", min=0.0, max=1.0, default=0.0
    )
    bpy.types.Material.msfs_roughness_blend_factor = bpy.props.FloatProperty(
        name="Roughness Blend Factor", min=0.0, max=1.0, default=0.0
    )
    bpy.types.Material.msfs_normal_blend_factor = bpy.props.FloatProperty(
        name="Normal Blend Factor", min=0.0, max=1.0, default=0.0
    )
    bpy.types.Material.msfs_emissive_blend_factor = bpy.props.FloatProperty(
        name="Emissive Blend Factor", min=0.0, max=1.0, default=0.0
    )
    bpy.types.Material.msfs_occlusion_blend_factor = bpy.props.FloatProperty(
        name="Occlusion Blend Factor", min=0.0, max=1.0, default=0.0
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialGeometryDecal.SerializedName, {}
        )
        if extension.get("baseColorBlendFactor"):
            material.msfs_base_color_blend_factor = extension.get(
                "baseColorBlendFactor"
            )
        if extension.get("metallicBlendFactor"):
            material.msfs_metallic_blend_factor = extension.get("metallicBlendFactor")
        if extension.get("roughnessBlendFactor"):
            material.msfs_roughness_blend_factor = extension.get("roughnessBlendFactor")
        if extension.get("normalBlendFactor"):
            material.msfs_normal_blend_factor = extension.get("normalBlendFactor")
        if extension.get("emissiveBlendFactor"):
            material.msfs_emissive_blend_factor = extension.get("emissiveBlendFactor")
        if extension.get("occlusionBlendFactor"):
            material.msfs_occlusion_blend_factor = extension.get("occlusionBlendFactor")

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_material_type == "msfs_geo_decal"
            or blender_material.msfs_material_type == "msfs_geo_decal_frosted"
        ):
            result[
                "baseColorBlendFactor"
            ] = blender_material.msfs_base_color_blend_factor
            result["metallicBlendFactor"] = blender_material.msfs_metallic_blend_factor
            result[
                "roughnessBlendFactor"
            ] = blender_material.msfs_roughness_blend_factor
            result["normalBlendFactor"] = blender_material.msfs_normal_blend_factor
            result["emissiveBlendFactor"] = blender_material.msfs_emissive_blend_factor
            result[
                "occlusionBlendFactor"
            ] = blender_material.msfs_occlusion_blend_factor

            gltf2_material.extensions[
                AsoboMaterialGeometryDecal.SerializedName
            ] = Extension(
                name=AsoboMaterialGeometryDecal.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialGhostEffect:

    SerializedName = "ASOBO_material_ghost_effect"

    class Defaults:
        bias = 1.0
        scale = 1.0
        power = 1.0

    bpy.types.Material.msfs_ghost_bias = bpy.props.FloatProperty(
        name="Ghost Bias", min=0.001, max=64.0, default=Defaults.bias
    )
    bpy.types.Material.msfs_ghost_scale = bpy.props.FloatProperty(
        name="Ghost Scale", min=0.0, max=1.0, default=Defaults.scale
    )
    bpy.types.Material.msfs_ghost_power = bpy.props.FloatProperty(
        name="Ghost Power", min=0.0, max=1.0, default=Defaults.power
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialGhostEffect.SerializedName, {}
        )
        if extension.get("bias"):
            material.msfs_ghost_bias = extension.get("bias")
        if extension.get("scale"):
            material.msfs_ghost_scale = extension.get("scale")
        if extension.get("power"):
            material.msfs_ghost_power = extension.get("power")

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_ghost":
            result["bias"] = blender_material.msfs_ghost_bias
            result["scale"] = blender_material.msfs_ghost_scale
            result["power"] = blender_material.msfs_ghost_power

            gltf2_material.extensions[
                AsoboMaterialGhostEffect.SerializedName
            ] = Extension(
                name=AsoboMaterialGhostEffect.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialDrawOrder:

    SerializedName = "ASOBO_material_draw_order"

    class Defaults:
        drawOrderOffset = 0

    bpy.types.Material.msfs_draw_order_offset = bpy.props.IntProperty(
        name="Draw Order Offset",
        description="Draw Order Offset, to manually sort decals draw order for example",
        min=-999,
        max=999,
        default=Defaults.drawOrderOffset,
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialDrawOrder.SerializedName, {}
        )
        if extension.get("drawOrderOffset"):
            material.msfs_draw_order_offset = extension.get("drawOrderOffset")

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_draw_order_offset
            != AsoboMaterialDrawOrder.Defaults.drawOrderOffset
        ):
            result["drawOrderOffset"] = blender_material.msfs_draw_order_offset

            gltf2_material.extensions[
                AsoboMaterialDrawOrder.SerializedName
            ] = Extension(
                name=AsoboMaterialDrawOrder.SerializedName,
                extension=result,
                required=False,
            )


class AsoboDayNightCycle:

    SerializedName = "ASOBO_material_day_night_switch"

    bpy.types.Material.msfs_day_night_cycle = bpy.props.BoolProperty(
        name="Day Night Cycle",
        description="The emissive will be related to the ingame Day Night Cycle. When this value is false the emissive is Always ON",
        default=False,
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboDayNightCycle.SerializedName)
        if extension is not None:
            material.msfs_day_night_cycle = True

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        if (
            blender_material.msfs_material_type == "msfs_standard"
            and blender_material.msfs_day_night_cycle
        ):
            gltf2_material.extensions[AsoboDayNightCycle.SerializedName] = Extension(
                name=AsoboDayNightCycle.SerializedName, extension={}, required=False
            )


class AsoboDisableMotionBlur:

    SerializedName = "ASOBO_material_disable_motion_blur"

    bpy.types.Material.msfs_disable_motion_blur = bpy.props.BoolProperty(
        name="Disable Motion Blur",
        description="When this value is ON, the MotionBlur is disabled on the material, no matter what is defined in graphic options",
        default=False,
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboDisableMotionBlur.SerializedName)
        if extension.get("enabled"):
            material.msfs_disable_motion_blur = True

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_material_type != "msfs_environment_occluder"
            and blender_material.msfs_disable_motion_blur
        ):
            result["enabled"] = True

            gltf2_material.extensions[
                AsoboDisableMotionBlur.SerializedName
            ] = Extension(
                name=AsoboDisableMotionBlur.SerializedName,
                extension=result,
                required=False,
            )


class AsoboPearlescent:

    SerializedName = "ASOBO_material_pearlescent"

    class Defaults:
        pearlShift = 0.0
        pearlRange = 0.0
        pearlBrightness = 0.0

    bpy.types.Material.msfs_use_pearl = bpy.props.BoolProperty(
        name="Use Pearl Effect", default=False
    )
    bpy.types.Material.msfs_pearl_shift = bpy.props.FloatProperty(
        name="Pearl Color Shift", min=-999.0, max=999.0, default=Defaults.pearlShift
    )
    bpy.types.Material.msfs_pearl_range = bpy.props.FloatProperty(
        name="Pearl Color Range", min=-999.0, max=999.0, default=Defaults.pearlRange
    )
    bpy.types.Material.msfs_pearl_brightness = bpy.props.FloatProperty(
        name="Pearl Color Brightness",
        min=-1.0,
        max=1.0,
        default=Defaults.pearlBrightness,
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboPearlescent.SerializedName, {})
        if extension:
            material.msfs_use_pearl = True
        if extension.get("pearlShift"):
            material.msfs_pearl_shift = extension.get("pearlShift")
        if extension.get("pearlRange"):
            material.msfs_pearl_range = extension.get("pearlRange")
        if extension.get("pearlBrightness"):
            material.msfs_pearl_brightness = extension.get("pearlBrightness")

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_material_type == "msfs_standard"
            and blender_material.msfs_use_pearl
        ):
            result["pearlShift"] = blender_material.msfs_pearl_shift
            result["pearlRange"] = blender_material.msfs_pearl_range
            result["pearlBrightness"] = blender_material.msfs_pearl_brightness

            gltf2_material.extensions[AsoboPearlescent.SerializedName] = Extension(
                name=AsoboPearlescent.SerializedName, extension=result, required=False
            )


class AsoboAlphaModeDither:

    SerializedName = "ASOBO_material_alphamode_dither"

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboAlphaModeDither.SerializedName, {}
        )
        if extension.get("enabled"):
            material.msfs_alpha_mode = "DITHER"

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_alpha_mode == "DITHER":
            result["enabled"] = True

            gltf2_material.extensions[AsoboAlphaModeDither.SerializedName] = Extension(
                name=AsoboAlphaModeDither.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialInvisible:

    SerializedName = "ASOBO_material_invisible"

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialInvisible.SerializedName, {}
        )
        if extension.get("enabled"):
            material.msfs_material_type = "msfs_invisible"

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_invisible":
            result["enabled"] = True

            gltf2_material.extensions[
                AsoboMaterialInvisible.SerializedName
            ] = Extension(
                name=AsoboMaterialInvisible.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialEnvironmentOccluder:

    SerializedName = "ASOBO_material_environment_occluder"

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialEnvironmentOccluder.SerializedName, {}
        )
        if extension.get("enabled"):
            material.msfs_material_type = "msfs_environment_occluder"

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_environment_occluder":
            result["enabled"] = True

            gltf2_material.extensions[
                AsoboMaterialEnvironmentOccluder.SerializedName
            ] = Extension(
                name=AsoboMaterialEnvironmentOccluder.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialUVOptions:

    SerializedName = "ASOBO_material_UV_options"

    class Defaults:
        AOUseUV2 = False
        clampUVX = False
        clampUVY = False
        clampUVZ = False
        UVOffsetU = 0.0
        UVOffsetV = 0.0
        UVTilingU = 0.0
        UVTilingV = 0.0
        UVRotation = 0.0

    bpy.types.Material.msfs_ao_use_uv2 = bpy.props.BoolProperty(
        name="AO Use UV2", default=Defaults.AOUseUV2
    )
    bpy.types.Material.msfs_clamp_uv_x = bpy.props.BoolProperty(
        name="Clamp UV X", default=Defaults.clampUVX
    )
    bpy.types.Material.msfs_clamp_uv_y = bpy.props.BoolProperty(
        name="Clamp UV Y", default=Defaults.clampUVY
    )
    bpy.types.Material.msfs_clamp_uv_y = bpy.props.BoolProperty( # Doesn't seem to actually be used, which makes sense. Keeping just in case
        name="Clamp UV Z", default=Defaults.clampUVZ
    )
    bpy.types.Material.msfs_uv_offset_u = bpy.props.FloatProperty(
        name="UV Offset U", min=-10.0, max=10.0, default=Defaults.UVOffsetU
    )
    bpy.types.Material.msfs_uv_offset_v = bpy.props.FloatProperty(
        name="UV Offset V", min=-10.0, max=10.0, default=Defaults.UVOffsetV
    )
    bpy.types.Material.msfs_uv_tiling_u = bpy.props.FloatProperty(
        name="UV Tiling U", min=-10.0, max=10.0, default=Defaults.UVTilingU
    )
    bpy.types.Material.msfs_uv_tiling_v = bpy.props.FloatProperty(
        name="UV Tiling V", min=-10.0, max=10.0, default=Defaults.UVTilingV
    )
    bpy.types.Material.msfs_uv_rotation = bpy.props.FloatProperty(
        name="UV Rotation", min=-360.0, max=360.0, default=Defaults.UVRotation
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialUVOptions.SerializedName, {}
        )
        if extension.get("AOUseUV2"):
            material.msfs_ao_use_uv2 = extension.get("AOUseUV2")
        if extension.get("clampUVX"):
            material.msfs_clamp_uv_x = extension.get("clampUVX")
        if extension.get("clampUVY"):
            material.msfs_clamp_uv_y = extension.get("clampUVY")
        if extension.get("clampUVZ"):
            material.msfs_clamp_uv_z = extension.get("clampUVZ")
        if extension.get("UVOffsetU"):
            material.msfs_uv_offset_u = extension.get("UVOffsetU")
        if extension.get("UVOffsetV"):
            material.msfs_uv_offset_v = extension.get("UVOffsetV")
        if extension.get("UVTilingU"):
            material.msfs_uv_tiling_u = extension.get("UVTilingU")
        if extension.get("UVTilingV"):
            material.msfs_uv_tiling_v = extension.get("UVTilingV")
        if extension.get("UVRotation"):
            material.msfs_uv_rotation = extension.get("UVRotation")

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_ao_use_uv2
            or blender_material.msfs_clamp_uv_x
            or blender_material.msfs_clamp_uv_y
            or blender_material.msfs_clamp_uv_z
            or (
                blender_material.msfs_uv_offset_u
                != AsoboMaterialUVOptions.Defaults.UVOffsetU
                or blender_material.msfs_uv_offset_v
                != AsoboMaterialUVOptions.Defaults.UVOffsetV
            )
            or (
                blender_material.msfs_uv_tiling_u
                != AsoboMaterialUVOptions.Defaults.UVTilingU
                or blender_material.msfs_uv_tiling_v
                != AsoboMaterialUVOptions.Defaults.UVTilingV
            )
            or blender_material.msfs_uv_rotation
            != AsoboMaterialUVOptions.Defaults.UVRotation
        ):
            result["AOUseUV2"] = blender_material.msfs_ao_use_uv2
            result["clampUVX"] = blender_material.msfs_clamp_uv_x
            result["clampUVY"] = blender_material.msfs_clamp_uv_y
            result["clampUVZ"] = blender_material.msfs_clamp_uv_z
            result["UVOffsetU"] = blender_material.msfs_uv_offset_u
            result["UVOffsetV"] = blender_material.msfs_uv_offset_v
            result["UVTilingU"] = blender_material.msfs_uv_tiling_u
            result["UVTilingV"] = blender_material.msfs_uv_tiling_v
            result["UVRotation"] = blender_material.msfs_uv_rotation

            gltf2_material.extensions[
                AsoboMaterialUVOptions.SerializedName
            ] = Extension(
                name=AsoboMaterialUVOptions.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialShadowOptions:

    SerializedName = "ASOBO_material_shadow_options"

    class Defaults:
        noCastShadow = False

    bpy.types.Material.msfs_no_cast_shadow = bpy.props.BoolProperty(
        name="Don't Cast Shadows", default=Defaults.noCastShadow
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialShadowOptions.SerializedName, {}
        )
        if extension.get("noCastShadow"):
            material.msfs_no_cast_shadow = extension.get("noCastShadow")

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_no_cast_shadow:
            result["noCastShadow"] = blender_material.msfs_no_cast_shadow

            gltf2_material.extensions[
                AsoboMaterialShadowOptions.SerializedName
            ] = Extension(
                name=AsoboMaterialShadowOptions.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialResponsiveAAOptions:

    SerializedName = "ASOBO_material_antialiasing_options"

    class Defaults:
        responsiveAA = False

    bpy.types.Material.msfs_responsive_aa = bpy.props.BoolProperty(
        name="Responsive AA", default=Defaults.responsiveAA
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialResponsiveAAOptions.SerializedName, {}
        )
        if extension.get("responsiveAA"):
            material.msfs_responsive_aa = extension.get("responsiveAA")

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_responsive_aa:
            result["responsiveAA"] = blender_material.msfs_responsive_aa

            gltf2_material.extensions[
                AsoboMaterialResponsiveAAOptions.SerializedName
            ] = Extension(
                name=AsoboMaterialResponsiveAAOptions.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialDetail:

    SerializedName = "ASOBO_material_detail_map"

    class Defaults:
        UVScale = 1.0
        UVOffset = [0.0, 0.0]
        blendThreshold = 0.1
        NormalScale = 1.0

    bpy.types.Material.msfs_detail_uv_scale = bpy.props.FloatProperty(
        name="Detail UV Scale", min=0.01, max=100, default=Defaults.UVScale
    )
    bpy.types.Material.msfs_detail_uv_offset_u = bpy.props.FloatProperty(
        name="Detail UV Offset U", min=-10.0, max=10.0, default=Defaults.UVOffset[0]
    )
    bpy.types.Material.msfs_detail_uv_offset_v = bpy.props.FloatProperty(
        name="Detail UV Offset V", min=-10.0, max=10.0, default=Defaults.UVOffset[1]
    )
    bpy.types.Material.msfs_detail_blend_threshold = bpy.props.FloatProperty(
        name="Blend Threshold", min=0.001, max=1.0, default=Defaults.blendThreshold
    )
    bpy.types.Material.msfs_detail_normal_scale = (
        bpy.props.FloatProperty(  # TODO: not sure where this is used in 3ds max
            name="Detail Normal Scale", min=0.0, max=1.0, default=Defaults.NormalScale
        )
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialDetail.SerializedName, {}
        )
        if extension.get("UVScale"):
            material.msfs_detail_uv_scale = extension.get("UVScale")
        if extension.get("UVOffset"):
            material.msfs_detail_uv_offset_u = extension.get("UVOffset")[0]
            material.msfs_detail_uv_offset_v = extension.get("UVOffset")[1]
        if extension.get("blendThreshold"):
            material.msfs_detail_blend_threshold = extension.get("blendThreshold")
        if extension.get("detailColorTexture"):
            material.msfs_detail_color_texture = MSFSMaterial.create_image(
                extension.get("detailColorTexture"), import_settings
            )
        if extension.get("detailNormalTexture"):
            material.msfs_detail_normal_texture = MSFSMaterial.create_image(
                extension.get("detailNormalTexture"), import_settings
            )
        if extension.get("detailMetalRoughAOTexture"):
            material.msfs_detail_occlusion_metallic_roughness_texture = (
                MSFSMaterial.create_image(
                    extension.get("detailMetalRoughAOTexture"), import_settings
                )
            )
        if extension.get("blendMaskTexture"):
            material.msfs_blend_mask_texture = MSFSMaterial.create_image(
                extension.get("blendMaskTexture"), import_settings
            )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type != "msfs_parallax" and (
            blender_material.msfs_detail_color_texture
            or blender_material.msfs_detail_normal_texture
            or blender_material.msfs_detail_occlusion_metallic_roughness_texture
            or blender_material.msfs_blend_mask_texture
        ):
            if blender_material.msfs_detail_color_texture:
                result["detailColorTexture"] = MSFSMaterial.export_image(
                    blender_material,
                    blender_material.msfs_detail_color_texture,
                    export_settings,
                )
            if blender_material.msfs_detail_normal_texture:
                result["detailNormalTexture"] = MSFSMaterial.export_image(
                    blender_material,
                    blender_material.msfs_detail_normal_texture,
                    export_settings,
                )
            if blender_material.msfs_detail_occlusion_metallic_roughness_texture:
                result["detailMetalRoughAOTexture"] = MSFSMaterial.export_image(
                    blender_material,
                    blender_material.msfs_detail_occlusion_metallic_roughness_texture,
                    export_settings,
                )
            if blender_material.msfs_blend_mask_texture:
                result["blendMaskTexture"] = MSFSMaterial.export_image(
                    blender_material,
                    blender_material.msfs_blend_mask_texture,
                    export_settings,
                )
            if (
                blender_material.msfs_detail_uv_scale
                != AsoboMaterialDetail.Defaults.UVScale
            ):
                result["UVScale"] = blender_material.msfs_detail_uv_scale
            if (
                blender_material.msfs_detail_blend_threshold
                != AsoboMaterialDetail.Defaults.blendThreshold
            ):
                result["blendThreshold"] = blender_material.msfs_detail_blend_threshold
            if (
                blender_material.msfs_detail_uv_offset_u
                != AsoboMaterialDetail.Defaults.UVOffset[0]
                or blender_material.msfs_detail_uv_offset_v
                != AsoboMaterialDetail.Defaults.UVOffset[1]
            ):
                result["UVOffset"] = (
                    blender_material.msfs_detail_uv_offset_u,
                    blender_material.msfs_detail_uv_offset_v,
                )

            gltf2_material.extensions[AsoboMaterialDetail.SerializedName] = Extension(
                name=AsoboMaterialDetail.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialFakeTerrain:

    SerializedName = "ASOBO_material_fake_terrain"

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialFakeTerrain.SerializedName, {}
        )
        if extension.get("enabled"):
            material.msfs_material_type = "msfs_fake_terrain"

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_fake_terrain":
            result["enabled"] = True

            gltf2_material.extensions[
                AsoboMaterialFakeTerrain.SerializedName
            ] = Extension(
                name=AsoboMaterialFakeTerrain.SerializedName,
                extension=result,
                required=False,
            )


class AsoboMaterialFresnelFade:

    SerializedName = "ASOBO_material_fresnel_fade"

    class Defaults:
        fresnelFactor = 1.0
        fresnelOpacityOffset = 1.0

    bpy.types.Material.msfs_fresnel_factor = bpy.props.FloatProperty(
        name="Fresnel Factor", min=0.001, max=100.0, default=Defaults.fresnelFactor
    )
    bpy.types.Material.msfs_fresnel_opacity_offset = bpy.props.FloatProperty(
        name="Fresnel Opacity Bias",
        min=-1.0,
        max=1.0,
        default=Defaults.fresnelOpacityOffset,
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboMaterialFresnelFade.SerializedName, {}
        )
        if extension:
            material.msfs_material_type = "msfs_fresnel_fade"
            if extension.get("fresnelFactor"):
                material.msfs_fresnel_factor = extension.get("fresnelFactor")
            if extension.get("fresnelOpacityOffset"):
                material.msfs_fresnel_opacity_offset = extension.get(
                    "fresnelOpacityOffset"
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_fresnel_fade":
            result["fresnelFactor"] = blender_material.msfs_fresnel_factor
            result[
                "fresnelOpacityOffset"
            ] = blender_material.msfs_fresnel_opacity_offset

            gltf2_material.extensions[
                AsoboMaterialFresnelFade.SerializedName
            ] = Extension(
                name=AsoboMaterialFresnelFade.SerializedName,
                extension=result,
                required=False,
            )


class AsoboSSS:

    SerializedName = "ASOBO_material_SSS"

    class Defaults:
        SSSColor = [1.0, 1.0, 1.0, 1.0]

    bpy.types.Material.msfs_sss_color = bpy.props.FloatVectorProperty(
        name="SSS Color",
        description="The RGBA components of the SSS color of the material. These values are linear. If a SSSTexture is specified, this value is multiplied with the texel values",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
        default=Defaults.SSSColor,
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboSSS.SerializedName, {})
        if extension:
            material.msfs_material_type = "msfs_sss"  # TODO: handle hair being weird. maybe have this go first before calling hair?
            if extension.get("SSSColor"):
                material.msfs_sss_color = extension.get("SSSColor")
            if extension.get("opacityTexture"):
                material.msfs_opacity_texture = MSFSMaterial.create_image(
                    extension.get("opacityTexture"), import_settings
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_material_type == "msfs_sss"
            or blender_material.msfs_material_type == "msfs_hair"
        ):
            result["SSSColor"] = blender_material.msfs_sss_color
            if blender_material.msfs_opacity_texture:
                result["opacityTexture"] = MSFSMaterial.export_image(
                    blender_material,
                    blender_material.msfs_opacity_texture,
                    export_settings,
                )

            gltf2_material.extensions[AsoboSSS.SerializedName] = Extension(
                name=AsoboSSS.SerializedName, extension=result, required=False
            )


class AsoboAnisotropic:

    SerializedName = "ASOBO_material_anisotropic"

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboAnisotropic.SerializedName, {})
        if extension:
            # MUST BE CALLED AFTER SSS
            if material.msfs_material_type == "msfs_sss":
                material.msfs_material_type = "msfs_hair"  # SSS and hair share identical properties, except for this. If present, switch from SSS to hair
            else:
                material.msfs_material_type = "msfs_anisotropic"
            if extension.get("anisotropicTexture"):
                material.msfs_wetness_ao_texture = MSFSMaterial.create_image(
                    extension.get("anisotropicTexture"), import_settings
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_material_type == "msfs_anisotropic"
            or blender_material.msfs_material_type == "msfs_hair"
        ) and blender_material.msfs_wetness_ao_texture:
            result["anisotropicTexture"] = MSFSMaterial.export_image(
                blender_material,
                blender_material.msfs_wetness_ao_texture,
                export_settings,
            )

            gltf2_material.extensions[AsoboAnisotropic.SerializedName] = Extension(
                name=AsoboAnisotropic.SerializedName, extension=result, required=False
            )


class AsoboWindshield:

    SerializedName = "ASOBO_material_windshield_v2"

    class Defaults:
        rainDropScale = 1
        wiper1State = 0
        wiper2State = 0
        wiper3State = 0
        wiper4State = 0

    bpy.types.Material.msfs_rain_drop_scale = bpy.props.IntProperty(
        name="Rain Drop Scale", min=0, max=100, default=Defaults.rainDropScale
    )
    bpy.types.Material.msfs_wiper_1_state = bpy.props.IntProperty(
        name="Wiper 1 State", min=0, max=1, default=Defaults.wiper1State
    )
    bpy.types.Material.msfs_wiper_2_state = bpy.props.IntProperty(
        name="Wiper 2 State", min=0, max=1, default=Defaults.wiper2State
    )
    bpy.types.Material.msfs_wiper_3_state = bpy.props.IntProperty(
        name="Wiper 3 State", min=0, max=1, default=Defaults.wiper3State
    )
    bpy.types.Material.msfs_wiper_4_state = bpy.props.IntProperty(
        name="Wiper 4 State", min=0, max=1, default=Defaults.wiper4State
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboWindshield.SerializedName, {})
        if extension:
            material.msfs_material_type = "msfs_windshield"
            if extension.get("rainDropScale"):
                material.msfs_rain_drop_scale = extension.get("rainDropScale")
            if extension.get("wiper1State"):
                material.msfs_wiper_1_state = extension.get("wiper1State")
            if extension.get("wiper2State"):
                material.msfs_wiper_2_state = extension.get("wiper2State")
            if extension.get("wiper3State"):
                material.msfs_wiper_3_state = extension.get("wiper3State")
            if extension.get("wiper4State"):
                material.msfs_wiper_4_state = extension.get("wiper4State")
            if extension.get("wiperMaskTexture"):
                material.msfs_wetness_ao_texture = MSFSMaterial.create_image(
                    extension.get("wiperMaskTexture"), import_settings
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_windshield":
            result["rainDropScale"] = blender_material.msfs_rain_drop_scale
            result["wiper1State"] = blender_material.msfs_wiper_1_state
            result["wiper2State"] = blender_material.msfs_wiper_2_state
            result["wiper3State"] = blender_material.msfs_wiper_3_state
            result["wiper4State"] = blender_material.msfs_wiper_4_state
            if blender_material.msfs_wetness_ao_texture:
                result["wiperMaskTexture"] = MSFSMaterial.export_image(
                    blender_material,
                    blender_material.msfs_wetness_ao_texture,
                    export_settings,
                )

            gltf2_material.extensions[AsoboWindshield.SerializedName] = Extension(
                name=AsoboWindshield.SerializedName, extension=result, required=False
            )


class AsoboClearCoat:

    SerializedName = "ASOBO_material_clear_coat"

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboClearCoat.SerializedName, {})
        if extension:
            material.msfs_material_type = "msfs_clearcoat"
            if extension.get("dirtTexture"):
                material.msfs_dirt_texture = MSFSMaterial.create_image(
                    extension.get("dirtTexture"), import_settings
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if (
            blender_material.msfs_material_type == "msfs_clearcoat"
            and blender_material.msfs_dirt_texture
        ):
            result["dirtTexture"] = MSFSMaterial.export_image(
                blender_material, blender_material.msfs_dirt_texture, export_settings
            )

            gltf2_material.extensions[AsoboClearCoat.SerializedName] = Extension(
                name=AsoboClearCoat.SerializedName, extension=result, required=False
            )


class AsoboParallaxWindow:

    SerializedName = "ASOBO_material_parallax_window"

    class Defaults:
        parallaxScale = 0.0
        roomSizeXScale = 1.0
        roomSizeYScale = 1.0
        roomNumberXY = 1
        corridor = False

    bpy.types.Material.msfs_parallax_scale = bpy.props.FloatProperty(
        name="Parallax Scale", min=0.0, max=1.0, default=Defaults.parallaxScale
    )
    bpy.types.Material.msfs_room_size_x = bpy.props.FloatProperty(
        name="Room Size X Scale", min=0.01, max=10.0, default=Defaults.roomSizeXScale
    )
    bpy.types.Material.msfs_room_size_y = bpy.props.FloatProperty(
        name="Room Size Y Scale", min=0.01, max=10.0, default=Defaults.roomSizeYScale
    )
    bpy.types.Material.msfs_room_number_xy = bpy.props.IntProperty(
        name="Room Number XY", min=1, max=16, default=Defaults.roomNumberXY
    )
    bpy.types.Material.msfs_parallax_corridor = bpy.props.BoolProperty(
        name="Corridor", default=Defaults.corridor
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(
            AsoboParallaxWindow.SerializedName, {}
        )
        if extension:
            material.msfs_material_type = "msfs_parallax"
            if extension.get("parallaxScale"):
                material.msfs_parallax_scale = extension.get("parallaxScale")
            if extension.get("roomSizeXScale"):
                material.msfs_room_size_x = extension.get("roomSizeXScale")
            if extension.get("roomSizeYScale"):
                material.msfs_room_size_y = extension.get("roomSizeYScale")
            if extension.get("roomNumberXY"):
                material.msfs_room_number_xy = extension.get("roomNumberXY")
            if extension.get("corridor"):
                material.msfs_parallax_corridor = extension.get("corridor")
            if extension.get("behindWindowMapTexture"):
                material.msfs_detail_color_texture = MSFSMaterial.create_image(
                    extension.get("behindWindowMapTexture"), import_settings
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_parallax":
            result["parallaxScale"] = blender_material.msfs_parallax_scale
            result["roomSizeXScale"] = blender_material.msfs_room_size_x
            result["roomSizeYScale"] = blender_material.msfs_room_size_y
            result["roomNumberXY"] = blender_material.msfs_room_number_xy
            result["corridor"] = blender_material.msfs_parallax_corridor

            if blender_material.msfs_detail_color_texture:
                result["behindWindowMapTexture"] = MSFSMaterial.export_image(
                    blender_material,
                    blender_material.msfs_detail_color_texture,
                    export_settings,
                )

            gltf2_material.extensions[AsoboParallaxWindow.SerializedName] = Extension(
                name=AsoboParallaxWindow.SerializedName,
                extension=result,
                required=False,
            )


class AsoboGlass:

    SerializedName = "ASOBO_material_glass"

    class Defaults:
        glassReflectionMaskFactor = 0.0
        glassDeformationFactor = 0.0

    bpy.types.Material.msfs_glass_reflection_mask_factor = bpy.props.FloatProperty(
        name="Glass Reflection Mask Factor",
        min=0.0,
        max=1.0,
        default=Defaults.glassReflectionMaskFactor,
    )
    bpy.types.Material.msfs_glass_deformation_factor = bpy.props.FloatProperty(
        name="Glass Deformation Factor",
        min=0.0,
        max=1.0,
        default=Defaults.glassDeformationFactor,
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboGlass.SerializedName, {})
        if extension:
            material.msfs_material_type = "msfs_glass"
            if extension.get("glassReflectionMaskFactor"):
                material.msfs_glass_reflection_mask_factor = extension.get(
                    "glassReflectionMaskFactor"
                )
            if extension.get("glassDeformationFactor"):
                material.msfs_glass_deformation_factor = extension.get(
                    "glassDeformationFactor"
                )

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = {}
        if blender_material.msfs_material_type == "msfs_glass":
            result[
                "glassReflectionMaskFactor"
            ] = blender_material.msfs_glass_reflection_mask_factor
            result[
                "glassDeformationFactor"
            ] = blender_material.msfs_glass_deformation_factor

            gltf2_material.extensions[AsoboGlass.SerializedName] = Extension(
                name=AsoboGlass.SerializedName, extension=result, required=False
            )


class AsoboTags:  # TODO: make sure this works and also sort these classes

    SerializedName = "ASOBO_tags"

    class AsoboTag:
        Collision = "Collision"
        Road = "Road"

    bpy.types.Material.msfs_collision_material = bpy.props.BoolProperty(
        name="Collision Material", default=False
    )
    bpy.types.Material.msfs_road_collision_material = bpy.props.BoolProperty(
        name="Road Collision Material", default=False
    )

    @staticmethod
    def from_dict(material, obj, import_settings):
        assert isinstance(obj, dict)
        extension = obj.get("extensions", {}).get(AsoboTags.SerializedName, [])
        if extension:
            if AsoboTags.AsoboTag.Collision in extension:
                material.msfs_collision_material = True
            if AsoboTags.AsoboTag.Road in extension:
                material.msfs_road_collision_material = True

    @staticmethod
    def to_extension(blender_material, gltf2_material, export_settings):
        result = []
        if blender_material.msfs_material_type != "msfs_environment_occluder" and (
            blender_material.msfs_collision_material
            or blender_material.msfs_road_collision_material
        ):
            if blender_material.msfs_collision_material:
                result.append(AsoboTags.AsoboTag.Collision)
            if blender_material.msfs_road_collision_material:
                result.append(AsoboTags.AsoboTag.Road)

            gltf2_material.extensions[AsoboTags.SerializedName] = Extension(
                name=AsoboTags.SerializedName, extension=result, required=False
            )