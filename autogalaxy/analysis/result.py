import numpy as np
from typing import Dict, Union

from autoconf import conf
import autofit as af
import autoarray as aa

from autogalaxy.galaxy.galaxy import Galaxy
from autogalaxy.plane.plane import Plane


class Result(af.Result):
    def __init__(
        self,
        samples: af.PDFSamples,
        model: af.Collection,
        analysis,
        search: af.NonLinearSearch,
    ):
        """
        After the non-linear search of a fit to a dataset is complete it creates a `Result` object which includes:

        - The samples of the non-linear search (E.g. MCMC chains, nested sampling samples) which are used to compute
        the maximum likelihood model, posteriors and other properties.

        - The model used to fit the data, which uses the samples to create specific instances of the model (e.g.
        an instance of the maximum log likelihood model).

        - The non-linear search used to perform the model fit.

        This class contains a number of methods which use the above objects to create the max log likelihood `Plane`,
        `FitIamging`, hyper-galaxy images,etc.

        Parameters
        ----------
        samples
            A PyAutoFit object which contains the samples of the non-linear search, for example the chains of an MCMC
            run of samples of the nested sampler.
        model
            The PyAutoFit model object, which includes model components representing the galaxies that are fitted to
            the imaging data.
        analysis
            The `Analysis` object that was used to perform the model-fit from which this result is inferred.
        search
            The non-linear search used to perform this model-fit.

        Returns
        -------
        ResultImaging
            The result of fitting the model to the imaging dataset, via a non-linear search.
        """
        super().__init__(samples=samples, model=model, search=search)

        self.analysis = analysis

    @property
    def max_log_likelihood_plane(self) -> Plane:
        """
        An instance of a `Plane` corresponding to the maximum log likelihood model inferred by the non-linear search.
        """
        instance = self.analysis.associate_hyper_images(instance=self.instance)

        return self.analysis.plane_for_instance(instance=instance)

    @property
    def path_galaxy_tuples(self) -> [(str, Galaxy)]:
        """
        Tuples associating the names of galaxies with instances from the best fit
        """
        return self.instance.path_instance_tuples_for_class(cls=Galaxy)


class ResultDataset(Result):
    @property
    def mask(self) -> aa.Mask2D:
        """
        The 2D mask applied to the dataset for the model-fit.
        """
        return self.max_log_likelihood_fit.mask

    @property
    def dataset(self) -> Union[aa.Imaging, aa.Interferometer]:
        """
        The dataset that was fitted by the model-fit.
        """
        return self.max_log_likelihood_fit.dataset

    @property
    def pixelization_list(self):
        """
        A list of all pixelization classes used by the model-fit.
        """
        return self.max_log_likelihood_plane.pixelization_list

    def image_for_galaxy(self, galaxy: Galaxy) -> np.ndarray:
        """
        Given an instance of a `Galaxy` object, return an image of the galaxy via the the maximum log likelihood fit.

        This image is extracted via the fit's `galaxy_model_image_dict`, which is necessary to make it straight
        forward to use the image as hyper-images.

        Parameters
        ----------
        galaxy
            A galaxy used by the model-fit.

        Returns
        -------
        ndarray or None
            A numpy arrays giving the model image of that galaxy.
        """
        return self.max_log_likelihood_fit.galaxy_model_image_dict[galaxy]

    @property
    def image_galaxy_dict(self) -> {str: Galaxy}:
        """
        A dictionary associating galaxy names with model images of those galaxies.

        This is used for creating the hyper-dataset used by Analysis objects to adapt aspects of a model to the dataset
        being fitted.
        """
        return {
            galaxy_path: self.image_for_galaxy(galaxy)
            for galaxy_path, galaxy in self.path_galaxy_tuples
        }

    @property
    def hyper_galaxy_image_path_dict(self) -> Dict[str, aa.Array2D]:
        """
        A dictionary associating 1D hyper galaxy images with their names.
        """

        hyper_minimum_percent = conf.instance["general"]["hyper"][
            "hyper_minimum_percent"
        ]

        hyper_galaxy_image_path_dict = {}

        for path, galaxy in self.path_galaxy_tuples:

            galaxy_image = self.image_galaxy_dict[path]

            if not np.all(galaxy_image == 0):
                minimum_galaxy_value = hyper_minimum_percent * max(galaxy_image)
                galaxy_image[galaxy_image < minimum_galaxy_value] = minimum_galaxy_value

            hyper_galaxy_image_path_dict[path] = galaxy_image

        return hyper_galaxy_image_path_dict

    @property
    def hyper_model_image(self) -> aa.Array2D:
        """
        The hyper model image used by Analysis objects to adapt aspects of a model to the dataset being fitted.

        The hyper model image is the sum of the hyper galaxy image of every individual galaxy.
        """
        hyper_model_image = aa.Array2D.manual_mask(
            array=np.zeros(self.mask.mask_sub_1.pixels_in_mask),
            mask=self.mask.mask_sub_1,
        )

        for path, galaxy in self.path_galaxy_tuples:
            hyper_model_image += self.hyper_galaxy_image_path_dict[path]

        return hyper_model_image
