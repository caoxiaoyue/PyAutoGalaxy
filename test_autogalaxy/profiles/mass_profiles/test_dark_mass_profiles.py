import os

from autoconf import conf
import autogalaxy as ag
import numpy as np
import pytest
from astropy import cosmology as cosmo
from autogalaxy.mock import mock

grid = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [2.0, 4.0]])


class TestAbstractNFW:
    def test__coord_function_f__from(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=3.0
        )

        # r > 1

        coord_f = truncated_nfw.coord_func_f(grid_radius=np.array([2.0, 3.0]))

        assert coord_f == pytest.approx(np.array([0.604599, 0.435209]), 1.0e-4)

        # r < 1

        coord_f = truncated_nfw.coord_func_f(grid_radius=np.array([0.5, 1.0 / 3.0]))

        assert coord_f == pytest.approx(1.52069, 1.86967, 1.0e-4)
        #
        # r == 1

        coord_f = truncated_nfw.coord_func_f(grid_radius=np.array([1.0, 1.0]))

        assert (coord_f == np.array([1.0, 1.0])).all()

    def test__coord_function_g__from(self):
        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=3.0
        )

        # r > 1

        coord_g = truncated_nfw.coord_func_g(grid_radius=np.array([2.0, 3.0]))

        assert coord_g == pytest.approx(np.array([0.13180, 0.070598]), 1.0e-4)

        # r < 1

        coord_g = truncated_nfw.coord_func_g(grid_radius=np.array([0.5, 1.0 / 3.0]))

        assert coord_g == pytest.approx(np.array([0.69425, 0.97838]), 1.0e-4)

        # r == 1

        coord_g = truncated_nfw.coord_func_g(grid_radius=np.array([1.0, 1.0]))

        assert coord_g == pytest.approx(
            np.real(np.array([1.0 / 3.0, 1.0 / 3.0])), 1.0e-4
        )

    def test__coord_function_h__from(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=3.0
        )

        coord_h = truncated_nfw.coord_func_h(grid_radius=np.array([0.5, 3.0]))

        assert coord_h == pytest.approx(np.array([0.134395, 0.840674]), 1.0e-4)

    def test__coord_function_k__from(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=2.0
        )

        coord_k = truncated_nfw.coord_func_k(grid_radius=np.array([2.0, 3.0]))

        assert coord_k == pytest.approx(np.array([-0.09983408, -0.06661738]), 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=4.0
        )

        coord_k = truncated_nfw.coord_func_k(grid_radius=np.array([2.0, 3.0]))

        assert coord_k == pytest.approx(np.array([-0.19869011, -0.1329414]), 1.0e-4)

    def test__coord_function_l__from(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=2.0
        )

        coord_l = truncated_nfw.coord_func_l(grid_radius=np.array([2.0, 2.0]))

        assert coord_l == pytest.approx(np.array([0.00080191, 0.00080191]), 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=3.0
        )

        coord_l = truncated_nfw.coord_func_l(grid_radius=np.array([2.0, 2.0]))

        assert coord_l == pytest.approx(np.array([0.00178711, 0.00178711]), 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=3.0
        )

        coord_l = truncated_nfw.coord_func_l(grid_radius=np.array([3.0, 3.0]))

        assert coord_l == pytest.approx(np.array([0.00044044, 0.00044044]), 1.0e-4)

    def test__coord_function_m__from(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=2.0
        )

        coord_m = truncated_nfw.coord_func_m(grid_radius=np.array([2.0, 2.0]))

        assert coord_m == pytest.approx(np.array([0.0398826, 0.0398826]), 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=3.0
        )

        coord_m = truncated_nfw.coord_func_m(grid_radius=np.array([2.0, 2.0]))

        assert coord_m == pytest.approx(np.array([0.06726646, 0.06726646]), 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=10.0, truncation_radius=3.0
        )

        coord_m = truncated_nfw.coord_func_m(grid_radius=np.array([3.0, 3.0]))

        assert coord_m == pytest.approx(np.array([0.06946888, 0.06946888]), 1.0e-4)

    def test__rho_at_scale_radius__unit_conversions(self):

        cosmology = mock.MockCosmology(
            arcsec_per_kpc=0.5, kpc_per_arcsec=2.0, critical_surface_density=2.0
        )

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        # When converting to kpc, the critical convergence is divided by kpc_per_arcsec**2.0 = 2.0**2.0
        # The scale radius also becomes scale_radius*kpc_per_arcsec = 2.0

        rho = nfw.rho_at_scale_radius_solar_mass_per_kpc3(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )
        assert rho == pytest.approx(0.5 / 2.0, 1e-3)

        cosmology = mock.MockCosmology(
            arcsec_per_kpc=0.25, kpc_per_arcsec=4.0, critical_surface_density=2.0
        )

        rho = nfw.rho_at_scale_radius_solar_mass_per_kpc3(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )
        assert rho == pytest.approx(0.5 / 4.0, 1e-3)

        cosmology = mock.MockCosmology(
            arcsec_per_kpc=0.25, kpc_per_arcsec=4.0, critical_surface_density=4.0
        )

        rho = nfw.rho_at_scale_radius_solar_mass_per_kpc3(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )
        assert rho == pytest.approx(0.25 / 4.0, 1e-3)

    def test__delta_concentration_value_in_default_units(self):
        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        cosmology = mock.MockCosmology(
            arcsec_per_kpc=1.0,
            kpc_per_arcsec=1.0,
            critical_surface_density=1.0,
            cosmic_average_density=1.0,
        )

        delta_concentration = nfw.delta_concentration(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )
        assert delta_concentration == pytest.approx(1.0, 1e-3)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=3.0, scale_radius=1.0)
        delta_concentration = nfw.delta_concentration(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )
        assert delta_concentration == pytest.approx(3.0, 1e-3)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=4.0)
        delta_concentration = nfw.delta_concentration(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )
        assert delta_concentration == pytest.approx(0.25, 1e-3)

    def test__solve_concentration(self):

        cosmology = mock.MockCosmology(
            arcsec_per_kpc=1.0,
            kpc_per_arcsec=1.0,
            critical_surface_density=1.0,
            cosmic_average_density=1.0,
        )

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        concentration = nfw.concentration(
            redshift_profile=0.5, redshift_source=1.0, cosmology=cosmology
        )

        assert concentration == pytest.approx(0.0074263, 1.0e-4)

    def test__radius_at_200__different_length_units_include_conversions(self):
        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        cosmology = mock.MockCosmology(arcsec_per_kpc=0.2, kpc_per_arcsec=5.0)

        concentration = nfw.concentration(
            cosmology=cosmology, redshift_profile=0.5, redshift_source=1.0
        )

        radius_200 = nfw.radius_at_200(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )

        assert radius_200 == concentration * 1.0

    def test__mass_at_200__unit_conversions_work(self):

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        cosmology = mock.MockCosmology(
            arcsec_per_kpc=1.0,
            kpc_per_arcsec=1.0,
            critical_surface_density=1.0,
            cosmic_average_density=1.0,
        )

        radius_at_200 = nfw.radius_at_200(
            redshift_object=0.5, redshift_source=1.0, cosmology=cosmology
        )

        mass_at_200 = nfw.mass_at_200_solar_masses(
            cosmology=cosmology, redshift_object=0.5, redshift_source=1.0
        )

        mass_calc = (
            200.0
            * ((4.0 / 3.0) * np.pi)
            * cosmology.cosmic_average_density
            * (radius_at_200 ** 3.0)
        )
        assert mass_at_200 == pytest.approx(mass_calc, 1.0e-5)

        # cosmology = mock.MockCosmology(arcsec_per_kpc=0.5, kpc_per_arcsec=2.0, critical_surface_density=2.0,
        #                           cosmic_average_density=1.0)
        #
        # radius_at_200 = nfw.radius_at_200_for_units(unit_length='arcsec', redshift_galaxy=0.5, redshift_source=1.0,
        #                                             cosmology=cosmology)
        #
        # mass_at_200 = nfw.mass_at_200(cosmology=cosmology, redshift_galaxy=0.5, redshift_source=1.0, unit_length='arcsec',
        #                               unit_mass='solMass')
        #
        # mass_calc = 200.0 * ((4.0 / 3.0) * np.pi) * cosmology.cosmic_average_density * (radius_at_200 ** 3.0)
        # assert mass_at_200 == pytest.approx(mass_calc, 1.0e-5)

    def test__values_of_quantities_for_real_cosmology(self):

        cosmology = cosmo.LambdaCDM(H0=70.0, Om0=0.3, Ode0=0.7)

        nfw = ag.mp.SphNFWTruncated(
            kappa_s=0.5, scale_radius=5.0, truncation_radius=10.0
        )

        rho = nfw.rho_at_scale_radius_solar_mass_per_kpc3(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )

        delta_concentration = nfw.delta_concentration(
            redshift_object=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="local",
            cosmology=cosmology,
        )

        concentration = nfw.concentration(
            redshift_profile=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="local",
            cosmology=cosmology,
        )

        radius_at_200 = nfw.radius_at_200(
            redshift_object=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="local",
            cosmology=cosmology,
        )

        mass_at_200 = nfw.mass_at_200_solar_masses(
            redshift_object=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="local",
            cosmology=cosmology,
        )

        mass_at_truncation_radius = nfw.mass_at_truncation_radius_solar_mass(
            redshift_profile=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="local",
            cosmology=cosmology,
        )

        assert rho == pytest.approx(29027857.01622403, 1.0e-4)
        assert delta_concentration == pytest.approx(213451.19421263796, 1.0e-4)
        assert concentration == pytest.approx(18.6605624462417, 1.0e-4)
        assert radius_at_200 == pytest.approx(93.302812, 1.0e-4)
        assert mass_at_200 == pytest.approx(27651532986258.375, 1.0e-4)
        assert mass_at_truncation_radius == pytest.approx(14877085957074.299, 1.0e-4)

        rho = nfw.rho_at_scale_radius_solar_mass_per_kpc3(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )

        delta_concentration = nfw.delta_concentration(
            redshift_object=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="profile",
            cosmology=cosmology,
        )

        concentration = nfw.concentration(
            redshift_profile=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="profile",
            cosmology=cosmology,
        )

        radius_at_200 = nfw.radius_at_200(
            redshift_object=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="profile",
            cosmology=cosmology,
        )

        mass_at_200 = nfw.mass_at_200_solar_masses(
            redshift_object=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="profile",
            cosmology=cosmology,
        )

        mass_at_truncation_radius = nfw.mass_at_truncation_radius_solar_mass(
            redshift_profile=0.6,
            redshift_source=2.5,
            redshift_of_cosmic_average_density="profile",
            cosmology=cosmology,
        )

        assert rho == pytest.approx(29027857.01622403, 1.0e-4)
        assert delta_concentration == pytest.approx(110665.28111397651, 1.0e-4)
        assert concentration == pytest.approx(14.401574489517804, 1.0e-4)
        assert radius_at_200 == pytest.approx(72.007872, 1.0e-4)
        assert mass_at_200 == pytest.approx(24516707575366.09, 1.0e-4)
        assert mass_at_truncation_radius == pytest.approx(13190486262169.797, 1.0e-4)


class TestNFWGeneralized:
    def test__deflections_via_integral_from(self):

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.0, 0.0), kappa_s=1.0, inner_slope=0.5, scale_radius=8.0
        )

        deflections = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.43501, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.37701, 1e-3)

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.3, 0.2), kappa_s=2.5, inner_slope=1.5, scale_radius=4.0
        )

        deflections = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(-9.31254, 1e-3)
        assert deflections[0, 1] == pytest.approx(-3.10418, 1e-3)

        gnfw = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0),
            kappa_s=1.0,
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.3, angle=100.0
            ),
            inner_slope=0.5,
            scale_radius=8.0,
        )
        deflections = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(0.26604, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.58988, 1e-3)

        gnfw = ag.mp.EllNFWGeneralized(
            centre=(0.3, 0.2),
            kappa_s=2.5,
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=100.0
            ),
            inner_slope=1.5,
            scale_radius=4.0,
        )
        deflections = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )
        assert deflections[0, 0] == pytest.approx(-5.99032, 1e-3)
        assert deflections[0, 1] == pytest.approx(-4.02541, 1e-3)

    def test__deflections_2d_via_mge_from(self):

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.0, 0.0), kappa_s=1.0, inner_slope=0.5, scale_radius=8.0
        )

        deflections_via_integral = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )
        deflections_via_mge = gnfw.deflections_2d_via_mge_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_mge, 1.0e-3)

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.3, 0.2), kappa_s=2.5, inner_slope=1.5, scale_radius=4.0
        )

        deflections_via_integral = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )
        deflections_via_mge = gnfw.deflections_2d_via_mge_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_mge, 1.0e-3)

        gnfw = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0),
            kappa_s=1.0,
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.3, angle=100.0
            ),
            inner_slope=0.5,
            scale_radius=8.0,
        )

        deflections_via_integral = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )
        deflections_via_mge = gnfw.deflections_2d_via_mge_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_mge, 1.0e-3)

        gnfw = ag.mp.EllNFWGeneralized(
            centre=(0.3, 0.2),
            kappa_s=2.5,
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=100.0
            ),
            inner_slope=1.5,
            scale_radius=4.0,
        )

        deflections_via_integral = gnfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )
        deflections_via_mge = gnfw.deflections_2d_via_mge_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_mge, 1.0e-3)

    def test__deflections_yx_2d_from(self):

        gnfw = ag.mp.EllNFWGeneralized()

        deflections = gnfw.deflections_yx_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_via_mge = gnfw.deflections_2d_via_mge_from(
            grid=np.array([[1.0, 0.0]])
        )

        assert (deflections == deflections_via_mge).all()

        gnfw = ag.mp.SphNFWGeneralized()

        deflections = gnfw.deflections_yx_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_via_mge = gnfw.deflections_2d_via_mge_from(
            grid=np.array([[1.0, 0.0]])
        )

        assert (deflections == deflections_via_mge).all()

    def test__convergence_2d_via_mge_from(self):

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.0, 0.0), kappa_s=1.0, inner_slope=1.5, scale_radius=1.0
        )

        convergence = gnfw.convergence_2d_via_mge_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.30840, 1e-2)

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.0, 0.0), kappa_s=2.0, inner_slope=1.5, scale_radius=1.0
        )

        convergence = gnfw.convergence_2d_via_mge_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.30840 * 2, 1e-2)

        gnfw = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0),
            kappa_s=1.0,
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=90.0
            ),
            inner_slope=1.5,
            scale_radius=1.0,
        )
        assert gnfw.convergence_2d_via_mge_from(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(0.30840, 1e-2)

        gnfw = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0),
            kappa_s=2.0,
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=90.0
            ),
            inner_slope=1.5,
            scale_radius=1.0,
        )
        assert gnfw.convergence_2d_via_mge_from(
            grid=np.array([[0.0, 1.0]])
        ) == pytest.approx(0.30840 * 2, 1e-2)

    def test__convergence_2d_from(self):

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.0, 0.0), kappa_s=1.0, inner_slope=1.5, scale_radius=1.0
        )

        convergence = gnfw.convergence_2d_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.30840, 1e-2)

    def test__potential_2d_from(self):

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.0, 0.0), kappa_s=1.0, inner_slope=0.5, scale_radius=8.0
        )

        potential = gnfw.potential_2d_from(grid=np.array([[0.1625, 0.1875]]))

        assert potential == pytest.approx(0.00920, 1e-3)

        gnfw = ag.mp.SphNFWGeneralized(
            centre=(0.0, 0.0), kappa_s=1.0, inner_slope=1.5, scale_radius=8.0
        )

        potential = gnfw.potential_2d_from(grid=np.array([[0.1625, 0.1875]]))

        assert potential == pytest.approx(0.17448, 1e-3)

        gnfw = ag.mp.EllNFWGeneralized(
            centre=(1.0, 1.0),
            kappa_s=5.0,
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=100.0
            ),
            inner_slope=1.0,
            scale_radius=10.0,
        )
        assert gnfw.potential_2d_from(grid=np.array([[2.0, 2.0]])) == pytest.approx(
            2.4718, 1e-4
        )

    def test__change_geometry(self):

        gnfw_0 = ag.mp.SphNFWGeneralized(centre=(0.0, 0.0))
        gnfw_1 = ag.mp.SphNFWGeneralized(centre=(1.0, 1.0))

        convergence_0 = gnfw_0.convergence_2d_from(grid=np.array([[1.0, 1.0]]))
        convergence_1 = gnfw_1.convergence_2d_from(grid=np.array([[0.0, 0.0]]))

        assert convergence_0 == convergence_1

        potential_0 = gnfw_0.potential_2d_from(grid=np.array([[1.0, 1.0]]))
        potential_1 = gnfw_1.potential_2d_from(grid=np.array([[0.0, 0.0]]))

        assert potential_0 == potential_1

        deflections_0 = gnfw_0.deflections_yx_2d_from(grid=np.array([[1.0, 1.0]]))
        deflections_1 = gnfw_1.deflections_yx_2d_from(grid=np.array([[0.0, 0.0]]))

        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-5)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-5)

        gnfw_0 = ag.mp.SphNFWGeneralized(centre=(0.0, 0.0))
        gnfw_1 = ag.mp.SphNFWGeneralized(centre=(0.0, 0.0))

        convergence_0 = gnfw_0.convergence_2d_from(grid=np.array([[1.0, 0.0]]))
        convergence_1 = gnfw_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence_0 == convergence_1

        potential_0 = gnfw_0.potential_2d_from(grid=np.array([[1.0, 0.0]]))
        potential_1 = gnfw_1.potential_2d_from(grid=np.array([[0.0, 1.0]]))

        assert potential_0 == potential_1

        deflections_0 = gnfw_0.deflections_yx_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = gnfw_1.deflections_yx_2d_from(grid=np.array([[0.0, 1.0]]))

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

        gnfw_0 = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        gnfw_1 = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        assert gnfw_0.convergence_2d_from(
            grid=np.array([[1.0, 0.0]])
        ) == gnfw_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        gnfw_0 = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        gnfw_1 = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )
        assert gnfw_0.potential_2d_from(
            grid=np.array([[1.0, 0.0]])
        ) == gnfw_1.potential_2d_from(grid=np.array([[0.0, 1.0]]))

        gnfw_0 = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.111111),
            kappa_s=1.0,
            inner_slope=1.5,
            scale_radius=1.0,
        )
        gnfw_1 = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, -0.111111),
            kappa_s=1.0,
            inner_slope=1.5,
            scale_radius=1.0,
        )
        deflections_0 = gnfw_0.deflections_yx_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = gnfw_1.deflections_yx_2d_from(grid=np.array([[0.0, 1.0]]))
        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

    def test__compare_to_nfw(self):

        nfw = ag.mp.EllNFW(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.111111),
            kappa_s=1.0,
            scale_radius=20.0,
        )
        gnfw = ag.mp.EllNFWGeneralized(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.111111),
            kappa_s=1.0,
            inner_slope=1.0,
            scale_radius=20.0,
        )

        assert nfw.deflections_yx_2d_from(grid) == pytest.approx(
            gnfw.deflections_yx_2d_from(grid), 1e-3
        )
        assert nfw.deflections_yx_2d_from(grid) == pytest.approx(
            gnfw.deflections_yx_2d_from(grid), 1e-3
        )

        assert nfw.potential_2d_from(grid) == pytest.approx(
            gnfw.potential_2d_from(grid), 1e-3
        )
        assert nfw.potential_2d_from(grid) == pytest.approx(
            gnfw.potential_2d_from(grid), 1e-3
        )

    def test__spherical_and_elliptical_match(self):

        elliptical = ag.mp.EllNFWGeneralized(
            centre=(0.1, 0.2),
            elliptical_comps=(0.0, 0.0),
            kappa_s=2.0,
            inner_slope=1.5,
            scale_radius=3.0,
        )
        spherical = ag.mp.SphNFWGeneralized(
            centre=(0.1, 0.2), kappa_s=2.0, inner_slope=1.5, scale_radius=3.0
        )

        assert elliptical.deflections_yx_2d_from(grid) == pytest.approx(
            spherical.deflections_yx_2d_from(grid), 1e-4
        )

        assert elliptical.convergence_2d_from(grid) == pytest.approx(
            spherical.convergence_2d_from(grid), 1e-4
        )
        assert elliptical.potential_2d_from(grid) == pytest.approx(
            spherical.potential_2d_from(grid), 1e-4
        )


class TestNFWTruncated:
    def test__deflections_yx_2d_from(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0, truncation_radius=2.0
        )

        # factor = (4.0 * kappa_s * scale_radius / (r / scale_radius))

        deflections = truncated_nfw.deflections_yx_2d_from(grid=np.array([[2.0, 0.0]]))

        factor = (4.0 * 1.0 * 1.0) / (2.0 / 1.0)
        assert deflections[0, 0] == pytest.approx(factor * 0.38209715, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(0.0, 1.0e-4)

        deflections = truncated_nfw.deflections_yx_2d_from(grid=np.array([[0.0, 2.0]]))

        assert deflections[0, 0] == pytest.approx(0.0, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(factor * 0.38209715, 1.0e-4)

        deflections = truncated_nfw.deflections_yx_2d_from(grid=np.array([[1.0, 1.0]]))

        factor = (4.0 * 1.0 * 1.0) / (np.sqrt(2) / 1.0)
        assert deflections[0, 0] == pytest.approx(
            (1.0 / np.sqrt(2)) * factor * 0.3125838, 1.0e-4
        )
        assert deflections[0, 1] == pytest.approx(
            (1.0 / np.sqrt(2)) * factor * 0.3125838, 1.0e-4
        )

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=2.0, scale_radius=1.0, truncation_radius=2.0
        )

        deflections = truncated_nfw.deflections_yx_2d_from(grid=np.array([[2.0, 0.0]]))

        factor = (4.0 * 2.0 * 1.0) / (2.0 / 1.0)
        assert deflections[0, 0] == pytest.approx(factor * 0.38209715, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(0.0, 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=1.0, scale_radius=4.0, truncation_radius=2.0
        )

        deflections = truncated_nfw.deflections_yx_2d_from(
            grid=ag.Grid2DIrregular([(2.0, 0.0)])
        )

        assert deflections[0, 0] == pytest.approx(2.1702661386, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(0.0, 1.0e-4)

    def test__convergence_2d_from(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0, truncation_radius=2.0
        )

        convergence = truncated_nfw.convergence_2d_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(2.0 * 0.046409642, 1.0e-4)

        convergence = truncated_nfw.convergence_2d_from(grid=np.array([[1.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 0.10549515, 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=3.0, scale_radius=1.0, truncation_radius=2.0
        )

        convergence = truncated_nfw.convergence_2d_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(6.0 * 0.046409642, 1.0e-4)

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=3.0, scale_radius=5.0, truncation_radius=2.0
        )

        convergence = truncated_nfw.convergence_2d_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(1.51047026, 1.0e-4)

    def test__mass_at_truncation_radius(self):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0, truncation_radius=1.0
        )

        cosmology = mock.MockCosmology(
            arcsec_per_kpc=1.0,
            kpc_per_arcsec=1.0,
            critical_surface_density=1.0,
            cosmic_average_density=1.0,
        )

        mass_at_truncation_radius = truncated_nfw.mass_at_truncation_radius_solar_mass(
            redshift_profile=0.5, redshift_source=1.0, cosmology=cosmology
        )

        assert mass_at_truncation_radius == pytest.approx(0.00009792581, 1.0e-5)

        # truncated_nfw = ag.mp.SphNFWTruncated(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0,
        #                                          truncation_radius=1.0)
        #
        # cosmology = mock.MockCosmology(arcsec_per_kpc=1.0, kpc_per_arcsec=1.0, critical_surface_density=2.0,
        #                           cosmic_average_density=3.0)
        #
        # mass_at_truncation_radius = truncated_nfw.mass_at_truncation_radius(redshift_galaxy=0.5, redshift_source=1.0,
        #     unit_length='arcsec', unit_mass='solMass', cosmology=cosmology)
        #
        # assert mass_at_truncation_radius == pytest.approx(0.00008789978, 1.0e-5)
        #
        # truncated_nfw = ag.mp.SphNFWTruncated(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=2.0,
        #                                          truncation_radius=1.0)
        #
        # mass_at_truncation_radius = truncated_nfw.mass_at_truncation_radius(redshift_galaxy=0.5, redshift_source=1.0,
        #     unit_length='arcsec', unit_mass='solMass', cosmology=cosmology)
        #
        # assert mass_at_truncation_radius == pytest.approx(0.0000418378, 1.0e-5)
        #
        # truncated_nfw = ag.mp.SphNFWTruncated(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=8.0,
        #                                          truncation_radius=4.0)
        #
        # mass_at_truncation_radius = truncated_nfw.mass_at_truncation_radius(redshift_galaxy=0.5, redshift_source=1.0,
        #     unit_length='arcsec', unit_mass='solMass', cosmology=cosmology)
        #
        # assert mass_at_truncation_radius == pytest.approx(0.0000421512, 1.0e-4)
        #
        # truncated_nfw = ag.mp.SphNFWTruncated(centre=(0.0, 0.0), kappa_s=2.0, scale_radius=8.0,
        #                                          truncation_radius=4.0)
        #
        # mass_at_truncation_radius = truncated_nfw.mass_at_truncation_radius(redshift_galaxy=0.5, redshift_source=1.0,
        #     unit_length='arcsec', unit_mass='solMass', cosmology=cosmology)
        #
        # assert mass_at_truncation_radius == pytest.approx(0.00033636625, 1.0e-4)

    def test__compare_nfw_and_truncated_nfw_with_large_truncation_radius(self,):

        truncated_nfw = ag.mp.SphNFWTruncated(
            centre=(0.0, 0.0), kappa_s=1.0, scale_radius=4.0, truncation_radius=50000.0
        )

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=4.0)

        truncated_nfw_convergence = truncated_nfw.convergence_2d_from(
            grid=np.array([[2.0, 2.0], [3.0, 1.0], [-1.0, -9.0]])
        )
        nfw_convergence = nfw.convergence_2d_from(
            grid=np.array([[2.0, 2.0], [3.0, 1.0], [-1.0, -9.0]])
        )

        assert truncated_nfw_convergence == pytest.approx(nfw_convergence, 1.0e-4)

        truncated_nfw_deflections = truncated_nfw.deflections_yx_2d_from(
            grid=np.array([[2.0, 2.0], [3.0, 1.0], [-1.0, -9.0]])
        )
        nfw_deflections = nfw.deflections_yx_2d_from(
            grid=np.array([[2.0, 2.0], [3.0, 1.0], [-1.0, -9.0]])
        )

        assert truncated_nfw_deflections == pytest.approx(nfw_deflections, 1.0e-4)


class TestNFW:
    def test__deflections_via_integral_from(self):
        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        deflections = nfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.56194, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.56194, 1e-3)

        nfw = ag.mp.SphNFW(centre=(0.3, 0.2), kappa_s=2.5, scale_radius=4.0)

        deflections = nfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(-2.08909, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.69636, 1e-3)

        nfw = ag.mp.EllNFW(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            kappa_s=1.0,
            scale_radius=1.0,
        )

        deflections = nfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.56194, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.56194, 1e-3)

        nfw = ag.mp.EllNFW(
            centre=(0.3, 0.2),
            elliptical_comps=(0.03669, 0.172614),
            kappa_s=2.5,
            scale_radius=4.0,
        )

        deflections = nfw.deflections_2d_via_integral_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(-2.59480, 1e-3)
        assert deflections[0, 1] == pytest.approx(-0.44204, 1e-3)

    def test__deflections_2d_via_cse_from(self):

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        deflections_via_integral = nfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1625, 0.1625]])
        )
        deflections_via_cse = nfw.deflections_2d_via_cse_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_cse, 1.0e-4)

        nfw = ag.mp.SphNFW(centre=(0.3, 0.2), kappa_s=2.5, scale_radius=4.0)

        deflections_via_integral = nfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1625, 0.1625]])
        )
        deflections_via_cse = nfw.deflections_2d_via_cse_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_cse, 1.0e-4)

        nfw = ag.mp.EllNFW(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            kappa_s=1.0,
            scale_radius=1.0,
        )

        deflections_via_integral = nfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1625, 0.1625]])
        )
        deflections_via_cse = nfw.deflections_2d_via_cse_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_cse, 1.0e-4)

        nfw = ag.mp.EllNFW(
            centre=(0.3, 0.2),
            elliptical_comps=(0.03669, 0.172614),
            kappa_s=2.5,
            scale_radius=4.0,
        )

        deflections_via_integral = nfw.deflections_2d_via_integral_from(
            grid=np.array([[0.1625, 0.1625]])
        )
        deflections_via_cse = nfw.deflections_2d_via_cse_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections_via_integral == pytest.approx(deflections_via_cse, 1.0e-4)

    def test__deflections_yx_2d_from(self):
        nfw = ag.mp.EllNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        deflections = nfw.deflections_yx_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_via_integral = nfw.deflections_2d_via_cse_from(
            grid=np.array([[1.0, 0.0]])
        )

        assert (deflections == deflections_via_integral).all()

    def test__convergence_2d_via_mge_from(self):

        # r = 2.0 (> 1.0)
        # F(r) = (1/(sqrt(3))*atan(sqrt(3)) = 0.60459978807
        # kappa(r) = 2 * kappa_s * (1 - 0.60459978807) / (4-1) = 0.263600141

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_via_mge_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.263600141, 1e-2)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_via_mge_from(grid=np.array([[0.5, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-2)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=2.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_via_mge_from(grid=np.array([[0.5, 0.0]]))

        assert convergence == pytest.approx(2.0 * 1.388511, 1e-2)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=2.0)

        convergence = nfw.convergence_2d_via_mge_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-2)

        nfw = ag.mp.EllNFW(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            kappa_s=1.0,
            scale_radius=1.0,
        )

        convergence = nfw.convergence_2d_via_mge_from(grid=np.array([[0.25, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-3)

    def test__convergence_2d_via_cse_from(self):

        # r = 2.0 (> 1.0)
        # F(r) = (1/(sqrt(3))*atan(sqrt(3)) = 0.60459978807
        # kappa(r) = 2 * kappa_s * (1 - 0.60459978807) / (4-1) = 0.263600141

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_via_cse_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.263600141, 1e-2)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_via_cse_from(grid=np.array([[0.5, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-2)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=2.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_via_cse_from(grid=np.array([[0.5, 0.0]]))

        assert convergence == pytest.approx(2.0 * 1.388511, 1e-2)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=2.0)

        convergence = nfw.convergence_2d_via_cse_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-2)

        nfw = ag.mp.EllNFW(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            kappa_s=1.0,
            scale_radius=1.0,
        )

        convergence = nfw.convergence_2d_via_cse_from(grid=np.array([[0.25, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-3)

    def test__convergence_2d_from(self):

        # r = 2.0 (> 1.0)
        # F(r) = (1/(sqrt(3))*atan(sqrt(3)) = 0.60459978807
        # kappa(r) = 2 * kappa_s * (1 - 0.60459978807) / (4-1) = 0.263600141

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_from(grid=np.array([[2.0, 0.0]]))

        assert convergence == pytest.approx(0.263600141, 1e-3)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_from(grid=np.array([[0.5, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-3)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=2.0, scale_radius=1.0)

        convergence = nfw.convergence_2d_from(grid=np.array([[0.5, 0.0]]))

        assert convergence == pytest.approx(2.0 * 1.388511, 1e-3)

        nfw = ag.mp.SphNFW(centre=(0.0, 0.0), kappa_s=1.0, scale_radius=2.0)

        convergence = nfw.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-3)

        nfw = ag.mp.EllNFW(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            kappa_s=1.0,
            scale_radius=1.0,
        )

        convergence = nfw.convergence_2d_from(grid=np.array([[0.25, 0.0]]))

        assert convergence == pytest.approx(1.388511, 1e-3)

    def test__potential_2d_from(self):

        nfw = ag.mp.SphNFW(centre=(0.3, 0.2), kappa_s=2.5, scale_radius=4.0)

        potential = nfw.potential_2d_from(grid=np.array([[0.1875, 0.1625]]))

        assert potential == pytest.approx(0.03702, 1e-3)

        nfw = ag.mp.SphNFW(centre=(0.3, 0.2), kappa_s=2.5, scale_radius=4.0)

        potential = nfw.potential_2d_from(grid=np.array([[0.1875, 0.1625]]))

        assert potential == pytest.approx(0.03702, 1e-3)

        nfw = ag.mp.EllNFW(
            centre=(0.3, 0.2),
            elliptical_comps=(0.03669, 0.172614),
            kappa_s=2.5,
            scale_radius=4.0,
        )

        potential = nfw.potential_2d_from(grid=np.array([[0.1625, 0.1625]]))

        assert potential == pytest.approx(0.05380, 1e-3)

    def test__spherical_and_elliptical_are_same(self):

        nfw_spherical = ag.mp.SphNFW(centre=(0.3, 0.2), kappa_s=2.5, scale_radius=4.0)
        nfw_elliptical = ag.mp.EllNFW(
            centre=(0.3, 0.2),
            elliptical_comps=(0.0, 0.0),
            kappa_s=2.5,
            scale_radius=4.0,
        )

        potential_spherical = nfw_spherical.potential_2d_from(
            grid=np.array([[0.1875, 0.1625]])
        )
        potential_elliptical = nfw_elliptical.potential_2d_from(
            grid=np.array([[0.1875, 0.1625]])
        )

        assert potential_spherical == pytest.approx(potential_elliptical, 1e-3)

        potential_spherical = nfw_spherical.potential_2d_from(
            grid=np.array([[50.0, 50.0]])
        )
        potential_elliptical = nfw_elliptical.potential_2d_from(
            grid=np.array([[50.0, 50.0]])
        )

        assert potential_spherical == pytest.approx(potential_elliptical, 1e-3)

        potential_spherical = nfw_spherical.potential_2d_from(
            grid=np.array([[-50.0, -50.0]])
        )
        potential_elliptical = nfw_elliptical.potential_2d_from(
            grid=np.array([[-50.0, -50.0]])
        )

        assert potential_spherical == pytest.approx(potential_elliptical, 1e-3)


class TestNFWTruncatedMCRDuffy:
    def test__mass_and_concentration_consistent_with_normal_truncated_nfw(self):

        cosmology = cosmo.FlatLambdaCDM(H0=70.0, Om0=0.3)

        truncated_nfw_mass = ag.mp.SphNFWTruncatedMCRDuffy(
            centre=(1.0, 2.0),
            mass_at_200=1.0e9,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        mass_at_200_via_mass = truncated_nfw_mass.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_mass = truncated_nfw_mass.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        truncated_nfw_kappa_s = ag.mp.SphNFWTruncated(
            centre=(1.0, 2.0),
            kappa_s=truncated_nfw_mass.kappa_s,
            scale_radius=truncated_nfw_mass.scale_radius,
            truncation_radius=truncated_nfw_mass.truncation_radius,
        )

        mass_at_200_via_kappa_s = truncated_nfw_kappa_s.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_kappa_s = truncated_nfw_kappa_s.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert mass_at_200_via_kappa_s == mass_at_200_via_mass
        assert concentration_via_kappa_s == concentration_via_mass

        assert isinstance(truncated_nfw_mass.kappa_s, float)

        assert truncated_nfw_mass.centre == (1.0, 2.0)

        assert truncated_nfw_mass.axis_ratio == 1.0
        assert isinstance(truncated_nfw_mass.axis_ratio, float)

        assert truncated_nfw_mass.angle == 0.0
        assert isinstance(truncated_nfw_mass.angle, float)

        assert truncated_nfw_mass.inner_slope == 1.0
        assert isinstance(truncated_nfw_mass.inner_slope, float)

        assert truncated_nfw_mass.scale_radius == pytest.approx(0.273382, 1.0e-4)


class TestNFWTruncatedMCRLludlow:
    def test__mass_and_concentration_consistent_with_normal_truncated_nfw__scatter_0(
        self
    ):

        cosmology = cosmo.FlatLambdaCDM(H0=70.0, Om0=0.3)

        truncated_nfw_mass = ag.mp.SphNFWTruncatedMCRLudlow(
            centre=(1.0, 2.0),
            mass_at_200=1.0e9,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        mass_at_200_via_mass = truncated_nfw_mass.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_mass = truncated_nfw_mass.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        truncated_nfw_kappa_s = ag.mp.SphNFWTruncated(
            centre=(1.0, 2.0),
            kappa_s=truncated_nfw_mass.kappa_s,
            scale_radius=truncated_nfw_mass.scale_radius,
            truncation_radius=truncated_nfw_mass.truncation_radius,
        )

        mass_at_200_via_kappa_s = truncated_nfw_kappa_s.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_kappa_s = truncated_nfw_kappa_s.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert mass_at_200_via_kappa_s == mass_at_200_via_mass
        assert concentration_via_kappa_s == concentration_via_mass

        assert isinstance(truncated_nfw_mass.kappa_s, float)

        assert truncated_nfw_mass.centre == (1.0, 2.0)

        assert truncated_nfw_mass.axis_ratio == 1.0
        assert isinstance(truncated_nfw_mass.axis_ratio, float)

        assert truncated_nfw_mass.angle == 0.0
        assert isinstance(truncated_nfw_mass.angle, float)

        assert truncated_nfw_mass.inner_slope == 1.0
        assert isinstance(truncated_nfw_mass.inner_slope, float)

        assert truncated_nfw_mass.scale_radius == pytest.approx(0.21164, 1.0e-4)
        assert truncated_nfw_mass.truncation_radius == pytest.approx(33.7134116, 1.0e-4)

    def test__scatter_is_nonzero(self):

        truncated_nfw_mass = ag.mp.SphNFWTruncatedMCRScatterLudlow(
            centre=(1.0, 2.0),
            mass_at_200=1.0e9,
            scatter_sigma=1.0,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert truncated_nfw_mass.scale_radius == pytest.approx(0.14983, 1.0e-4)
        assert truncated_nfw_mass.truncation_radius == pytest.approx(33.7134116, 1.0e-4)

        truncated_nfw_mass = ag.mp.SphNFWTruncatedMCRScatterLudlow(
            centre=(1.0, 2.0),
            mass_at_200=1.0e9,
            scatter_sigma=-1.0,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert truncated_nfw_mass.scale_radius == pytest.approx(0.29895, 1.0e-4)
        assert truncated_nfw_mass.truncation_radius == pytest.approx(33.7134116, 1.0e-4)


class TestNFWMCRDuffy:
    def test__mass_and_concentration_consistent_with_normal_nfw(self):

        cosmology = cosmo.FlatLambdaCDM(H0=70.0, Om0=0.3)

        nfw_mass = ag.mp.SphNFWMCRDuffy(
            centre=(1.0, 2.0),
            mass_at_200=1.0e9,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        mass_at_200_via_mass = nfw_mass.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_mass = nfw_mass.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        nfw_kappa_s = ag.mp.SphNFW(
            centre=(1.0, 2.0),
            kappa_s=nfw_mass.kappa_s,
            scale_radius=nfw_mass.scale_radius,
        )

        mass_at_200_via_kappa_s = nfw_kappa_s.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_kappa_s = nfw_kappa_s.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert mass_at_200_via_kappa_s == mass_at_200_via_mass
        assert concentration_via_kappa_s == concentration_via_mass

        assert isinstance(nfw_mass.kappa_s, float)

        assert nfw_mass.centre == (1.0, 2.0)

        assert nfw_mass.axis_ratio == 1.0
        assert isinstance(nfw_mass.axis_ratio, float)

        assert nfw_mass.angle == 0.0
        assert isinstance(nfw_mass.angle, float)

        assert nfw_mass.inner_slope == 1.0
        assert isinstance(nfw_mass.inner_slope, float)

        assert nfw_mass.scale_radius == pytest.approx(0.273382, 1.0e-4)


class TestNFWMCRLudlow:
    def test__mass_and_concentration_consistent_with_normal_nfw__scatter_0(self):

        cosmology = cosmo.FlatLambdaCDM(H0=70.0, Om0=0.3)

        nfw_mass = ag.mp.SphNFWMCRLudlow(
            centre=(1.0, 2.0),
            mass_at_200=1.0e9,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        mass_at_200_via_mass = nfw_mass.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_mass = nfw_mass.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        nfw_kappa_s = ag.mp.SphNFW(
            centre=(1.0, 2.0),
            kappa_s=nfw_mass.kappa_s,
            scale_radius=nfw_mass.scale_radius,
        )

        mass_at_200_via_kappa_s = nfw_kappa_s.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_kappa_s = nfw_kappa_s.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert mass_at_200_via_kappa_s == mass_at_200_via_mass
        assert concentration_via_kappa_s == concentration_via_mass

        assert isinstance(nfw_mass.kappa_s, float)

        assert nfw_mass.centre == (1.0, 2.0)

        assert nfw_mass.axis_ratio == 1.0
        assert isinstance(nfw_mass.axis_ratio, float)

        assert nfw_mass.angle == 0.0
        assert isinstance(nfw_mass.angle, float)

        assert nfw_mass.inner_slope == 1.0
        assert isinstance(nfw_mass.inner_slope, float)

        assert nfw_mass.scale_radius == pytest.approx(0.21164, 1.0e-4)

        deflections_ludlow = nfw_mass.deflections_yx_2d_from(grid=grid)
        deflections = nfw_kappa_s.deflections_yx_2d_from(grid=grid)

        assert (deflections_ludlow == deflections).all()

    def test__same_as_above_but_elliptical(self):

        cosmology = cosmo.FlatLambdaCDM(H0=70.0, Om0=0.3)

        nfw_mass = ag.mp.EllNFWMCRLudlow(
            centre=(1.0, 2.0),
            elliptical_comps=(0.1, 0.2),
            mass_at_200=1.0e9,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        mass_at_200_via_mass = nfw_mass.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_mass = nfw_mass.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        nfw_kappa_s = ag.mp.EllNFW(
            centre=(1.0, 2.0),
            elliptical_comps=(0.1, 0.2),
            kappa_s=nfw_mass.kappa_s,
            scale_radius=nfw_mass.scale_radius,
        )

        mass_at_200_via_kappa_s = nfw_kappa_s.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_kappa_s = nfw_kappa_s.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert mass_at_200_via_kappa_s == mass_at_200_via_mass
        assert concentration_via_kappa_s == concentration_via_mass

        assert isinstance(nfw_mass.kappa_s, float)

        assert nfw_mass.centre == (1.0, 2.0)

        axis_ratio, angle = ag.convert.axis_ratio_and_angle_from(
            elliptical_comps=(0.1, 0.2)
        )

        assert nfw_mass.axis_ratio == axis_ratio
        assert isinstance(nfw_mass.axis_ratio, float)

        assert nfw_mass.angle == angle
        assert isinstance(nfw_mass.angle, float)

        assert nfw_mass.inner_slope == 1.0
        assert isinstance(nfw_mass.inner_slope, float)

        assert nfw_mass.scale_radius == pytest.approx(0.21164, 1.0e-4)

        deflections_ludlow = nfw_mass.deflections_yx_2d_from(grid=grid)
        deflections = nfw_kappa_s.deflections_yx_2d_from(grid=grid)

        assert (deflections_ludlow == deflections).all()

    def test__same_as_above_but_generalized_elliptical(self):

        cosmology = cosmo.FlatLambdaCDM(H0=70.0, Om0=0.3)

        nfw_mass = ag.mp.EllNFWGeneralizedMCRLudlow(
            centre=(1.0, 2.0),
            elliptical_comps=(0.1, 0.2),
            mass_at_200=1.0e9,
            inner_slope=2.0,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        mass_at_200_via_mass = nfw_mass.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_mass = nfw_mass.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        nfw_kappa_s = ag.mp.EllNFWGeneralized(
            centre=(1.0, 2.0),
            elliptical_comps=(0.1, 0.2),
            kappa_s=nfw_mass.kappa_s,
            scale_radius=nfw_mass.scale_radius,
            inner_slope=2.0,
        )

        mass_at_200_via_kappa_s = nfw_kappa_s.mass_at_200_solar_masses(
            redshift_object=0.6, redshift_source=2.5, cosmology=cosmology
        )
        concentration_via_kappa_s = nfw_kappa_s.concentration(
            redshift_profile=0.6, redshift_source=2.5, cosmology=cosmology
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert mass_at_200_via_kappa_s == mass_at_200_via_mass
        assert concentration_via_kappa_s == concentration_via_mass

        assert isinstance(nfw_mass.kappa_s, float)

        assert nfw_mass.centre == (1.0, 2.0)

        axis_ratio, angle = ag.convert.axis_ratio_and_angle_from(
            elliptical_comps=(0.1, 0.2)
        )

        assert nfw_mass.axis_ratio == axis_ratio
        assert isinstance(nfw_mass.axis_ratio, float)

        assert nfw_mass.angle == angle
        assert isinstance(nfw_mass.angle, float)

        assert nfw_mass.inner_slope == 2.0
        assert isinstance(nfw_mass.inner_slope, float)

        assert nfw_mass.scale_radius == pytest.approx(0.21164, 1.0e-4)

        deflections_ludlow = nfw_mass.deflections_yx_2d_from(grid=grid)
        deflections = nfw_kappa_s.deflections_yx_2d_from(grid=grid)

        assert (deflections_ludlow == deflections).all()

    def test__scatter_is_nonzero(self):

        nfw = ag.mp.SphNFWMCRScatterLudlow(
            mass_at_200=1.0e9,
            scatter_sigma=1.0,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert nfw.scale_radius == pytest.approx(0.14983, 1.0e-4)

        nfw = ag.mp.SphNFWMCRScatterLudlow(
            mass_at_200=1.0e9,
            scatter_sigma=-1.0,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        # We uare using the SphNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert nfw.scale_radius == pytest.approx(0.29895, 1.0e-4)

        nfw_ell = ag.mp.EllNFWMCRScatterLudlow(
            elliptical_comps=(0.5, 0.5),
            mass_at_200=1.0e9,
            scatter_sigma=1.0,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        # We uare using the EllNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert nfw_ell.elliptical_comps == (0.5, 0.5)
        assert nfw_ell.scale_radius == pytest.approx(0.14983, 1.0e-4)

        nfw_ell = ag.mp.EllNFWMCRScatterLudlow(
            elliptical_comps=(0.5, 0.5),
            mass_at_200=1.0e9,
            scatter_sigma=-1.0,
            redshift_object=0.6,
            redshift_source=2.5,
        )

        # We uare using the EllNFWTruncated to check the mass gives a conosistnt kappa_s, given certain radii.

        assert nfw_ell.elliptical_comps == (0.5, 0.5)
        assert nfw_ell.scale_radius == pytest.approx(0.29895, 1.0e-4)

        deflections_sph = nfw.deflections_yx_2d_from(grid=grid)
        deflections_ell = nfw_ell.deflections_yx_2d_from(grid=grid)

        assert deflections_sph[0] != pytest.approx(deflections_ell[0], 1.0e-4)
