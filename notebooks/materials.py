"""
materials.py
================================================================================
Material definitions for the Spherical Tokamak neutronics model (vvij_ptnr_2023.ipynb).

This module was factored out of the notebook so that:
  1. The notebook stays focused on geometry / simulation / analysis logic.
  2. Material data (densities, nuclide weight fractions) can be version
     controlled, unit tested, and reused by other scripts without having to
     re-run or duplicate the notebook cells.
  3. Anyone extending the shielding material trade study only needs to touch
     this one file.


"""

import openmc


# Common constants

cu_den = 8.96  # density of the magnetic (copper) material, g/cm3
name_tag = "inshield"
density_unit = "g/cm3"


# 'inshield' candidate shielding material compositions.
# Each entry becomes one row in the material trade study
# (Newmaterial_file_<i+1>.xml when exported).
#*********************************************************************************

compositions = [
    # 1) Tungsten diboride
    {
        "name": "Tungsten diboride (WB2)",
        "density": 14.80,
        "nuclides": [
            {"nuclide": "W180", "amount": 0.001046193, "unit": "wo"},
            {"nuclide": "W182", "amount": 0.23103439, "unit": "wo"},
            {"nuclide": "W183", "amount": 0.12475857, "unit": "wo"},
            {"nuclide": "W184", "amount": 0.267128064, "unit": "wo"},
            {"nuclide": "W186", "amount": 0.247860668, "unit": "wo"},
            {"nuclide": "B10", "amount": 0.025506251, "unit": "wo"},
            {"nuclide": "B11", "amount": 0.102665864, "unit": "wo"},
        ],
    },
    # 2) Hafnium hydride
    {
        "name": "Hafnium hydride (HfH2)",
        "density": 11.40,
        "nuclides": [
            {"nuclide": "Hf174", "amount": 0.001582131, "unit": "wo"},
            {"nuclide": "Hf176", "amount": 0.052012549, "unit": "wo"},
            {"nuclide": "Hf177", "amount": 0.183922703, "unit": "wo"},
            {"nuclide": "Hf178", "amount": 0.269753297, "unit": "wo"},
            {"nuclide": "Hf179", "amount": 0.134678882, "unit": "wo"},
            {"nuclide": "Hf180", "amount": 0.346882173, "unit": "wo"},
            {"nuclide": "H1", "amount": 0.01116698, "unit": "wo"},
            {"nuclide": "H2", "amount": 0.00000128435, "unit": "wo"},
        ],
    },
    # 3) Zirconium hydride
    {
        "name": "Zirconium hydride (ZrH2)",
        "density": 5.6,
        "nuclides": [
            {"nuclide": "Zr90", "amount": 0.503376273, "unit": "wo"},
            {"nuclide": "Zr91", "amount": 0.109774184, "unit": "wo"},
            {"nuclide": "Zr92", "amount": 0.167792091, "unit": "wo"},
            {"nuclide": "Zr94", "amount": 0.170042364, "unit": "wo"},
            {"nuclide": "Zr96", "amount": 0.027394627, "unit": "wo"},
            {"nuclide": "H1", "amount": 0.021617974, "unit": "wo"},
            {"nuclide": "H2", "amount": 0.00000248635, "unit": "wo"},
        ],
    },
    # 4) Tungsten
    {
        "name": "Tungsten (W)",
        "density": 19.3,
        "nuclides": [
            {"nuclide": "W180", "amount": 0.001175, "unit": "wo"},
            {"nuclide": "W182", "amount": 0.262270, "unit": "wo"},
            {"nuclide": "W183", "amount": 0.142406, "unit": "wo"},
            {"nuclide": "W184", "amount": 0.306582, "unit": "wo"},
            {"nuclide": "W186", "amount": 0.287567, "unit": "wo"},
        ],
    },
    # 5) Tantalum Boride (TaB2)
    {
        "name": "Tantalum boride (TaB2)",
        "density": 12.54,
        "nuclides": [
            {"nuclide": "Ta180", "amount": 0.000107281, "unit": "wo"},
            {"nuclide": "Ta181", "amount": 0.893153995, "unit": "wo"},
            {"nuclide": "B10", "amount": 0.021241006, "unit": "wo"},
            {"nuclide": "B11", "amount": 0.085497718, "unit": "wo"},
        ],
    },
    # 6) Hafnium diboride (HfB2)
    {
        "name": "Hafnium diboride (HfB2)",
        "density": 11.19,
        "nuclides": [
            {"nuclide": "Hf174", "amount": 0.001427116, "unit": "wo"},
            {"nuclide": "Hf176", "amount": 0.046916441, "unit": "wo"},
            {"nuclide": "Hf177", "amount": 0.165902243, "unit": "wo"},
            {"nuclide": "Hf178", "amount": 0.24332329, "unit": "wo"},
            {"nuclide": "Hf179", "amount": 0.121483256, "unit": "wo"},
            {"nuclide": "Hf180", "amount": 0.312895199, "unit": "wo"},
            {"nuclide": "B10", "amount": 0.021502438, "unit": "wo"},
            {"nuclide": "B11", "amount": 0.086550016, "unit": "wo"},
        ],
    },
    # 7) Tantalum carbide (TaC)
    {
        "name": "Tantalum carbide (TaC)",
        "density": 14.5,
        "nuclides": [
            {"nuclide": "Ta180", "amount": 0.000112624, "unit": "wo"},
            {"nuclide": "Ta181", "amount": 0.937642235, "unit": "wo"},
            {"nuclide": "C12", "amount": 0.061579118, "unit": "wo"},
            {"nuclide": "C13", "amount": 0.000666023, "unit": "wo"},
        ],
    },
    # 8) Hafnium Carbide (HfC)
    {
        "name": "Hafnium carbide (HfC)",
        "density": 12.76,
        "nuclides": [
            {"nuclide": "Hf174", "amount": 0.00149912, "unit": "wo"},
            {"nuclide": "Hf176", "amount": 0.049283575, "unit": "wo"},
            {"nuclide": "Hf177", "amount": 0.174272718, "unit": "wo"},
            {"nuclide": "Hf178", "amount": 0.255599987, "unit": "wo"},
            {"nuclide": "Hf179", "amount": 0.127612603, "unit": "wo"},
            {"nuclide": "Hf180", "amount": 0.328682095, "unit": "wo"},
            {"nuclide": "C12", "amount": 0.062375267, "unit": "wo"},
            {"nuclide": "C13", "amount": 0.000674634, "unit": "wo"},
        ],
    },
    # 9) Zirconium diboride (ZrB2)
    {
        "name": "Zirconium diboride (ZrB2)",
        "density": 6.17,
        "nuclides": [
            {"nuclide": "Zr90", "amount": 0.415918058, "unit": "wo"},
            {"nuclide": "Zr91", "amount": 0.090701664, "unit": "wo"},
            {"nuclide": "Zr92", "amount": 0.138639353, "unit": "wo"},
            {"nuclide": "Zr94", "amount": 0.140498656, "unit": "wo"},
            {"nuclide": "Zr96", "amount": 0.022634996, "unit": "wo"},
            {"nuclide": "B10", "amount": 0.038129847, "unit": "wo"},
            {"nuclide": "B11", "amount": 0.153477425, "unit": "wo"},
        ],
    },
    # 10) Titanium diboride (TiB2)
    {
        "name": "Titanium diboride (TiB2)",
        "density": 4.38,
        "nuclides": [
            {"nuclide": "Ti46", "amount": 0.056829394, "unit": "wo"},
            {"nuclide": "Ti47", "amount": 0.051249781, "unit": "wo"},
            {"nuclide": "Ti48", "amount": 0.507813689, "unit": "wo"},
            {"nuclide": "Ti49", "amount": 0.037266306, "unit": "wo"},
            {"nuclide": "Ti50", "amount": 0.035681971, "unit": "wo"},
            {"nuclide": "B10", "amount": 0.061920613, "unit": "wo"},
            {"nuclide": "B11", "amount": 0.249238247, "unit": "wo"},
        ],
    },
    # 11) Tungsten carbide (WC)
    {
        "name": "Tungsten carbide (WC)",
        "density": 15.63,
        "nuclides": [
            {"nuclide": "W180", "amount": 0.00112641, "unit": "wo"},
            {"nuclide": "W182", "amount": 0.248748766, "unit": "wo"},
            {"nuclide": "W183", "amount": 0.134324334, "unit": "wo"},
            {"nuclide": "W184", "amount": 0.287609894, "unit": "wo"},
            {"nuclide": "W186", "amount": 0.266865186, "unit": "wo"},
            {"nuclide": "C12", "amount": 0.060669229, "unit": "wo"},
            {"nuclide": "C13", "amount": 0.000656182, "unit": "wo"},
        ],
    },
    # 12) Concrete (Portland)
    {
        "name": "Concrete (Portland)",
        "density": 2.3,
        "elements": [
            {"element": "H", "amount": 0.168753, "unit": "ao"},
            {"element": "C", "amount": 0.001416, "unit": "ao"},
            {"element": "O", "amount": 0.562526, "unit": "ao"},
            {"element": "Na", "amount": 0.011838, "unit": "ao"},
            {"element": "Mg", "amount": 0.0014, "unit": "ao"},
            {"element": "Al", "amount": 0.021354, "unit": "ao"},
            {"element": "Si", "amount": 0.204119, "unit": "ao"},
            {"element": "K", "amount": 0.005656, "unit": "ao"},
            {"element": "Ca", "amount": 0.018674, "unit": "ao"},
            {"element": "Fe", "amount": 0.004264, "unit": "ao"},
        ],
    },
    # 13) Lead (Pb)
    {
        "name": "Lead (Pb)",
        "density": 11.35,
        "elements": [{"element": "Pb", "amount": 1.000000, "unit": "wo"}],
    },
    # 14) Steel, Medium carbon
    {
        "name": "Steel, medium carbon",
        "density": 7.872,
        "elements": [
            {"element": "C", "amount": 0.022813, "unit": "ao"},
            {"element": "Mn", "amount": 0.008977, "unit": "ao"},
            {"element": "P", "amount": 0.000708, "unit": "ao"},
            {"element": "S", "amount": 0.000854, "unit": "ao"},
            {"element": "Fe", "amount": 0.966648, "unit": "ao"},
        ],
    },
    # 15) Light water
    {
        "name": "Light water (H2O)",
        "density": 0.997,
        "nuclides": [
            {"nuclide": "H1", "amount": 0.111872, "unit": "wo"},
            {"nuclide": "H2", "amount": 0.000026, "unit": "wo"},
            {"nuclide": "O16", "amount": 0.885692, "unit": "wo"},
            {"nuclide": "O17", "amount": 0.000359, "unit": "wo"},
            {"nuclide": "O18", "amount": 0.002048, "unit": "wo"},
        ],
    },
    # 16) Lithium Hydride
    {
        "name": "Lithium hydride (LiH)",
        "density": 0.82,
        "nuclides": [
            {"nuclide": "H1", "amount": 0.126802675, "unit": "wo"},
            {"nuclide": "H2", "amount": 0.000014584, "unit": "wo"},
            {"nuclide": "Li6", "amount": 0.06627457, "unit": "wo"},
            {"nuclide": "Li7", "amount": 0.806908171, "unit": "wo"},
        ],
    },
    # 17) Boron Carbide
    {
        "name": "Boron carbide (B4C)",
        "density": 2.52,
        "nuclides": [
            {"nuclide": "B10", "amount": 0.155743408, "unit": "wo"},
            {"nuclide": "B11", "amount": 0.626886781, "unit": "wo"},
            {"nuclide": "C12", "amount": 0.215043954, "unit": "wo"},
            {"nuclide": "C13", "amount": 0.002325857, "unit": "wo"},
        ],
    },
    # 18) Cadmium (Cd)
    {
        "name": "Cadmium (Cd)",
        "density": 8.65,
        "elements": [{"element": "Cd", "amount": 1.000000, "unit": "wo"}],
    },
    # 19) Gadolinium (Gd)
    {
        "name": "Gadolinium (Gd)",
        "density": 7.9004,
        "elements": [{"element": "Gd", "amount": 1.000000, "unit": "wo"}],
    },
    # 20) Indium (In)
    {
        "name": "Indium (In)",
        "density": 7.31,
        "elements": [{"element": "In", "amount": 1.000000, "unit": "wo"}],
    },
    # 21) Silver (Ag)
    {
        "name": "Silver (Ag)",
        "density": 10.5,
        "elements": [{"element": "Ag", "amount": 1.000000, "unit": "wo"}],
    },
    # 22) Steel, Boron Stainless
    {
        "name": "Steel, boron stainless",
        "density": 7.87,
        "elements": [
            {"element": "Cr", "amount": 0.196075, "unit": "ao"},
            {"element": "Ni", "amount": 0.118895, "unit": "ao"},
            {"element": "B", "amount": 0.056685, "unit": "ao"},
            {"element": "C", "amount": 0.002181, "unit": "ao"},
            {"element": "N", "amount": 0.000374, "unit": "ao"},
            {"element": "P", "amount": 0.000034, "unit": "ao"},
            {"element": "S", "amount": 0.000049, "unit": "ao"},
            {"element": "Co", "amount": 0.000267, "unit": "ao"},
            {"element": "Si", "amount": 0.012871, "unit": "ao"},
            {"element": "Mn", "amount": 0.018214, "unit": "ao"},
            {"element": "Fe", "amount": 0.594355, "unit": "ao"},
        ],
    },
    # 23) Beryllium (Be)
    {
        "name": "Beryllium (Be)",
        "density": 1.848,
        "elements": [{"element": "Be", "amount": 1.000000, "unit": "wo"}],
    },
    # 24) Tantalum (Ta)
    {
        "name": "Tantalum (Ta)",
        "density": 16.654,
        "elements": [{"element": "Ta", "amount": 1.000000, "unit": "wo"}],
    },
    # Add more 'inshield' material compositions here...
]



# Fixed (non-shielding-trade-study) materials
#**************************************************************
def _build_fixed_materials():
    """Recreates the plasma / blanket / magnet / structural materials.

    """
    # Plasma material
    material_plasma = openmc.Material(material_id=1, name="ITER_plasma")
    material_plasma.add_element("H", 1, "wo")
    material_plasma.set_density("g/cm3", 0.00001)

    # Tungsten (M20 in the reference MCNP model) - used for the blanket
    material_tungsten = openmc.Material(material_id=6, name="Blanket")
    material_tungsten.add_nuclide("W180", 0.001175, "wo")
    material_tungsten.add_nuclide("W182", 0.262270, "wo")
    material_tungsten.add_nuclide("W183", 0.142406, "wo")
    material_tungsten.add_nuclide("W184", 0.306582, "wo")
    material_tungsten.add_nuclide("W186", 0.287567, "wo")
    material_tungsten.set_density("g/cm3", 19.3)

    # Copper - central column magnet material
    material_copper = openmc.Material(material_id=3, name="magnet")
    material_copper.add_nuclide("Cu63", 0.684792, "wo")
    material_copper.add_nuclide("Cu65", 0.315208, "wo")
    material_copper.set_density("g/cm3", cu_den)

    # Stainless Steel 301 - tie bar
    material_stainless_steel = openmc.Material(material_id=4, name="bar")
    material_stainless_steel.add_nuclide("C12", 0.001502, "wo")
    material_stainless_steel.add_nuclide("Cr50", 0.007095, "wo")
    material_stainless_steel.add_nuclide("Cr52", 0.142289, "wo")
    material_stainless_steel.add_nuclide("Cr53", 0.016445, "wo")
    material_stainless_steel.add_nuclide("Cr54", 0.004171, "wo")
    material_stainless_steel.add_nuclide("Mn55", 0.020000, "wo")
    material_stainless_steel.add_nuclide("Fe54", 0.041692, "wo")
    material_stainless_steel.add_nuclide("Fe56", 0.678693, "wo")
    material_stainless_steel.add_nuclide("Fe57", 0.015954, "wo")
    material_stainless_steel.add_nuclide("Fe58", 0.002160, "wo")
    material_stainless_steel.add_nuclide("Ni58", 0.047038, "wo")
    material_stainless_steel.add_nuclide("Ni60", 0.018743, "wo")
    material_stainless_steel.add_nuclide("Ni61", 0.000828, "wo")
    material_stainless_steel.add_nuclide("Ni62", 0.002684, "wo")
    material_stainless_steel.add_nuclide("Ni64", 0.000706, "wo")
    material_stainless_steel.set_density("g/cm3", 8.0)

    return material_plasma, material_tungsten, material_copper, material_stainless_steel



(
    material_plasma,
    material_tungsten,
    material_copper,
    material_stainless_steel,
) = _build_fixed_materials()


def build_inshield_material(composition_index, material_id=None):
    """
        Builds a single 'inshield' openmc.Material from `compositions`.

   
    """
    composition = compositions[composition_index]
    if material_id is None:
        material_id = 10 + composition_index

    material_inshield = openmc.Material(material_id=material_id, name=name_tag)

    if "elements" in composition:
        for element in composition["elements"]:
            material_inshield.add_element(
                element["element"], element["amount"], element.get("unit", "ao")
            )

    if "nuclides" in composition:
        for nuclide in composition["nuclides"]:
            material_inshield.add_nuclide(
                nuclide["nuclide"], nuclide["amount"], nuclide["unit"]
            )

    material_inshield.set_density(density_unit, composition["density"])
    return material_inshield


def build_all_materials(composition_index):
    material_inshield = build_inshield_material(composition_index)
    return [
        material_plasma,
        material_tungsten,
        material_copper,
        material_stainless_steel,
        material_inshield,
    ]


def export_material_xml_files(output_dir="."):
    import os

    written = []
    for i in range(len(compositions)):
        materials_file = openmc.Materials(build_all_materials(i))
        out_path = os.path.join(output_dir, f"Newmaterial_file_{i + 1}.xml")
        materials_file.export_to_xml(out_path)
        written.append(out_path)
    return written


if __name__ == "__main__":
    # Allows `python materials.py` to regenerate all material XML files
    # without touching the notebook.
    paths = export_material_xml_files()
    print(f"Wrote {len(paths)} material XML files:")
    for p in paths:
        print(" -", p)
