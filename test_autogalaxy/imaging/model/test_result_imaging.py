import numpy as np

import autofit as af
import autogalaxy as ag

from autogalaxy.imaging.model.result import ResultImaging

from autogalaxy.mock import mock


class TestResultImaging:
    def test___image_dict(self, analysis_imaging_7x7):

        galaxies = af.ModelInstance()
        galaxies.galaxy = ag.Galaxy(redshift=0.5)
        galaxies.source = ag.Galaxy(redshift=1.0)

        instance = af.ModelInstance()
        instance.galaxies = galaxies

        samples = mock.MockSamples(max_log_likelihood_instance=instance)

        result = ResultImaging(
            samples=samples, analysis=analysis_imaging_7x7, model=None, search=None
        )

        image_dict = result.image_galaxy_dict
        assert isinstance(image_dict[("galaxies", "galaxy")], np.ndarray)
        assert isinstance(image_dict[("galaxies", "source")], np.ndarray)

        result.instance.galaxies.light = ag.Galaxy(redshift=0.5)

        image_dict = result.image_galaxy_dict
        assert (image_dict[("galaxies", "galaxy")].native == np.zeros((7, 7))).all()
        assert isinstance(image_dict[("galaxies", "source")], np.ndarray)
