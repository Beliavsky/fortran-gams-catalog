# Neural networks and nonlinear regression

The catalog classifies a supported task, not the neural-network label alone.
Existing approximation and differentiation mappings are retained.

| Repository | Added class | Reviewed entry point | Scope |
| --- | --- | --- | --- |
| [thchang/NN_MOD](https://github.com/thchang/NN_MOD) | L8e1b1 | `NEURALNET_MOD::NEURALNET%TRAIN` | Default squared-error gradient, internal SGD, scalar response; omit custom loss and regularization. |
| [modern-fortran/neural-fortran](https://github.com/modern-fortran/neural-fortran) | L8e1b1 | `nf::network%train` | Default quadratic loss and SGD for a continuous-response dense network. |
| [nedtaylor/athena](https://github.com/nedtaylor/athena) | L8e1b1 | `athena__network::network_type%train` | Compiled regression network configured with MSE and an unpenalized optimizer. |
| [scientific-computing/FKB](https://github.com/scientific-computing/FKB) | L8e | `mod_network::network_type%output` | Evaluation of an initialized or loaded continuous-response model. |
| [BerkeleyLab/fiats](https://github.com/BerkeleyLab/fiats) | L8e | `inference_engine_m::inference_engine_t%infer` | Tensor inference with continuous-response coefficients, activation and normalization metadata. |

**L8e1b1** is nonlinear ordinary-least-squares parameter estimation for unweighted
data, with no derivatives supplied by the caller. Internal backpropagation or
automatic differentiation does not mean that the user supplies a regression
Jacobian. The mapping applies to the squared-error configurations above, not to
all selectable losses or optimizers. Parent classes L8e1b, L8e1 and L8e include
these entries automatically. The labels follow the
[Netlib GAMS hierarchy](https://netlib.org/bib/gams.html).

Prediction-only mappings stop at **L8e**: a reviewed evaluation interface does
not establish a particular fitting method. FSKLEARN already has an L8e review.
Classification-only uses, automatic-differentiation utilities and differential-
equation solvers are not automatically classified as nonlinear regression.
ENNUF's currently reviewed dense/activation layer kernels remain under K; this
review does not establish a complete regression-model interface for them.

Each new mapping has a commit pin, normalized source-file hashes, procedure and
argument declaration ranges, and scope limitations in the
[independent review ledger](local-reviews.md). NN_MOD's author least-squares
example is a linear special case. Athena's sine example uses an optional W&B
application wrapper. Neither example was run for this review. No new driver was
compiled or executed, and no claim of convergence, global optimality,
uncertainty estimates or comparative accuracy is made.
