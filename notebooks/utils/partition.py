"""NIID partitioner based on class dropping."""

import random

import numpy as np
from datasets import ClassLabel, Dataset
from flwr_datasets.partitioner.partitioner import Partitioner


class MockPartitioner(Partitioner):
    """Mock partitioner that wraps a list of datasets."""

    def __init__(self, datasets: list[Dataset]) -> None:
        super().__init__()
        self._datasets = datasets

    def load_partition(self, partition_id: int) -> Dataset:
        """Load a single IID partition based on the partition index.

        Parameters
        ----------
        partition_id : int
            the index that corresponds to the requested partition

        Returns
        -------
        dataset_partition : Dataset
            single dataset partition
        """
        return self._datasets[partition_id]

    @property
    def num_partitions(self) -> int:
        """Total number of partitions."""
        return len(self._datasets)

    @property
    def dataset(self) -> Dataset:
        """Get the dataset property."""
        raise NotImplementedError("MockPartitioner does not support getting dataset.")

    @Partitioner.dataset.setter
    def dataset(self, value: Dataset) -> None:
        """Set the dataset property."""
        raise NotImplementedError("MockPartitioner does not support setting dataset.")


class ClassDropPartitioner(Partitioner):
    """Partitioner creates each partition sampled randomly from the dataset.

    Parameters
    ----------
    num_partitions : int
        The total number of partitions that the data will be divided into.
    seed : int, optional
        Random seed for deterministic partitioning. If not provided, a random seed will
        be generated.
    """

    def __init__(
        self,
        num_partitions: int,
        partition_by: str = "label",
        n_drop: int = 2,
        droppable: list[str] | None = None,
        seed: int | None = None,
    ) -> None:
        super().__init__()
        if num_partitions <= 0:
            raise ValueError("The number of partitions must be greater than zero.")
        self._num_partitions = num_partitions
        if seed is None:
            self._seed = random.randint(0, 2**10)
        else:
            self._seed = seed
        self._n_drop = n_drop
        self._partition_by = partition_by
        self._droppable = droppable

    def load_partition(self, partition_id: int) -> Dataset:
        """Load a single IID partition based on the partition index.

        Parameters
        ----------
        partition_id : int
            the index that corresponds to the requested partition

        Returns
        -------
        dataset_partition : Dataset
            single dataset partition
        """
        rng = np.random.default_rng(seed=self._seed + partition_id)

        cls_to_drop = rng.choice(self._droppable, size=self._n_drop, replace=False)
        return self.dataset.shard(
            num_shards=self._num_partitions, index=partition_id, contiguous=True
        ).filter(lambda x: x[self._partition_by] not in cls_to_drop)

    @property
    def num_partitions(self) -> int:
        """Total number of partitions."""
        return self._num_partitions

    @Partitioner.dataset.setter
    def dataset(self, value: Dataset) -> None:
        """Set the dataset property."""
        label = value.features[self._partition_by]
        classes = value.unique(self._partition_by)

        if self._droppable is not None:
            if isinstance(label, ClassLabel):
                self._droppable = [label.str2int(cls) for cls in self._droppable]

            self._droppable = [cls for cls in self._droppable if cls in classes]
        else:
            self._droppable = list(classes)

        if len(self._droppable) < self._n_drop:
            raise ValueError(
                f"Not enough droppable classes in the dataset. "
                f"Available: {len(classes)}, Droppable: {len(self._droppable)}"
            )

        ds = value.shuffle(seed=self._seed)
        Partitioner.dataset.fset(self, ds)


if __name__ == "__main__":
    # Test the partitioner with the NSL-KDD dataset.

    from collections import Counter

    from nslkdd import load_nslkdd

    ds = load_nslkdd()
    print(ds["train"].unique("label"))
    partitioner = ClassDropPartitioner(
        num_partitions=10,
        droppable=[
            "back",
            "httptunnel",
            "ipsweep",
            "neptune",
            "portsweep",
            "saint",
            "satan",
            "smurf",
        ],
    )
    partitioner.dataset = ds["train"]
    partition = partitioner.load_partition(partition_id=0)
    print(partition)
    print("Labels count:", Counter(partition["label"]))
    partbis = partitioner.load_partition(partition_id=0)
    print(partbis)
    print("Labels count:", Counter(partbis["label"]))
    assert partition.data == partbis.data, "Partitions should be equal"
    print("Partition labels:", len(partition.unique("label")))
    print("Dataset labels:", len(ds["train"].unique("label")))
