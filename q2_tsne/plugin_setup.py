import qiime2.plugin
from qiime2.plugin import (Plugin, Properties, Int, Float, Str, Range, Bool)
import qiime2.sdk
from q2_types.distance_matrix import DistanceMatrix
from q2_types.ordination import PCoAResults
from q2_diversity import _beta as beta
import q2_tsne
from q2_tsne._t_sne import (_joint_probabilities, _kl_divergence, _kl_divergence_bh, __init__)

plugin = qiime2.plugin.Plugin(
        name='tsne',
        version='0.0.1',
        website='github.com/scikit-learn/scikit-learn/blob/0fb307bf3/sklearn/manifold/_t_sne.py#L476',
        package='q2_tsne',
        description=('A t-SNE QIIME2 plugin for Adam Zhangs Final Project Fall 2020'),
        short_description='t-SNE QIIME2 plugin',
        )

plugin.methods.register_function(
        function=_joint_probabilities,
        inputs={'X': DistanceMatrix},
        parameters={
            'distances': DistanceMatrix,
            'desired_perplexity': Float,
            'verbose': Int,
            },
        outputs=[('P', DistanceMatrix),
        ],
        input_descriptions={
            'X': ('Distance Matrix output from QIIME 2 beta diversity analysis on which PCoA is computed')
            },
        parameter_descriptions={
            'distances': ('Distances of samples stored as one-dimensional matrices'),
            'desired_perplexity': ('Desired perplexity of joint probability distributions, default 30'),
            'verbose': ('Verbosity level, default 0')
            },
        output_descriptions={'P': 'Condensed joint probability matrix'},
        name='Joint Probabilities',
        description=('Compute joint probabilities p_ij from distances.')
)

plugin.methods.register_function(
        function=_kl_divergence,
        inputs={'X': DistanceMatrix},
        parameters={
            'params': DistanceMatrix,
            'P': DistanceMatrix,
            'degrees_of_freedom': Int,
            'n_samples': Int,
            'n_components': Int,
            'skip_num_points': Int,
            'compute_error': Bool,

        },
        outputs=[('kl_divergence', Float),
                 ('grad', DistanceMatrix)
        ],
        input_descriptions={
            'X': ('Distance Matrix output from QIIME 2 beta diversity analysis on which PCoA is computed')
            },
        parameter_descriptions={
            'params': ('Unraveled embedding'),
            'P': ('Condensed joint probability matrix'),
            'degrees_of_freedom': ('Student t-dist DoF'),
            'n_samples': ('Number of samples'),
            'n_components': ('Dimension of embedded space'),
            'skip_num_points': ('Gradient is not computed for points with indices below this threshold'),
            'compute_error': ('kl_divergence not computed if False')
            },
        output_descriptions={'kl_divergence': 'Kullback-Leibler divergence of p_ij and q_ij',
                             'grad': 'Unraveled gradient of the KL divergence with respect to embedding'},
        name='Kullback-Leibler divergence',
        description='t-SNE objective function: gradient of the KL divergence of p_ijs and q_ijs with absolute error'
)

plugin.methods.register_function(
        function=_kl_divergence_bh,
        inputs={'X': DistanceMatrix},
        parameters={
            'params': DistanceMatrix,
            'P': DistanceMatrix,
            'degrees_of_freedom': Int,
            'n_samples': Int,
            'n_components': Int,
            'angle': Float,
            'skip_num_points': Int,
            'verbose': Int,
            'compute_error': Bool,
            'num_threads': Int
        },
        outputs=[('kl_divergence', Float),
                 ('grad', DistanceMatrix)
        ],
        input_descriptions={
            'X': ('Distance Matrix output from QIIME 2 beta diversity analysis on which PCoA is computed')
            },
        parameter_descriptions={
            'params': ('Unraveled embedding'),
            'P': ('Condensed joint probability matrix'),
            'degrees_of_freedom': ('Student t-dist DoF'),
            'n_samples': ('Number of samples'),
            'n_components': ('Dimension of embedded space'),
            'angle': ('Angular size used in Barnes-Hut t-SNE'),
            'skip_num_points': ('Gradient is not computed for points with indices below this threshold'),
            'verbose': ('Verbosity level, default 0'),
            'compute_error': ('kl_divergence not computed if False'),
            'num_threads': ('Number of threads used to compute the gradient.')
            },
        output_descriptions={'kl_divergence': 'Kullback-Leibler divergence of p_ij and q_ij',
                             'grad': 'Unraveled gradient of the KL divergence with respect to embedding'},
        name='Barnes-Hut Kullback-Leibler divergence',
        description='t-SNE objective function: gradient of the KL divergence of p_ijs and q_ijs using Barnes-Hut tree methods to calculate the gradient that runs in 0(NlogN) instead of 0(N^2)'
)

plugin.methods.register_function(
        function=__init__,
        inputs={'X': DistanceMatrix},
        parameters={
            'n_components': Int,
            'perplexity': Float,
            'early_exaggeration': Float,
            'learning_rate': Float,
            'n_iter': Int,
            'n_iter_without_progress': Int,
            'min_grad_norm': Float,
            'metric': String,
            'init': String,
            'verbose': Int,
            'random_state': Int,
            'method': String,
            'angle': Float,
            'n_jobs': Int,
        },
        outputs=[('pcoa', PCoAResults),
        ],
        input_descriptions={
            'X': ('Distance Matrix output from QIIME 2 beta diversity analysis on which PCoA is computed')
            },
        parameter_descriptions={
            'n_components': ('Dimension of the embedded space, default 2'),
            'perplexity': ('Number of nearest neighbors that is used in other manifold learning algorithms, default 30'),
            'early_exaggeration': ('Controls how tight natural clusters in the original space are in the embedded space and how much space will be between them, default 12'),
            'learning_rate': ('The learning rate, default 200'),
            'n_iter': ('Max number of iterations for optimization, default 1000'),
            'n_iter_without_progress': ('Max number of iterations without progress before abort, default 300'),
            'min_grad_norm': ('Optimization is stopped if gradient norm falls below threshold, default 1e-7'),
            'metric': ('Metric to use when calculating distance between instances in a feature array, default is assumed to be distance matrix'),
            'init': ('Initialization of embedding, default random'),
            'verbose': ('Verbosity level, default 0'),
            'random_state': ('Determine the random number generator, default None'),
            'method': ('Gradient calculation algorithm, default is Barnes-Hut'),
            'angle': ('Angular sized used with Barnes-Hut, default 0.5'),
            'n_jobs': ('Number of parallel jobs to run for neighbors search')
            },
        output_descriptions={'pcoa': 'The resulting PCoA matrix.'},
        name='t-SNE',
        description='t-SNE is a tool to visualize high-dimensional data. It converts similarities between data points to joint probabilities and tries to minimize the Kullback-Leibler divergence between the joint probabilities of the low-dimensional embedding and the high-dimensional data.'
)


