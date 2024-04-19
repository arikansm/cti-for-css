import tensorflow as tf


class DependencyChecker:
    @staticmethod
    def is_gpu_usage_available() -> bool:
        return len(tf.config.list_physical_devices('GPU')) > 0
