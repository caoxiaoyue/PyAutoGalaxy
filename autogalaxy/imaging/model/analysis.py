from astropy import cosmology as cosmo
from typing import Optional

import autofit as af
import autoarray as aa

from autogalaxy.analysis.analysis import AnalysisDataset
from autogalaxy.analysis.visualizer import Visualizer
from autogalaxy.hyper.hyper_data import HyperImageSky
from autogalaxy.hyper.hyper_data import HyperBackgroundNoise
from autogalaxy.imaging.model.result import ResultImaging
from autogalaxy.imaging.fit_imaging import FitImaging
from autogalaxy.plane.plane import Plane

from autogalaxy import exc


class AnalysisImaging(AnalysisDataset):
    def __init__(
        self,
        dataset: aa.Imaging,
        hyper_dataset_result: ResultImaging = None,
        cosmology=cosmo.Planck15,
        settings_pixelization: aa.SettingsPixelization = None,
        settings_inversion: aa.SettingsInversion = None,
    ):
        """
        Analysis classes are used by PyAutoFit to fit a model to a dataset via a non-linear search.

        An Analysis class defines the `log_likelihood_function` which fits the model to the dataset and returns the
        log likelihood value defining how well the model fitted the data. The Analysis class handles many other tasks,
        such as visualization, outputting results to hard-disk and storing results in a format that can be loaded after
        the model-fit is complete using PyAutoFit's database tools.

        This Analysis class is used for model-fits which fit galaxies (or objects containing galaxies like a `Plane`)
        to an imaging dataset.

        This class stores the settings used to perform the model-fit for certain components of the model (e.g. a
        pixelization or inversion), the Cosmology used for the analysis and hyper datasets used for certain model
        classes.

        Parameters
        ----------
        dataset
            The `Imaging` dataset that the model is fitted too.
        hyper_dataset_result
            The hyper-model image and hyper galaxies images of a previous result in a model-fitting pipeline, which are
            used by certain classes for adapting the analysis to the properties of the dataset.
        cosmology
            The Cosmology assumed for this analysis.
        settings_pixelization
            Settings controlling how a pixelization is fitted for example if a border is used when creating the
            pixelization.
        settings_inversion
            Settings controlling how an inversion is fitted for example which linear algebra formalism is used.
        """
        super().__init__(
            dataset=dataset,
            hyper_dataset_result=hyper_dataset_result,
            cosmology=cosmology,
            settings_pixelization=settings_pixelization,
            settings_inversion=settings_inversion,
        )

    @property
    def imaging(self):
        return self.dataset

    def log_likelihood_function(self, instance: af.ModelInstance) -> float:
        """
        Given an instance of the model, where the model parameters are set via a non-linear search, fit the model
        instance to the imaging dataset.

        This function returns a log likelihood which is used by the non-linear search to guide the model-fit.

        For this analysis class, this function performs the following steps:

        1) If the analysis has a hyper dataset, associated the model galaxy images of this dataset to the galaxies in
        the model instance.

        2) Extract attributes which model aspects of the data reductions, like the scaling the background sky
        and background noise.

        3) Extracts all galaxies from the model instance and set up a `Plane`.

        4) Use the `Plane` and other attributes to create a `FitImaging` object, which performs steps such as creating
        model images of every galaxy in the plane, blurring them with the imaging dataset's PSF and computing residuals,
        a chi-squared statistic and the log likelihood.

        Certain models will fail to fit the dataset and raise an exception. For example if an `Inversion` is used, the
        linear algebra calculation may be invalid and raise an Exception. In such circumstances the model is discarded
        and its likelihood value is passed to the non-linear search in a way that it ignores it (for example, using a
        value of -1.0e99).

        Parameters
        ----------
        instance
            An instance of the model that is being fitted to the data by this analysis (whose parameters have been set
            via a non-linear search).

        Returns
        -------
        float
            The log likelihood indicating how well this model instance fitted the imaging data.
        """

        self.associate_hyper_images(instance=instance)

        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)

        hyper_background_noise = self.hyper_background_noise_for_instance(
            instance=instance
        )

        plane = self.plane_for_instance(instance=instance)

        try:
            fit = self.fit_imaging_for_plane(
                plane=plane,
                hyper_image_sky=hyper_image_sky,
                hyper_background_noise=hyper_background_noise,
            )

            return fit.figure_of_merit
        except (
            exc.PixelizationException,
            exc.InversionException,
            exc.GridException,
        ) as e:
            raise exc.FitException from e

    def fit_imaging_for_plane(
        self,
        plane: Plane,
        hyper_image_sky: Optional[HyperImageSky],
        hyper_background_noise: Optional[HyperBackgroundNoise],
        use_hyper_scalings: bool = True,
    ) -> FitImaging:
        """
        Given a `Plane`, which the analysis constructs from a model instance, create a `FitImaging` object.

        This function is used in the `log_likelihood_function` to fit the model to the imaging data and compute the
        log likelihood.

        Parameters
        ----------
        plane
            The plane of galaxies whose model images are used to fit the imaging data.
        hyper_image_sky
            A model component which scales the background sky level of the data before computing the log likelihood.
        hyper_background_noise
            A model component which scales the background noise level of the data before computing the log likelihood.
        use_hyper_scalings
            If false, the scaling of the background sky and noise are not performed irrespective of the model components
            themselves.

        Returns
        -------
        FitImaging
            The fit of the plane to the imaging dataset, which includes the log likelihood.
        """
        return FitImaging(
            dataset=self.dataset,
            plane=plane,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
            use_hyper_scalings=use_hyper_scalings,
            settings_pixelization=self.settings_pixelization,
            settings_inversion=self.settings_inversion,
        )

    def visualize(
        self,
        paths: af.DirectoryPaths,
        instance: af.ModelInstance,
        during_analysis: bool,
    ) -> None:
        """
        Output images of the maximum log likelihood model inferred by the model-fit. This function is called throughout
        the non-linear search at regular intervals, and therefore provides on-the-fly visualization of how well the
        model-fit is going.

        The visualization performed by this function includes:

        - Images of the best-fit `Plane`, including the images of each of its galaxies.

        - Images of the best-fit `FitImaging`, including the model-image, residuals and chi-squared of its fit to
        the imaging data.

        - The hyper-images of the model-fit showing how the hyper galaxies are used to represent different galaxies in
        the dataset.

        - If hyper features are used to scale the noise or background sky, a `FitImaging` with these features turned
        off may be output, to indicate how much these features are altering the dataset.

        The images output by this function are customized using the file `config/visualize/plots.ini`.

        Parameters
        ----------
        paths
            The PyAutoFit paths object which manages all paths, e.g. where the non-linear search outputs are stored,
            visualization, and the pickled objects used by the aggregator output by this function.
        instance
            An instance of the model that is being fitted to the data by this analysis (whose parameters have been set
            via a non-linear search).
        during_analysis
            If True the visualization is being performed midway through the non-linear search before it is finished,
            which may change which images are output.
        """
        instance = self.associate_hyper_images(instance=instance)
        plane = self.plane_for_instance(instance=instance)
        hyper_image_sky = self.hyper_image_sky_for_instance(instance=instance)
        hyper_background_noise = self.hyper_background_noise_for_instance(
            instance=instance
        )

        fit = self.fit_imaging_for_plane(
            plane=plane,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
        )

        visualizer = Visualizer(visualize_path=paths.image_path)
        visualizer.visualize_imaging(imaging=self.imaging)
        visualizer.visualize_fit_imaging(fit=fit, during_analysis=during_analysis)

        if fit.inversion is not None:
            visualizer.visualize_inversion(
                inversion=fit.inversion, during_analysis=during_analysis
            )

        visualizer.visualize_hyper_images(
            hyper_galaxy_image_path_dict=self.hyper_galaxy_image_path_dict,
            hyper_model_image=self.hyper_model_image,
            plane=plane,
        )

        if visualizer.plot_fit_no_hyper:

            fit = self.fit_imaging_for_plane(
                plane=plane,
                hyper_image_sky=None,
                hyper_background_noise=None,
                use_hyper_scalings=False,
            )

            visualizer.visualize_fit_imaging(
                fit=fit, during_analysis=during_analysis, subfolders="fit_no_hyper"
            )

    def make_result(
        self, samples: af.PDFSamples, model: af.Collection, search: af.NonLinearSearch
    ) -> ResultImaging:
        """
        After the non-linear search is complete create its `Result`, which includes:

        - The samples of the non-linear search (E.g. MCMC chains, nested sampling samples) which are used to compute
        the maximum likelihood model, posteriors and other properties.

        - The model used to fit the data, which uses the samples to create specific instances of the model (e.g.
        an instance of the maximum log likelihood model).

        - The non-linear search used to perform the model fit.

        The `ResultImaging` object contains a number of methods which use the above objects to create the max
        log likelihood `Plane`, `FitImaging`, hyper-galaxy images,etc.

        Parameters
        ----------
        samples
            A PyAutoFit object which contains the samples of the non-linear search, for example the chains of an MCMC
            run of samples of the nested sampler.
        model
            The PyAutoFit model object, which includes model components representing the galaxies that are fitted to
            the imaging data.
        search
            The non-linear search used to perform this model-fit.

        Returns
        -------
        ResultImaging
            The result of fitting the model to the imaging dataset, via a non-linear search.
        """
        return ResultImaging(samples=samples, model=model, analysis=self, search=search)

    def save_attributes_for_aggregator(self, paths: af.DirectoryPaths):
        """
        Before the non-linear search begins, this routine saves attributes of the `Analysis` object to the `pickles`
        folder such that they can be load after the analysis using PyAutoFit's database and aggregator tools.

        For this analysis, it uses the `AnalysisDataset` object's method to output the following:

        - The dataset's data.
        - The dataset's noise-map.
        - The settings associated with the dataset.
        - The settings associated with the inversion.
        - The settings associated with the pixelization.
        - The Cosmology.
        - The hyper dataset's model image and galaxy images, if used.

        This function also outputs attributes specific to an imaging dataset:

       - Its PSF.
       - Its mask.

        It is common for these attributes to be loaded by many of the template aggregator functions given in the
        `aggregator` modules. For example, when using the database tools to perform a fit, the default behaviour is for
        the dataset, settings and other attributes necessary to perform the fit to be loaded via the pickle files
        output by this function.

        Parameters
        ----------
        paths
            The PyAutoFit paths object which manages all paths, e.g. where the non-linear search outputs are stored, visualization,
            and the pickled objects used by the aggregator output by this function.
        """
        super().save_attributes_for_aggregator(paths=paths)

        paths.save_object("psf", self.dataset.psf_unormalized)
        paths.save_object("mask", self.dataset.mask)
