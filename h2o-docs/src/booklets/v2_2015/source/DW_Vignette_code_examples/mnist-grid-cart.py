import h2o
from h2o.estimators.deepwater import H2ODeepWaterEstimator

# Start or connect to H2O
h2o.init(nthreads=-1, strict_version_check=False)

# Import data and transform data
train = h2o.import_file("bigdata/laptop/mnist/train.csv.gz")

features = list(range(0,784))
target = 784

train[target] = train[target].asfactor()

# Set up grid
hidden_opt = [[200,200], [1024,1024]]
learn_rate_opt = [1e-6, 1e-5]
hyper_parameters = {"hidden": hidden_opt, "learning_rate":learn_rate_opt}

# Build model and train model grid
from h2o.grid.grid_search import H2OGridSearch
model_grid = H2OGridSearch(H2ODeepWaterEstimator, hyper_params=hyper_parameters)

model_grid.train(x=features, y=target, training_frame=train, epochs=100, activation="Rectifier", ignore_const_cols=False, mini_batch_size=256, input_dropout_ratio=0.1, hidden_dropout_ratios=[0.5,0.5], stopping_rounds=3, stopping_tolerance=0.05, stopping_metric="misclassification", score_interval=2, score_duty_cycle=0.5, score_training_samples=1000, score_validation_samples=1000, nfolds=5, gpu=True, seed=1234)

# Evaluate model
print(model_grid)
