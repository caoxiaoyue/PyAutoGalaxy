from __future__ import division, print_function

import numpy as np
import pytest

import autogalaxy as ag

grid = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [2.0, 4.0]])


def test__blurred_image_2d_via_psf_from(
    sub_grid_2d_7x7, blurring_grid_2d_7x7, psf_3x3, convolver_7x7
):

    lp = ag.lp.EllSersic(intensity=1.0)
    operate_lp = ag.OperateImage.from_light_obj(light_obj=lp)

    lp_blurred_image_2d = operate_lp.blurred_image_2d_via_psf_from(
        grid=sub_grid_2d_7x7, blurring_grid=blurring_grid_2d_7x7, psf=psf_3x3
    )

    image_2d = lp.image_2d_from(grid=sub_grid_2d_7x7)
    blurring_image_2d = lp.image_2d_from(grid=blurring_grid_2d_7x7)

    blurred_image_2d = convolver_7x7.convolve_image(
        image=image_2d.binned, blurring_image=blurring_image_2d.binned
    )

    assert blurred_image_2d.slim == pytest.approx(lp_blurred_image_2d.slim, 1.0e-4)
    assert blurred_image_2d.native == pytest.approx(lp_blurred_image_2d.native, 1.0e-4)


def test__blurred_image_2d_list_via_psf_from(
    sub_grid_2d_7x7, blurring_grid_2d_7x7, psf_3x3
):

    lp_0 = ag.lp.EllSersic(intensity=1.0)
    lp_1 = ag.lp.EllSersic(intensity=2.0)

    lp_0_operate_image = ag.OperateImage.from_light_obj(light_obj=lp_0)
    lp_1_operate_image = ag.OperateImage.from_light_obj(light_obj=lp_1)

    lp_0_blurred_image_2d = lp_0_operate_image.blurred_image_2d_via_psf_from(
        grid=sub_grid_2d_7x7, blurring_grid=blurring_grid_2d_7x7, psf=psf_3x3
    )

    lp_1_blurred_image_2d = lp_1_operate_image.blurred_image_2d_via_psf_from(
        grid=sub_grid_2d_7x7, blurring_grid=blurring_grid_2d_7x7, psf=psf_3x3
    )

    gal = ag.Galaxy(redshift=0.5, lp_0=lp_0, lp_1=lp_1)

    gal_operate_image = ag.OperateImage.from_light_obj(light_obj=gal)

    blurred_image_2d_list = gal_operate_image.blurred_image_2d_list_via_psf_from(
        grid=sub_grid_2d_7x7, blurring_grid=blurring_grid_2d_7x7, psf=psf_3x3
    )

    assert lp_0_blurred_image_2d.shape_slim == 9
    assert blurred_image_2d_list[0].slim == pytest.approx(
        lp_0_blurred_image_2d.slim, 1.0e-4
    )
    assert lp_1_blurred_image_2d.shape_slim == 9
    assert blurred_image_2d_list[1].slim == pytest.approx(
        lp_1_blurred_image_2d.slim, 1.0e-4
    )

    assert blurred_image_2d_list[0].native == pytest.approx(
        lp_0_blurred_image_2d.native, 1.0e-4
    )
    assert blurred_image_2d_list[1].native == pytest.approx(
        lp_1_blurred_image_2d.native, 1.0e-4
    )


def test__blurred_image_2d_via_convolver_from(
    sub_grid_2d_7x7, blurring_grid_2d_7x7, convolver_7x7
):
    lp = ag.lp.EllSersic(intensity=1.0)
    operate_lp = ag.OperateImage.from_light_obj(light_obj=lp)

    lp_blurred_image_2d = operate_lp.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    image_2d = lp.image_2d_from(grid=sub_grid_2d_7x7)
    blurring_image_2d = lp.image_2d_from(grid=blurring_grid_2d_7x7)

    blurred_image_2d = convolver_7x7.convolve_image(
        image=image_2d.binned, blurring_image=blurring_image_2d.binned
    )

    assert blurred_image_2d.slim == pytest.approx(lp_blurred_image_2d.slim, 1.0e-4)
    assert blurred_image_2d.native == pytest.approx(lp_blurred_image_2d.native, 1.0e-4)


def test__blurred_image_2d_list_via_convolver_from(
    sub_grid_2d_7x7, blurring_grid_2d_7x7, convolver_7x7
):

    lp_0 = ag.lp.EllSersic(intensity=1.0)
    lp_1 = ag.lp.EllSersic(intensity=2.0)

    lp_0_operate_image = ag.OperateImage.from_light_obj(light_obj=lp_0)
    lp_1_operate_image = ag.OperateImage.from_light_obj(light_obj=lp_1)

    lp_0_blurred_image_2d = lp_0_operate_image.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )
    lp_1_blurred_image_2d = lp_1_operate_image.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    gal = ag.Galaxy(redshift=0.5, lp_0=lp_0, lp_1=lp_1)

    gal_operate_image = ag.OperateImage.from_light_obj(light_obj=gal)

    blurred_image_2d_list = gal_operate_image.blurred_image_2d_list_via_convolver_from(
        grid=sub_grid_2d_7x7,
        blurring_grid=blurring_grid_2d_7x7,
        convolver=convolver_7x7,
    )

    assert lp_0_blurred_image_2d.shape_slim == 9
    assert blurred_image_2d_list[0].slim == pytest.approx(
        lp_0_blurred_image_2d.slim, 1.0e-4
    )
    assert lp_1_blurred_image_2d.shape_slim == 9
    assert blurred_image_2d_list[1].slim == pytest.approx(
        lp_1_blurred_image_2d.slim, 1.0e-4
    )

    assert blurred_image_2d_list[0].native == pytest.approx(
        lp_0_blurred_image_2d.native, 1.0e-4
    )
    assert blurred_image_2d_list[1].native == pytest.approx(
        lp_1_blurred_image_2d.native, 1.0e-4
    )


def test__unmasked_blurred_image_2d_via_psf_from():

    psf = ag.Kernel2D.manual_native(
        array=(np.array([[0.0, 3.0, 0.0], [0.0, 1.0, 2.0], [0.0, 0.0, 0.0]])),
        pixel_scales=1.0,
    )

    mask = ag.Mask2D.manual(
        mask=[[True, True, True], [True, False, True], [True, True, True]],
        pixel_scales=1.0,
        sub_size=1,
    )

    grid = ag.Grid2D.from_mask(mask=mask)

    lp = ag.lp.EllSersic(intensity=0.1)
    operate_lp = ag.OperateImage.from_light_obj(light_obj=lp)

    unmasked_blurred_image_2d = operate_lp.unmasked_blurred_image_2d_via_psf_from(
        grid=grid, psf=psf
    )

    print(unmasked_blurred_image_2d)

    assert unmasked_blurred_image_2d.native == pytest.approx(
        np.array(
            [
                [1.31618566e-01, 2.48460648e02, 1.91885830e-01],
                [9.66709359e-02, 8.29737297e01, 1.65678804e02],
                [4.12176698e-02, 8.74484826e-02, 1.01484934e-01],
            ]
        ),
        1.0e-4,
    )


def test__unmasked_blurred_image_2d_list_via_psf_from():
    psf = ag.Kernel2D.manual_native(
        array=(np.array([[0.0, 3.0, 0.0], [0.0, 1.0, 2.0], [0.0, 0.0, 0.0]])),
        pixel_scales=1.0,
    )

    mask = ag.Mask2D.manual(
        mask=[[True, True, True], [True, False, True], [True, True, True]],
        pixel_scales=1.0,
        sub_size=1,
    )

    grid = ag.Grid2D.from_mask(mask=mask)

    lp_0 = ag.lp.EllSersic(intensity=1.0)
    lp_1 = ag.lp.EllSersic(intensity=2.0)

    padded_grid = grid.padded_grid_from(kernel_shape_native=psf.shape_native)

    manual_blurred_image_0 = lp_0.image_2d_from(grid=padded_grid)
    manual_blurred_image_0 = psf.convolved_array_from(array=manual_blurred_image_0)

    manual_blurred_image_1 = lp_1.image_2d_from(grid=padded_grid)
    manual_blurred_image_1 = psf.convolved_array_from(array=manual_blurred_image_1)

    gal = ag.Galaxy(redshift=0.5, lp_0=lp_0, lp_1=lp_1)

    operate_list = ag.OperateImage.from_light_obj(light_obj=gal)

    unmasked_blurred_image_2d_list = operate_list.unmasked_blurred_image_2d_list_via_psf_from(
        grid=grid, psf=psf
    )

    assert unmasked_blurred_image_2d_list[0].native == pytest.approx(
        manual_blurred_image_0.binned.native[1:4, 1:4], 1.0e-4
    )

    assert unmasked_blurred_image_2d_list[1].native == pytest.approx(
        manual_blurred_image_1.binned.native[1:4, 1:4], 1.0e-4
    )


def test__visibilities_from_grid_and_transformer(
    grid_2d_7x7, sub_grid_2d_7x7, transformer_7x7_7
):
    lp = ag.lp.EllSersic(intensity=1.0)
    operate_lp = ag.OperateImage.from_light_obj(light_obj=lp)

    lp_visibilities = operate_lp.visibilities_via_transformer_from(
        grid=grid_2d_7x7, transformer=transformer_7x7_7
    )

    image_2d = lp.image_2d_from(grid=grid_2d_7x7)
    visibilities = transformer_7x7_7.visibilities_from(image=image_2d.binned)

    assert visibilities == pytest.approx(lp_visibilities, 1.0e-4)


def test__visibilities_list_via_transformer_from(sub_grid_2d_7x7, transformer_7x7_7):

    lp_0 = ag.lp.EllSersic(intensity=1.0)
    lp_1 = ag.lp.EllSersic(intensity=2.0)

    lp_0_image = lp_0.image_2d_from(grid=sub_grid_2d_7x7)
    lp_1_image = lp_1.image_2d_from(grid=sub_grid_2d_7x7)

    lp_0_visibilities = transformer_7x7_7.visibilities_from(image=lp_0_image)
    lp_1_visibilities = transformer_7x7_7.visibilities_from(image=lp_1_image)

    gal = ag.Galaxy(redshift=0.5, lp_0=lp_0, lp_1=lp_1)

    operate_list = ag.OperateImage.from_light_obj(light_obj=gal)

    visibilities_list = operate_list.visibilities_list_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )

    assert (lp_0_visibilities == visibilities_list[0]).all()
    assert (lp_1_visibilities == visibilities_list[1]).all()
