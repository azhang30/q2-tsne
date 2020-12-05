import qiime2.plugin
from qiime2.plugin import (Plugin, Properties, Int, Float, Str, Range, Bool)
import qiime2.sdk
from q2_types.distance_matrix import DistanceMatrix
from q2_types.ordination import PCoAResults
from q2_diversity import _beta as beta
import q2_tsne
from q2_tsne._tsne import (_joint_probabilities, _kl_divergence, _kl_divergence_bh, _tsne)

plugin = Plugin(
        name='tsne',
        version='0.0.1',
        website='https://github.com/azhang30/q2-tsne/blob/main/q2_tsne/plugin_setup.py',
        package='q2_tsne',
        description=('A t-SNE QIIME2 plugin for Adam Zhangs Final Project Fall 2020'),
        short_description='t-SNE QIIME2 plugin',
        )

plugin.methods.register_function(
        function=joint_probabilities,
        inputs={'X': DistanceMatrix},
        parameters={
            'distances': DistanceMatrix,
            'desired_perplexity': Float,
            'verbose': Int,
            },
        outputs=[('P', DistanceMatrix),
        ],
)

plugin.methods.register_function(
        function=kl_divergence,
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
)

plugin.methods.register_function(
        function=kl_divergence_bh,
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
)

plugin.methods.register_function(
        function=tsne,
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
            'distance_matrix': ('The distance matrix on which PCoA should be computed.')
            },
        output_descriptions={'pcoa': 'The resulting PCoA matrix.'}
)


