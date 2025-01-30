from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `datasets` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `directory_path` VARCHAR(255) NOT NULL,
    `sample_count` INT NOT NULL,
    `metadata` JSON,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `parent_id` INT,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_datasets_datasets_9d1e4717` FOREIGN KEY (`parent_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_datasets_users_eff16096` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `images` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `file_path` VARCHAR(255) NOT NULL UNIQUE,
    `metadata` JSON,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `dataset_id` INT NOT NULL,
    CONSTRAINT `fk_images_datasets_25ef7ef6` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `models` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `trainings` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `experiment_name` VARCHAR(255) NOT NULL UNIQUE,
    `precision` DOUBLE NOT NULL,
    `recall` DOUBLE NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `dataset_id` INT NOT NULL,
    `model_id` INT NOT NULL,
    CONSTRAINT `fk_training_datasets_b3bd7ba2` FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_training_models_01425669` FOREIGN KEY (`model_id`) REFERENCES `models` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `datasets`;
        DROP TABLE IF EXISTS `models`;
        DROP TABLE IF EXISTS `trainings`;
        DROP TABLE IF EXISTS `images`;"""
