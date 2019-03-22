.. _standard-parameters:

Standard parameters
===================

In OpenSCM a ':ref:`parameter <parameter-hierarchy>`' is any named input or output variable of a mode, e.g. |CO2| emissions, equilibrium climate sensitivity, aerosol forcing scaling.
As described :ref:`here <parameter-hierarchy>`, parameters are given in a hierarchy, e.g. ``Emissions`` -> ``CO2`` -> ``Industrial``.

Simple climate models come in many different shapes and forms hence we do not expect them to all be able to do everything.
However, to be included in OpenSCM they should make sure their parameters fit into these standard parameters as far as possible to ensure models can be interchanged easily.
Of course, also model-specific parameters are possible (see also :ref:`writing-adapters`).


Conventions
-----------

In the following, 'pre-industrial' refers to an unperturbed state of the climate.
Individual adapters can translate this into whatever year they need to for their model, but they should do such translations with this definition in mind.

'Reference period' refers to the period a given variable is reported relative to the mean of.
For example, 'surface temperature relative to a 1961-1990 reference period' refers to surface temperatures relative to the mean of the period 1961-1990.
Adapters can report variables without reference periods if these are not used internally by the models.
However, if the model uses an internal reference period then this should be indicated in the reported variable names by appending ``(rel. to XXXX-YYYY)`` to the variable name.
Hence, 'surface temperature relative to a 1961-1990 reference period' would become ``Surface Temperature (rel. to 1961-1990)``.
[TODO: discuss with other authors how we want this to play out]


Aggregation
-----------

Parameters in OpenSCM come as part of a hierarchy, in the following separated by the ``|`` character.
For example, ``Emissions|CO2|Energy``.
``Emissions|CO2|Energy`` is emissions of |CO2| from the energy sub-sector (whatever 'energy' happens to mean in this context).
As far as it makes sense, parameters that are higher in the hierarchy (e.g. ``Emissions|CO2`` is 'higher' than ``Emissions|CO2|Energy``) are the sum of all the variables which are one level below them in the hierarchy.
For example, for ``Emissions|CO2|Energy``, ``Emissions|CO2|Transport`` and ``Emissions|CO2|Agriculture`` given, ``Emissions|CO2`` would be the sum of these.


Standards
---------

Standard parameters
*******************

Below we provide a list of the OpenSCM standard parameters adapters must adhere to as far as a specific variable concerns them.
Alongside we give the type of unit that the parameter should be given in and how it should be expected by adapters.
Conversion between particular units is done automatically if possible.

In the following, ``<GAS>`` can be one of the standard :ref:`gases`.

.. csv-table:: Standard parameters
    :header: "Parameter name 0", "Parameter name 1", "Parameter name 2", "Unit type", "Note"

    ``Emissions``, ``<GAS>``,, "mass <GAS> / time"
    ``Atmospheric Concentrations``, ``<GAS>``,, "concentration (e.g. parts per X)", "Aggregation possible, but does not always make sense"
    ``Pool``, ``<GAS>``,, "mass <GAS>"
    ``Radiative Forcing``,,, "power / area", "Aggregation gives total forcing, but be carful of double reporting, e.g. providing ``Radiative Forcing|Aerosols|Direct Effect`` and ``Radiative Forcing|Aerosols|NOx``"
    ``Radiative Forcing``, ``<GAS>``
    ``Radiative Forcing``, ``Aerosols``
    ``Radiative Forcing``, ``Aerosols``, ``Direct Effect``
    ``Radiative Forcing``, ``Aerosols``, ``Indirect Effect``
    ``Radiative Forcing``, ``Aerosols``, ``SOx``
    ``Radiative Forcing``, ``Aerosols``, ``NOx``
    ``Radiative Forcing``, ``Aerosols``, ``OC``
    ``Radiative Forcing``, ``Aerosols``, ``BC``
    ``Radiative Forcing``, ``Land-use Change``
    ``Radiative Forcing``, ``Black Carbon on Snow``
    ``Radiative Forcing``, ``Volcanic``
    ``Radiative Forcing``, ``Solar``
    ``Radiative Forcing``, ``External``
    ``X to Y Flux``,,, "mass / time", "See :ref:`material_fluxes`"
    ``Surface Temperature``,,, "temperature", "Surface air temperature i.e. ``tas``"
    ``Ocean Temperature``,,, "temperature", "Surface ocean temperature i.e. ``tos``"
    ``Ocean Heat Content``,,, "energy"
    ``Sea Level Rise``,,, "length"
    ``Equilibrium Climate Sensitivity``,,, "temperature"
    ``Transient Climate Response``,,, "temperature"
    ``f2xco2``,,, "power / area", "Radiative forcing due to a doubling of atmospheric |CO2| concentrations from pre-industrial level"

.. _gases:

Gases
*****

.. csv-table:: Gases
    :header: "Name", "Description"

    ``CO2``, Carbon
    ``CH4``, Methane
    ``N2O``, Nitrous oxide
    ``SOx``, Sulfur oxide
    ``CO``, Carbon monoxide
    ``NMVOC``, Volatile organic compound
    ``NOx``, Nitrogen oxide
    ``BC``, Black carbon
    ``OC``, Organic carbon
    ``NH3``, NH3
    ``NF3``, NF3
    ``CF4``, CF4
    ``C2F6``, C2F6
    ``C3F8``, C3F8
    ``cC4F8``, cC4F8
    ``C4F10``, C4F10
    ``C5F12``, C5F12
    ``C6F14``, C6F14
    ``C7F16``, C7F16
    ``C8F18``, C8F18
    ``CCl4``, CCl4
    ``CHCl3``, CHCl3
    ``CH2Cl2``, CH2Cl2
    ``CH3CCl3``, CH3CCl3
    ``CH3Cl``, CH3Cl
    ``CH3Br``, CH3Br
    ``HFC23``, HFC23
    ``HFC32``, HFC32
    ``HFC4310``, HFC4310
    ``HFC125``, HFC125
    ``HFC134a``, HFC134a
    ``HFC143a``, HFC143a
    ``HFC152a``, HFC152a
    ``HFC227ea``, HFC227ea
    ``HFC236fa``, HFC236fa
    ``HFC245fa``, HFC245fa
    ``HFC365mfc``, HFC365mfc
    ``CFC11``, CFC11
    ``CFC12``, CFC12
    ``CFC113``, CFC113
    ``CFC114``, CFC114
    ``CFC115``, CFC115
    ``HCFC22``, HCFC22
    ``HCFC141b``, HCFC141b
    ``HCFC142b``, HCFC142b
    ``SF6``, SF6
    ``SO2F2``, SO2F2
    ``Halon1202``, Halon1202
    ``Halon1211``, Halon1211
    ``Halon1301``, Halon1301
    ``Halon2402``, Halon2402

.. _material_fluxes:

Material Fluxes
***************

These variables can be used to store the flux of material within the model.
They should be of the form ``X to Y Flux`` where the material is flowing from ``X`` into ``Y`` (and hence negative values represent flows from ``Y`` into ``X``):

- ``Land to Air Flux|CO2|Permafrost`` (mass carbon / time) - land to air flux of |CO2| from permafrost
- ``Land to Air Flux|CH4|Permafrost`` (mass methane / time)


Standard regions
----------------

Similarly to variables, regions are also given in a hierarchy.
Regions which are higher in the hierarchy are the sum of all the regions which are one level below them in the hierarchy (be careful of this when looking at e.g. |CO2| concentration data at a regional level).

.. csv-table:: Gases
    :header: "Name 0", "Name 1", "Name 2, "Description"

    ``World``
    ``World``, ``Northern Hemisphere``
    ``World``, ``Northern Hemisphere``, ``Ocean``
    ``World``, ``Northern Hemisphere``, ``Land``
    ``World``, ``Southern Hemisphere``
    ``World``, ``Southern Hemisphere``, ``Ocean``
    ``World``, ``Southern Hemisphere``, ``Land``
    ``World``, ``Ocean``
    ``World``, ``Land``
    ``World``, ``R5ASIA``
    ``World``, ``R5REF``
    ``World``, ``R5MAF``
    ``World``, ``R5OECD``
    ``World``, ``R5LAM``
    ``World``, ``R5.2ASIA``
    ``World``, ``R5.2REF``
    ``World``, ``R5.2MAF``
    ``World``, ``R5.2OECD``
    ``World``, ``R5.2LAM``
    ``World``, ``Bunkers``
