import tensorflow as tf
from nslkdd import load_nslkdd

# Load the dataset from disk
dataset = load_nslkdd()

print(dataset)

# Identify categorical and numerical features
categorical_features = [
    "protocol_type",
    "service",
    "flag",
]
numerical_features = [
    col
    for col, feat in dataset["train"].features.items()
    if col not in ["label", "binary_label"] and col not in categorical_features
]
feature_columns = numerical_features + categorical_features


def dict_to_tensor(features, label):
    # Stack all features as float32
    x = tf.stack(
        [tf.cast(features[col], tf.float32) for col in feature_columns], axis=-1
    )
    return x, label


# Prepare the tf.data.Dataset for training
train_tf = (
    dataset["train"]
    .to_tf_dataset(
        columns=feature_columns, label_cols="binary_label", shuffle=True, batch_size=256
    )
    .map(dict_to_tensor)
)
test_tf = (
    dataset["test"]
    .to_tf_dataset(
        columns=feature_columns,
        label_cols="binary_label",
        shuffle=False,
        batch_size=256,
    )
    .map(dict_to_tensor)
)


# Build a simple ANN model
model = tf.keras.Sequential(
    [
        tf.keras.layers.Input(shape=(len(feature_columns),)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ]
)

print(model.summary())

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])


# Train the model
model.fit(train_tf, epochs=10)  # , validation_data=test_tf)


# Evaluate
loss, acc = model.evaluate(test_tf)
print(f"Test accuracy: {acc:.4f}")
